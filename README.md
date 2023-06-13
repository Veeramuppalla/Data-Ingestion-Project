# Data-Ingestion-Project
This project contains the functionality of processing the source data and transforming into desired format and loading into target database using AWS Cloud Services like Lambda, S3, Event Bridge etc.,

Steps to Execute the Project:
---------------------------------------------------------------------------
Step 1:
---------------------------------------------------------------------------
Files in the repository:
src\ingestion_lambda_function_raw\lambda.py
This python file contains the code that is designed to run in an AWS Lambda function.

The code imports necessary packages, including json, boto3 (the AWS SDK for Python), logging, and os. It also imports the datetime module for working with dates and times.

The current date is obtained using datetime.now() and is stored in the variables year, month, and day.

The codelambdabucket variable is set to the value of an environment variable named "codebucket".

The code configures logging using the logging.basicConfig() function, setting the log level to INFO and specifying the log format.

An s3_client and s3_resource object are created using the boto3.client() and boto3.resource() methods, respectively, to interact with Amazon S3.

An sns_client object is created to interact with Amazon SNS (Simple Notification Service).

The sending_email() function is defined, which takes a subject and message as input and publishes an SNS message with the specified subject and message to a pre-configured SNS topic.

The lambda_handler() function is defined, which serves as the entry point for the AWS Lambda function. It takes the event and context parameters.

The function begins by fetching a JSON configuration file named "source_system/config.json" from an S3 bucket. The bucket name is obtained from the codelambdabucket variable. The contents of the file are loaded into the config variable.

The relevant configuration values are extracted from the config dictionary, including the source and target S3 bucket names.

The code lists the objects (files) in the source S3 bucket using s3_client.list_objects_v2(). The response is then iterated over, and the keys (object names) are extracted and stored in the file_name_list list.

The script then processes each file in the file_name_list starting from the second element (index 1). It splits the file name into parts using filename_parts = a.split(".").

A new target S3 key is constructed using the current date and the extracted parts of the filename. This key follows a specific naming convention with the year, month, and day subfolders.

The script attempts to copy the source file to the target S3 bucket using bucket.copy(), passing the copy_source and new_name variables. If the copy operation is successful, it prints a success message and sends an email using the sending_email() function. If an exception occurs during the copy operation, it prints a failure message and sends an email.

File name : s3.tf

This file uses the aws_s3_bucket resource and creates 3 different s3 buckets.
source_bucket - This bucket is the source of the data files.
raw_bucket - This bucket is created for fetching and storing the data for further processing.
config_bucket - This bucket is used to store the configuration fies.

Using the aws_s3_object resource, the config files from the local folders are pushed to the buckets created.

File name : providers.tf

This file contains the details of the provider - AWS
The value for region is stored in the variables.tf file.

File name : sns.tf

This File contains the details of the Simple Notification Service from the Amazon.
This is used to send email notifications when the process has completed.
Resources used in this file are defined below.
aws_sns_topic - This resource is used to create a topic for the SNS service.
aws_sns_topic_subscription - This resource is used to create a topic subscription.
It has the variable email_id which is the receivers email id, fetched from variables.tf
aws_iam_policy_document - This is a AWS policy document which is required to allow the resources for all SNS Actions.
aws_iam_role_policy - This is a AWS policy created for the SNS and the policy document defined above is attached to the role created for executed for lambda as the email has to be triggered from the lambda function.

File name : step_function.tf

File name : lambda.tf

File name : lambda_role.tf

File name : variables.tf

File name : developer.tfvars

