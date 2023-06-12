## IMPORTING PACKAGES
import json
import boto3
import logging
import os
from datetime import datetime

current_date = datetime.now()
year = current_date.year
month = current_date.month
day = current_date.day
codelambdabucket = os.environ['codebucket']

######################## For Logging #########################

logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(lineno)s %(levelname)s %(message)s"
)

log = logging.getLogger("Ingest-Raw")
log.setLevel(logging.INFO)


###################### Creating s3 and sns objects ############

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
sns_client = boto3.client('sns')

###################### Function to send an email with SNS ########

def sending_email(subject,message):
    response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-2:862370907407:data-pipeline-notification',
        Message=message,
        Subject=subject,
    )

######################## Code for Lambda #######################

def lambda_handler(event, context):
    dataset='source_system/config.json'
      
    # Fecthing Date from the config.json
    response = s3_client.get_object(Bucket=codelambdabucket, Key=dataset)
    config_data = response['Body'].read().decode('utf-8')
    config = json.loads(config_data)
    lambda_config = config['lambda_config'][0]
    s3_bucket_name = lambda_config['s3_bucket_name']
    source_folder = lambda_config['source_folder']
    target_bucket_name = lambda_config['target_bucket_name']
    
    print(s3_bucket_name)

    response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
    
    file_name_list = []

    for obj in response['Contents']:
        file_name = obj['Key']
        file_name = file_name.replace(source_folder + '/', '')
        file_name_list.append(file_name)
        
    print(file_name_list)
        
    for a in file_name_list[1:]:
        filename_parts = a.split(".")
        #print(filename_parts)
    
        new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/day={day}/{filename_parts[0]}_{current_date}.{filename_parts[1]}"
        try:
            copy_source = {
                    'Bucket': s3_bucket_name,
                    'Key': f"{source_folder}/{a}"
                }
            bucket = s3_resource.Bucket(target_bucket_name)
            bucket.copy(copy_source, new_name)
            print("Copy SuccessFull")
            sending_email("Copy Sucess" ," Copy Success from Source to Destination ")
        except Exception as e:
            print("Copy Failed")
            sending_email("Copy Failed", "Copy Failed from Source to Destination")

    