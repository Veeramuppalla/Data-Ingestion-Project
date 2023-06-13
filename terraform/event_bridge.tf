###  FOR CREATING EVENT BRIDGE

resource "aws_cloudwatch_event_rule" "event_bridge_rule" {
  name        = "step-function-invocation-rule"
  description = "Rule to Invoke Step Function"
  schedule_expression = "rate(5 minutes)"  # Schedule to run every 30 minutes
}

resource "aws_cloudwatch_event_target" "event_bridge_target" {
  rule      = aws_cloudwatch_event_rule.event_bridge_rule.name
  arn       = aws_sfn_state_machine.yash-state-machine-tf.arn
  role_arn  = aws_iam_role.eb_role.arn
  input     = "{\"dataset\":\"movielens\"}"
  
}

resource "aws_cloudwatch_event_rule" "event_bridge_rule-new" {
  name        = "step-function-invocation-rule-new"
  description = "Rule to Invoke Step Function"
  schedule_expression = "rate(5 minutes)"  # Schedule to run every 30 minutes
}

resource "aws_cloudwatch_event_target" "event_bridge_target-new" {
  rule      = aws_cloudwatch_event_rule.event_bridge_rule-new.name
  arn       = aws_sfn_state_machine.yash-state-machine-tf.arn
  role_arn  = aws_iam_role.eb_role.arn
  input     = "{\"dataset\":\"movielens\"}"
  
}