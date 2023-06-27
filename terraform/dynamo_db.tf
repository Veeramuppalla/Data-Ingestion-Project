resource "aws_dynamodb_table" "data-ingestion-audit-tf" {
  name           = "data-ingestion-audit-tf"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key = "SK"
  attribute {
    name = "PK"
    type = "S"
  } 
  attribute {
    name = "SK"
    type = "S"
  }
}


data "aws_iam_policy_document" "dynamo_db_policy" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:*"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "dynamo_db_policy_tf" {
  name   = "dynamo_db_policy_tf"
  policy = data.aws_iam_policy_document.dynamo_db_policy.json

}

resource "aws_iam_role_policy_attachment" "aws_dynamo_db_policy_attachment_tf" {
  role       = aws_iam_role.iam_role_lambda_tf.name
  policy_arn = aws_iam_policy.dynamo_db_policy_tf.arn
} 