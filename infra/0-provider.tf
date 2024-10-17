terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  shared_config_files      = ["/Users/juan/.aws/config"]
  shared_credentials_files = ["/Users/juan/.aws/credentials"]
  profile                  = "default"

  default_tags {
    tags = {
      owner       = "Juan Roldan"
      project     = "AWS ECS 10K-for-10M"
      cost-center = "AWS ECS 10K-for-10M Billing"
      environment = var.env
      app_name    = var.app_name
      Name        = "Managed by Terraform"
    }
  }
}
