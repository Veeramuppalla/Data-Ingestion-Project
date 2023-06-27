## IMPORTING PACKAGES
import json
import boto3
import logging
import os
from datetime import datetime
from aws_lambda_powertools import Logger
import uuid



current_date = datetime.now()
year = current_date.year
month = current_date.month
day = current_date.day
hour = current_date.hour
codelambdabucket = os.environ['codebucket']

date_string = current_date.strftime("%Y-%m-%d %H:%M:%S") # for db insert converting to string

##############################  FOR LOGGING ################################

log = Logger(service="ingest_raw")
#log.info("Starting AWS powertool")

######################## For Sending Email #########################

def sending_email(subject,message):
    response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-2:862370907407:data-pipeline-notification',
        Message=message,
        Subject=subject,
    )

## FUNCTION FOR DYNAMO DB INSERT ##

def insert_to_audit_table(item):
    table.put_item(Item=item)
    
## FUNCTION FOR UPDATE TABLE

def update_audit_attribute(table, item_key, attribute_name, new_attribute_value):
    response = dynamodb_client.update_item(
        TableName=table,
        Key=item_key,
        UpdateExpression=f'SET {attribute_name} = :value',
        ExpressionAttributeValues={':value': {'S': new_attribute_value}}
    )
    
###################### Creating s3 and sns objects ############

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
sns_client = boto3.client('sns')

## DEFINING FOR DYNAMO DB ##

dynamodb = boto3.resource('dynamodb')
table_name = 'data-ingestion-audit-tf'
table = dynamodb.Table(table_name)

    
### FUNCTION FOR CHECKING TABLE EXISTS OR NOT ##
dynamodb_client = boto3.client('dynamodb')

def check_table_exists(table_name):
    waiter = dynamodb_client.get_waiter('table_exists')
    try:
        output=  waiter.wait(TableName=table_name)  
           
    except Exception as e:
        print(e)
       # sending_email("Dynamo DB Table Not Found","Dynamo DB Table Not Found")


###################### Function to send an email with SNS ########

def file_copy(source_bucket_name, source_folder, target_bucket_name, file_name, new_name):
    copy_source = {
        'Bucket': source_bucket_name,
        'Key': f"{source_folder}/{file_name}"
    }
    bucket = s3_resource.Bucket(target_bucket_name)
    bucket.copy(copy_source, new_name)
    
######################## Code for Lambda #######################

def lambda_handler(event, context):

    dataset = "movielens"
    
    response = s3_client.get_object(Bucket=codelambdabucket, Key=f"{dataset}/config/ingest_config.json")
    config_data = response['Body'].read().decode('utf-8')
    config = json.loads(config_data)
    pipeline = config['pipeline']
    
    print(event)
    log.info(event)
    
    print(context)
    log.info(context)
    
   
    step_function_arn = context.invoked_function_arn
    step_function_arn_parts = step_function_arn.split(':')
    acquisition = ':'.join(step_function_arn_parts[:5])
    
    for asset in pipeline:
        data_asset = asset['data_asset']
        
        raw_config = asset['raw']
        source_bucket = raw_config['source_bucket']
        source_folder = raw_config['source_folder']
        target_bucket = raw_config['target_bucket']
        partition = raw_config['partition']
        file_pattern = raw_config['file_pattern']
        file_name_from_pattern = file_pattern + '.csv'
        
        PK = dataset + "|" + data_asset + "|"+ context.function_name
        SK = str(uuid.uuid4())
        
        item = {
                    'PK': PK,
                    'SK': SK,
                    'process_name': 'test',
                    'function_name': context.function_name,
                    'acquisition': acquisition,
                    'file_name': 'test',
                    'date_time': date_string,
                    'process_time': 'test',
                    'status_code': 'IN PROGRESS',
                    'log_stream_name': context.log_stream_name,
                    'log_group_name': context.log_group_name,
                    'error_message': 'test'
                }
        
        
        check_table_exists(table_name)
        insert_to_audit_table(item)
        
       # table_name = 'data-ingestion-audit-tf'
        item_key = {'PK': {'S': PK}, 'SK': {'S': SK}}
        update_audit_attribute(table_name,item_key,'file_name',file_name_from_pattern) 
 
        response = s3_client.list_objects(Bucket=source_bucket, Prefix=source_folder)
        objects = response['Contents']
        
        file_name_list = []
        for obj in response['Contents']:
            file_name = obj['Key']
            file_name = file_name.replace(source_folder + '/', '')
            file_name_list.append(file_name)
        
        for a in file_name_list:
            filename_parts = a.split(".")
            if filename_parts[0] == file_pattern:
    
                if partition == "HOUR":
                    new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/day={day}/hour={hour}/{filename_parts[0]}_{year}_{month}_{day}_{hour}.{filename_parts[1]}"
                elif partition == "DAY":
                    new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/day={day}/{filename_parts[0]}_{year}_{month}_{day}.{filename_parts[1]}"
                elif partition == "YEAR":
                    new_name = f"{source_folder}/{filename_parts[0]}/year={year}/{filename_parts[0]}_{year}.{filename_parts[1]}"
                elif partition == "MONTH":
                    new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/{filename_parts[0]}_{year}_{month}.{filename_parts[1]}"

                try:
                    start_time = datetime.now()
                    file_copy(source_bucket, source_folder, target_bucket, a, new_name)
                    end_time = datetime.now()
                    status_code="PASS"
                    update_audit_attribute(table_name,item_key,'status_code',status_code) 
                   # sending_email("Copy Success", "From Source to Destination")
                    
                except Exception as e:
                    status_code="FAIL"
                    update_audit_attribute(table_name,item_key,'status_code',status_code) 
                   # sending_email("Copy Failed", "From Source to Destination")
                    print(e)
                
                processing_time = end_time - start_time
                update_audit_attribute(table_name,item_key,'process_time',str(processing_time)) 