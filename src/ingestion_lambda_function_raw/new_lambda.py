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
hour = current_date.hour
codelambdabucket = os.environ['codebucket']

######################## For Logging #########################

def sending_email(subject,message):
    response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-2:862370907407:data-pipeline-notification',
        Message=message,
        Subject=subject,
    )



###################### Creating s3 and sns objects ############

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
sns_client = boto3.client('sns')

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

    # Fecthing Date from the config.json
    response = s3_client.get_object(Bucket=codelambdabucket, Key=f"{dataset}/config/ingest_config.json")
    config_data = response['Body'].read().decode('utf-8')
    config = json.loads(config_data)
    source_bucket = config['pipeline'][0]['raw']['source_bucket']
    source_folder = config['pipeline'][0]['raw']['source_folder']
    target_bucket = config['pipeline'][0]['raw']['target_bucket']
    partition = config['pipeline'][0]['raw']['partition']
    file_pattern = config['pipeline'][0]['raw']['file_pattern']
    
    response = s3_client.list_objects(Bucket=source_bucket, Prefix=source_folder)
    objects = response['Contents']
    
    file_name_list = []
    for obj in response['Contents']:
        file_name = obj['Key']
        file_name = file_name.replace(source_folder + '/', '')
        file_name_list.append(file_name)

    
    for a in file_name_list[1:]:
        filename_parts = a.split(".")
       # print(a)
        print(filename_parts[0])
        if filename_parts[0] == file_pattern:
            if partition == "as":
                new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/day={day}/hour={hour}/{filename_parts[0]}_{year}_{month}_{day}_{hour}.{filename_parts[1]}"
                print(new_name)
                try:
                    file_copy(source_bucket,source_folder, target_bucket,a,new_name)
                    print("Success")
                    sending_email("Copy Success", " From Source to Destination")
                except Exception as e:
                    print("Copy Failed")
                    sending_email("Copy Failed", " From Source to Destination")
                    
            elif partition == "asDAY":
                new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/day={day}/{filename_parts[0]}_{year}_{month}_{day}.{filename_parts[1]}"
                print(new_name)
                try:
                    file_copy(source_bucket,source_folder, target_bucket,a,new_name)
                    print("Success")
                    sending_email("Copy Success", " From Source to Destination")
                except Exception as e:
                    print("Copy Failed")
                    sending_email("Copy Failed", " From Source to Destination")
                
            elif partition == "d":
                new_name = f"{source_folder}/{filename_parts[0]}/year={year}/{filename_parts[0]}_{year}.{filename_parts[1]}"
                print(new_name)
                try:
                    file_copy(source_bucket,source_folder, target_bucket,a,new_name)
                    print("Succesds")
                    sending_email("Copy Success", " From Source to Destination")
                except Exception as e:
                    print("Copy Failed")
                    sending_email("Copy Failed", " From Source to Destination")

            elif partition == "wds":
                new_name = f"{source_folder}/{filename_parts[0]}/year={year}/month={month}/{filename_parts[0]}_{year}_{month}.{filename_parts[1]}"
                print(new_name)
                try:
                    file_copy(source_bucket,source_folder, target_bucket,a,new_name)
                    print("Success")
                    sending_email("Copy Success", " From Source to Destination")
                except Exception as e:
                    print("Copy Failed")
                    sending_email("Copy Failed", " From Source to Destination")
        else:
            print("Filename and Pattern Does Not Match")
            sending_email("File Name Mismatch ", " Pleas check the configuration file")
        
    
  
        
   
    