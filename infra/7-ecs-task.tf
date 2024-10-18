resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "main"
  subnet_ids = [aws_subnet.subnet.id, aws_subnet.subnet2.id]

  tags = {
    Name = "DB subnet group"
  }
}

resource "aws_db_parameter_group" "postgres" {
  name   = "my-pg"
  family = "postgres16"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "postgres" {
  identifier             = "postgres-db"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "postgresdb" # DBName must begin with a letter and contain only alphanumeric characters.
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  username               = "juan"
  password               = "justfortestingpurposes"
  parameter_group_name   = aws_db_parameter_group.postgres.name
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.db_security_group.id]
}

resource "aws_ecs_task_definition" "custom_nginx_flask_task" {
  family                   = "weather-app-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = "arn:aws:iam::account-id:role/ecsTaskExecutionRole"
  cpu                      = 1024
  memory                   = 2048

  container_definitions = jsonencode([
    {
      name        = "redis"
      image       = "redis:alpine"
      cpu         = 0
      memory      = 256
      networkMode = "awsvpc"
      command     = ["redis-server", "--loglevel", "verbose"]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/log-group/${var.app_name}/${var.env}/redis"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = 6379
          hostPort      = 6379
        }
      ]
      healthCheck = {
        command     = ["CMD-SHELL", "redis-cli ping"]
        interval    = 10
        timeout     = 5
        retries     = 3
        startPeriod = 10
      }
    },
    {
      name        = "data-populator"
      image       = "juanroldan1989/data-populator:latest"
      cpu         = 128
      memory      = 256
      networkMode = "awsvpc"
      essential   = false
      environment = [
        { "name" : "POSTGRES_USER", "value" : "juan" },
        { "name" : "POSTGRES_PASSWORD", "value" : "justfortestingpurposes" },
        { "name" : "POSTGRES_HOST", "value" : aws_db_instance.postgres.address },
        { "name" : "POSTGRES_DB", "value" : aws_db_instance.postgres.db_name },
        { "name" : "BATCH_SIZE", "value" : "10000" },
        { "name" : "TOTAL_RECORDS", "value" : "100000" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/log-group/${var.app_name}/${var.env}/data-populator"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "data-query"
      image       = "juanroldan1989/data-query:latest"
      cpu         = 128
      memory      = 256
      networkMode = "awsvpc"
      essential   = false
      depends_on = [
        { "containerName" : "data-populator", "condition" : "SUCCESS" }
      ]
      environment = [
        { "name" : "POSTGRES_USER", "value" : "juan" },
        { "name" : "POSTGRES_PASSWORD", "value" : "justfortestingpurposes" },
        { "name" : "POSTGRES_HOST", "value" : aws_db_instance.postgres.address },
        { "name" : "POSTGRES_DB", "value" : aws_db_instance.postgres.db_name }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/log-group/${var.app_name}/${var.env}/data-query"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "flask"
      image       = "juanroldan1989/flask:latest"
      cpu         = 128
      memory      = 256
      networkMode = "awsvpc"
      essential   = true
      dependsOn = [
        { "containerName" : "redis", "condition" : "HEALTHY" },
        { "containerName" : "data-populator", "condition" : "COMPLETE" }, # "data-populator" container is not essential
        { "containerName" : "data-query", "condition" : "COMPLETE" }      # "data-query" container is not essential
      ]
      environment = [
        { "name" : "POSTGRES_USER", "value" : "juan" },
        { "name" : "POSTGRES_PASSWORD", "value" : "justfortestingpurposes" },
        { "name" : "POSTGRES_HOST", "value" : aws_db_instance.postgres.address },
        { "name" : "POSTGRES_DB", "value" : aws_db_instance.postgres.db_name },
        { "name" : "USE_POOLING", "value" : "true" },
        { "name" : "POOL_MINCONN", "value" : "5" },
        { "name" : "POOL_MAXCONN", "value" : "15" },
        { "name" : "CACHE", "value" : "true" },
        { "name" : "CACHE_EXPIRY", "value" : "300" },
        { "name" : "REDIS_HOST", "value" : "redis" },
        { "name" : "REDIS_PORT", "value" : "6379" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/log-group/${var.app_name}/${var.env}/flask"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
      healthCheck = {
        command     = ["CMD-SHELL", "curl --silent --fail http://localhost:5000/health-check || exit 1"]
        interval    = 10
        timeout     = 10
        retries     = 3
        startPeriod = 30
      }
    },
    {
      name        = "nginx"
      image       = "juanroldan1989/nginx:latest"
      cpu         = 128
      memory      = 256
      networkMode = "awsvpc"
      dependsOn = [
        { "containerName" : "flask", "condition" : "HEALTHY" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/log-group/${var.app_name}/${var.env}/nginx"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    },
  ])

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}
