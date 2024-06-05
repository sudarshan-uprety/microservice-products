import os
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv('DB')
CognitoClientId = os.getenv('CognitoClientId')
CognitoRegionName = os.getenv('CognitoRegionName')
