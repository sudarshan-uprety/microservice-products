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
S3Expiration = os.getenv('S3Expiration')
LOKI_URL = os.getenv('LOKI_URL')
ENV = os.getenv('ENV')

# event names
DECREASE_PRODUCT_QUANTITY_EVENT = 'DECREASE_PRODUCT_QUANTITY_EVENT'
INCREASE_PRODUCT_QUANTITY_EVENT = 'INCREASE_PRODUCT_QUANTITY_EVENT'
