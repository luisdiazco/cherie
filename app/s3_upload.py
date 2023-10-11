import boto3
from uuid import uuid4
import app.key_config as keys
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer
import logging


def upload_to_s3(file, bucket_name, username, product_id):
    s3 = boto3.client('s3',
                      aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY)

    # Construct the path for the image in the S3 bucket
    file_path = f"cherie-products/{username}/{product_id}/{file.filename}"

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_path,
            ExtraArgs={
                "ACL": "private-read",
                "ContentType": file.content_type
            }
        )
    except ClientError as e:
        logging.error(e)
        return None

    return {"url": f"https://{bucket_name}.s3.amazonaws.com/{file_path}", "product_id": product_id}
