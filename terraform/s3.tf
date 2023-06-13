 
#resource "aws_s3_bucket" "source_bucket" {
#    bucket = "yash-movielens-source-bucket-tf"
#}

#resource "aws_s3_bucket" "raw_bucket" {
#    bucket = "yash-movielens-raw-bucket-tf"
    
#}

#resource "aws_s3_bucket" "config_bucket" {
#    bucket = "source-system-config"
#} 

#resource "aws_s3_object" "object" {
#    bucket = aws_s3_bucket.config_bucket.id
#    key = "source_system/config.json"
#    acl = "private"
#    source = "../src/config/config.json"
#    etag = filemd5("../src/config/config.json")
#}

#locals {
#  config_files = fileset("../data/movielens", "**/*")
#}

#resource "aws_s3_bucket_object" "upload_objects" {
#  for_each = local.config_files

 # bucket = aws_s3_bucket.source_bucket.id
  #key    = "movielens/${each.value}"
  #source = "../data/movielens/${each.value}"

  #etag = filemd5("../data/movielens/${each.value}")
#}