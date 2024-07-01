import os
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv('DB')
CognitoClientId = os.getenv('CognitoClientId')
CognitoRegionName = os.getenv('CognitoRegionName')
UserPoolID = os.getenv('UserPoolID')
S3Bucket = os.getenv('S3Bucket')
AWSAccessKeyId = os.getenv('AWSAccessKeyId')
AWSSecretKeyID = os.getenv('AWSSecretKeyID')