import boto3
from django.conf import settings



def generate_s3_presigned_url(object_key, expiration=600):
    """
    Generates a presigned URL for an S3 object.

    Args:
        object_key (str): The key (path) of the object in the S3 bucket.
        expiration (int): The duration in seconds for which the presigned URL is valid.
                          Defaults to 3600 seconds (1 hour).

    Returns:
        str: The presigned URL, or None if an error occurs.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME # Ensure this is defined in your settings.py
    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None