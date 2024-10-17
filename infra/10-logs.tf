resource "aws_cloudwatch_log_group" "db_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/db"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "db_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/db"
  log_group_name = aws_cloudwatch_log_group.db_log_group.name
}

resource "aws_cloudwatch_log_group" "redis_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/redis"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "redis_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/redis"
  log_group_name = aws_cloudwatch_log_group.redis_log_group.name
}

resource "aws_cloudwatch_log_group" "data_populator_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/data-populator"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "data_populator_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/data-populator"
  log_group_name = aws_cloudwatch_log_group.data_populator_log_group.name
}

resource "aws_cloudwatch_log_group" "data_query_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/data-query"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "data_query_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/data-query"
  log_group_name = aws_cloudwatch_log_group.data_query_log_group.name
}

resource "aws_cloudwatch_log_group" "flask_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/flask"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "flask_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/flask"
  log_group_name = aws_cloudwatch_log_group.flask_log_group.name
}

resource "aws_cloudwatch_log_group" "nginx_log_group" {
  name              = "/ecs/log-group/${var.app_name}/${var.env}/nginx"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "nginx_log_stream" {
  name           = "/ecs/log-stream/${var.app_name}/${var.env}/nginx"
  log_group_name = aws_cloudwatch_log_group.nginx_log_group.name
}
