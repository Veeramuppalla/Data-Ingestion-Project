
### To Archive the python code for lambda function
data "archive_file" "lambda_code" {
  type        = "zip"
  source_dir  = "C:/Users/yashz/project/data_ingestion_project/src/ingestion_lambda_function_raw/"  # Update with the path to your Lambda function code directory
  output_path = "C:/Users/yashz/project/data_ingestion_project/src/ingestion_lambda_function_raw/lambda.zip"  # Update with the desired path and name for the Lambda function code archive
}


resource "aws_lambda_function" "ingest-source-raw-data-tf" {
  function_name    = "ingest-source-raw-data-tf"
  role             = aws_iam_role.iam_role_lambda_tf.arn
  handler          = "lambda.lambda_handler"
  timeout          = 900
  runtime          = "python3.10"   # Update with the appropriate Python version
  filename         = data.archive_file.lambda_code.output_path

  ephemeral_storage {
    size = 512
  }

  environment {
    variables = {
      codebucket = "source-system-config"
    }
    
  }
}
