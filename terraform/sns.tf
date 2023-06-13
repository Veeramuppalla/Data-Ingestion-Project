data "aws_iam_policy_document" "sns_topic_policy_tf" {
  
  statement {
    effect = "Allow"

    actions = [
      "SNS:*",
    
    ]
    resources = ["*"]
  }
}


resource "aws_sns_topic" "creating_topic_tf" {
  name = "yash-data-ingestion-pipeline"
} 

resource "aws_iam_role_policy" "sns_topic_policy_tf" {
  name = "sns_topic_policy"
  policy = data.aws_iam_policy_document.sns_topic_policy_tf.json
  role   = aws_iam_role.iam_role_lambda_tf.name
} 

resource "aws_sns_topic_subscription" "user_updates_sns_target" {
  topic_arn = aws_sns_topic.creating_topic_tf.arn
  protocol  = "email-json"
  #endpoint  = "yashjkz855@gmail.com"
  endpoint = var.email_id
}