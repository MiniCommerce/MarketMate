from main.env import config
import boto3
import uuid
import datetime


class S3Client:
    def __init__(self):
        self.s3_client = boto3.client(
            service_name='s3',
            region_name=config('AWS_REGION', default=None),
            aws_access_key_id=config('AWS_ACCESS_KEY', default=None),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY', default=None),
        )
        self.bucket_name = config('BUCKET_NAME', default=None)
        self.region_name = config('AWS_REGION', default=None)
    
    def image_path(self):
        file_id = str(uuid.uuid4())
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        file_path = f'{date}/{file_id}'
        
        return file_path
    
    def s3_path(self):
        path = f'https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/'

        return path
    
    def upload(self, file):
        try:
            file_path = self.image_path()
            full_path = self.s3_path() + file_path
            self.s3_client.upload_fileobj(
                file, 
                self.bucket_name, 
                file_path, 
                ExtraArgs = {'ContentType': file.content_type}
                )
            
            return full_path
        except Exception as e:
            print(f"error:{e}")
            return ''

s3 = S3Client()