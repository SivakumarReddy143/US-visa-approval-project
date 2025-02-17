import boto3
import os
from dotenv import load_dotenv
from us_visa.constant import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_KEY_ID_ENV_KEY,REGION_NAME
load_dotenv()

class S3Client:
    s3_client=None
    s3_resource = None
    def __init__(self,region_name=REGION_NAME):
        if S3Client.s3_client==None or S3Client.s3_resource == None:
            __access_key_id= os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            __secret_access_key = os.getenv(AWS_SECRET_KEY_ID_ENV_KEY)
            
            if __access_key_id is None:
                raise Exception(f"Environmental variable for {AWS_ACCESS_KEY_ID_ENV_KEY} is not set")
            
            if __secret_access_key is None:
                raise Exception(f"Environment variable for {AWS_SECRET_KEY_ID_ENV_KEY} is not set")
            
            S3Client.s3_resource=boto3.resource('s3',
                                                aws_access_key_id=__access_key_id,
                                                aws_secret_access_key=__secret_access_key,
                                                region_name=region_name
                                                )
            S3Client.s3_client = boto3.client('s3',
                                              aws_access_key_id=__access_key_id,
                                              aws_secret_access_key=__secret_access_key,
                                              region_name=region_name
                                              )
        self.resource=S3Client.s3_resource
        self.client=S3Client.s3_client