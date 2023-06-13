### FOR STEP FUNCTION ##
resource "aws_sfn_state_machine" "yash-state-machine-tf" {
  name     = "yash-state-machine-tf"
  role_arn = aws_iam_role.state_machine_role.arn

  definition = <<EOF
{
  "Comment": "A description of my state machine",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:us-east-2:862370907407:function:ingest-source-raw-data-tf:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 2,
          "MaxAttempts": 6,
          "BackoffRate": 2
        }
      ],
      "End": true
    }
  }
}
EOF
}

resource "aws_iam_role" "state_machine_role" {
  name = "state_machine_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}




data "aws_iam_policy_document" "event_bridge_policy" {

  statement {
    effect = "Allow"

    actions = [
      "states:StartExecution"
    ]

    resources = [
      "arn:aws:states:us-east-2:862370907407:stateMachine:yash-state-machine-tf"
    ]
  }
}

data "aws_iam_policy_document" "assume_role_eb" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eb_role"{
  name ="eb_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_eb.json
}

resource "aws_iam_role_policy" "eb_role_policy" {
  name   = "eb_role_policy"
  policy = data.aws_iam_policy_document.event_bridge_policy.json
  role   = aws_iam_role.eb_role.name
}

resource "aws_iam_role_policy" "lambda-execution" {
  name = "lambda-execution"
  role = aws_iam_role.state_machine_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "lambda:*",
        "states:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

