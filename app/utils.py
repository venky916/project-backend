import environ
import boto3
from botocore.exceptions import NoCredentialsError

# Load environment variables from .env
environ.Env.read_env()

# Create an Env instance
env = environ.Env()


# AWS S3 Configuration
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')


def upload_to_s3(foldername,file):
    s3 = boto3.client("s3",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_S3_REGION_NAME)
    
# Define the upload path in the S3 bucket
    upload_path = f'{foldername}/{file.name}'

    try:
        # Upload the file to S3
        s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, upload_path)

        # Generate the S3 URL
        s3_url = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{upload_path}'

        return s3_url
    
    except NoCredentialsError:
        return None
    


        
