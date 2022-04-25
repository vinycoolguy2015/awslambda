resource "aws_api_gateway_rest_api" "parameter_store" {
  name = "parameter_store"
  endpoint_configuration {
    types            = ["PRIVATE"]
    vpc_endpoint_ids = [aws_vpc_endpoint.api_gateway_endpoint.id]
  }
}

resource "aws_api_gateway_resource" "parameter_store" {
  parent_id   = aws_api_gateway_rest_api.parameter_store.root_resource_id
  path_part   = "get_parameter"
  rest_api_id = aws_api_gateway_rest_api.parameter_store.id
}

resource "aws_api_gateway_method" "parameter_store_method" {
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.parameter_store.id
  rest_api_id   = aws_api_gateway_rest_api.parameter_store.id
}

resource "aws_api_gateway_integration" "parameter_store_integration" {
  http_method             = aws_api_gateway_method.parameter_store_method.http_method
  resource_id             = aws_api_gateway_resource.parameter_store.id
  rest_api_id             = aws_api_gateway_rest_api.parameter_store.id
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.parameter_store_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.parameter_store_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.parameter_store.execution_arn}/*/*"
  #source_arn    = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.parameter_store.id}/*"
}

resource "aws_api_gateway_rest_api_policy" "parameter_store_policy" {
  rest_api_id = aws_api_gateway_rest_api.parameter_store.id
  policy      = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": "${aws_api_gateway_rest_api.parameter_store.execution_arn}/*"
        },
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": "${aws_api_gateway_rest_api.parameter_store.execution_arn}/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:SourceVpce": "${aws_vpc_endpoint.api_gateway_endpoint.id}"
                }
            }
        }
    ]
}
EOF
}

resource "aws_api_gateway_deployment" "default_deployment" {
  rest_api_id = aws_api_gateway_rest_api.parameter_store.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.parameter_store.id,
      aws_api_gateway_method.parameter_store_method.id,
      aws_api_gateway_integration.parameter_store_integration.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "default_deployment" {
  deployment_id = aws_api_gateway_deployment.default_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.parameter_store.id
  stage_name    = "default"
}
