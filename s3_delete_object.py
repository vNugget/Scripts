import boto3

s3_client = boto3.client('s3')

def delete_file(bucket_name, file_name):
    obj = s3_client.delete_object(Bucket=bucket_name, Key=file_name)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']
        print("Filename {} was added to bucket {}".format(file_name,bucket))
        if file_name.split(".")[-1] == "exe":
            delete_file(bucket,file_name)
            print("Deleting file {}".format(file_name))
