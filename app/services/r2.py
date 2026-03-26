import boto3
import os

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
    region_name="auto",
)

BUCKET = os.getenv("R2_BUCKET")


def upload_file(file_obj, filename, content_type):
    s3.upload_fileobj(
        file_obj,
        BUCKET,
        filename,
        ExtraArgs={"ContentType": content_type}
    )

    return f"{os.getenv('R2_ENDPOINT')}/{BUCKET}/{filename}"