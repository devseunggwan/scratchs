data "archive_file" "python_lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/src.zip"
}

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function
resource "aws_lambda_function" "test_lambda" {
  # architectures    = ["x86_64"]
  function_name = "test_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  role          = "write your role arn"
  timeout       = 60
  memory_size   = 128

  # zip 파일 업로드
  package_type     = "Zip"
  filename         = data.archive_file.python_lambda_package.output_path
  source_code_hash = filebase64sha256(data.archive_file.python_lambda_package.output_path)

  # 이미지(ECR) 업로드
  # package_type     = "Image"
  # image_uri = ""

  # Klayers Layer: https://github.com/keithrozario/Klayers/tree/master/deployments/python3.11
  layers = [
    "arn:aws:lambda:ap-northeast-2:770693421928:layer:Klayers-p311-cryptography:7",
    "arn:aws:lambda:ap-northeast-2:770693421928:layer:Klayers-p311-pandas:10",
  ]

  environment {
    variables = {
      foo = "bar"
    }
  }
  tags = {
    Environment = "dev"
  }

  depends_on = [data.archive_file.python_lambda_package]
}