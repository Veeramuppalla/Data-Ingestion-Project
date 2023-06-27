## Creating a IAM Policy Document for Assume Role

data "aws_iam_policy_document" "assume_role_tf" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

## Creating a IAM Policy Document for Cloud Watch Policy

data "aws_iam_policy_document" "cloud_watch_policy_tf" {

  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:us-east-2:${var.account_id}:*",
      "arn:aws:logs:us-east-2:${var.account_id}:log-group:/aws/lambda/ingest-source-raw-data-tf:*"
    ]
  }
}

## Creating a IAM Policy Document for S3 Policy

data "aws_iam_policy_document" "s3_policy_tf" {
  statement {
    effect = "Allow"

    actions = [
      "s3:*",
      "s3-object-lambda:*",
    ]

    resources = ["*"]
  }
}

# Creating a role for lambda function and attaching the assume role

resource "aws_iam_role" "iam_role_lambda_tf" {
  name               = "yash-ingest-sourcedata-rawdata-role-tf"
  assume_role_policy = data.aws_iam_policy_document.assume_role_tf.json

}

# Creating a role for S3 and attaching the S3 policy

resource "aws_iam_policy" "aws_s3_policy_tf" {
  name   = "s3_policy"
  policy = data.aws_iam_policy_document.s3_policy_tf.json

}

# Creating a role for Cloud Watch and attaching the cloud watch policy

resource "aws_iam_role_policy" "cloud_watch_role_policy_tf" {
  name   = "cloud_watch_policy"
  policy = data.aws_iam_policy_document.cloud_watch_policy_tf.json
  role   = aws_iam_role.iam_role_lambda_tf.name
}

resource "aws_iam_role_policy_attachment" "aws_s3_policy_attachment_tf" {
  role       = aws_iam_role.iam_role_lambda_tf.name
  policy_arn = aws_iam_policy.aws_s3_policy_tf.arn
} 
