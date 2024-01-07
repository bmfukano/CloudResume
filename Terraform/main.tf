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

variable "lambda_dynmanodb_key" {
  type = string
}

variable "dynamodb_table" {
  type = string
}

resource "aws_lambda_function" "update_visitor_count" {

  filename    = "${path.module}/../Lambda/update_visitor_count.zip"
  function_name = "updateVisitorCount"
  role          = "arn:aws:iam::148984741960:role/LambaReadWriteVisitorCount"
  runtime       = "python3.12"
  handler       = "update_visitor_count.lambda_handler"
  publish       = false
  environment {
    variables = {
      "${var.lambda_dynmanodb_key}" = var.dynamodb_table
    }
  }
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

resource "aws_apigatewayv2_route" "update_visitor_count_route" {
  api_id    = aws_apigatewayv2_api.resume_visitor_count.id
  route_key = "GET /updateVisitorCount"
  target    = "integrations/${aws_apigatewayv2_integration.update_visitor_count_integration.id}"
}

resource "aws_apigatewayv2_integration" "update_visitor_count_integration" {
  api_id           = aws_apigatewayv2_api.resume_visitor_count.id
  integration_type = "AWS_PROXY"

  connection_type           = "INTERNET"
  integration_method        = "POST"
  passthrough_behavior      = "WHEN_NO_MATCH"
  payload_format_version    = "2.0"
  integration_uri        = "arn:aws:lambda:us-east-1:148984741960:function:updateVisitorCount"
}
