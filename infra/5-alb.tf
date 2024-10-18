resource "aws_lb" "ecs_alb" {
  name               = "ecs-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_security_group.id]
  subnets            = [aws_subnet.subnet.id, aws_subnet.subnet2.id]

  tags = {
    Name = "ecs-alb"
  }
}

resource "aws_lb_listener" "ecs_alb_listener" {
  load_balancer_arn = aws_lb.ecs_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_tg.arn
  }
}

resource "aws_lb_target_group" "ecs_tg" {
  name     = "ecs-target-group"
  port     = 80
  protocol = "HTTP"

  # target_type = "ip": This is necessary because ECS Fargate tasks are provisioned with an IP address in the AWS VPC network,
  # and the load balancer needs to route traffic to the IP addresses of these tasks rather than an EC2 instance ID.
  target_type = "ip"

  vpc_id = aws_vpc.main.id

  health_check {
    path                = "/nginx-health-check"
    interval            = 30        # Interval between health checks
    timeout             = 5         # Timeout for the response from the target
    healthy_threshold   = 3         # Number of consecutive successes to mark as healthy
    unhealthy_threshold = 3         # Number of consecutive failures to mark as unhealthy
    matcher             = "200-299" # Expected response status codes
  }
}
