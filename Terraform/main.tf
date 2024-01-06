terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.31.0"
    }
  }
}

provider "aws" {
    region = "us-east-1"
}

provider "aws" {
    alias = "us-east-2"

    region = "us-east-2"
}

resource "aws_s3_bucket" "website_bucket" {
    bucket = "brianfukanoresume"

    provider = aws.us-east-2
}

resource "aws_lambda_function" "update_visitor_count" {

  filename    = "${path.module}/../Lambda/update_visitor_count.zip"
  function_name = "updateVisitorCount"
  role          = "arn:aws:iam::148984741960:role/LambaReadWriteVisitorCount"
  runtime       = "python3.12"
  handler       = "update_visitor_count.lambda_handler"
  publish       = false
}

resource "aws_apigatewayv2_api" "resume_visitor_count" {
  name        = "resumeVisitorCount"
  protocol_type = "HTTP"

  cors_configuration {
          allow_credentials = false
          allow_headers     = []
          allow_methods     = [
              "GET",
            ]
          allow_origins     = [
              "*",
            ]
          expose_headers    = []
          max_age           = 0
  }
}
