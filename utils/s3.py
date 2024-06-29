import uuid

import urllib.parse

from utils import helpers
from utils import variables


def upload_image(image):
    file_name = str(uuid.uuid4()) + '.jpg'
    key = f"uploads/product/image/{file_name}"
    s3_client = helpers.boto3_s3_client()
    s3_client.put_object(
        Body=image,
        Bucket=variables.S3Bucket,
        Key=key,
        ContentType='image/jpeg'
    )
    url = f"https://{variables.S3Bucket}.s3.amazonaws.com/{key}"
    return url


def delete_image(image):
    # Parse the URL to get the path
    parsed_url = urllib.parse.urlparse(image)

    # The key is the path without the leading '/'
    key = parsed_url.path.lstrip('/')

    s3_client = helpers.boto3_s3_client()
    try:
        # First, check if the object exists
        s3_client.head_object(Bucket=variables.S3Bucket, Key=key)

        # If it exists, delete it
        response = s3_client.delete_object(
            Bucket=variables.S3Bucket,
            Key=key
        )

        # Check if deleted was successful
        if response['ResponseMetadata']['HTTPStatusCode'] == 204:
            return True
        else:
            return False

    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return True
        else:
            return False

    except Exception as e:
        return False
