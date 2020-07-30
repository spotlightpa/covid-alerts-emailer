import logging
import boto3
import os
from definitions import DIR_OUTPUT
from pathlib import Path


def copy_to_s3(
    local_file_path: Path,
    bucket_name: str,
    destination_dir: str,
    content_type: str = "text/csv",
) -> None:
    """
    Uploads a local file to an S3 bucket.

    Note: Requires AWS credentials to be provided in a .env file stored in root project directory under AWS_KEY_ID
    and AWS_SECRET_KEY_ID or credentials must be stored at ~/.aws/credentials like so:

        [default]
            aws_access_key_id=AKIAIOSFODNN7EXAMPLE
            aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    Args:
        local_file_path (Path): File path for file to be transferred.
        bucket_name (str): Name of bucket where files should be copied to.
        destination_dir (str): Directory of where files should be copied to inside bucket.
        content_type (str) OPTION: http header info about the contents of the file. Defaults to "text/csv"

    Returns:
        None
    """
    filename = local_file_path.name
    logging.info(f"Move {filename} to s3")

    try:
        # CHECK FILE EXISTS
        if not local_file_path.is_file():
            logging.error(
                f"No file found at {local_file_path},"
                "aborting attempt to move file to S3."
            )
            raise

        # GET ENV VARS
        keyID = os.environ.get("AWS_KEY_ID")
        sKeyID = os.environ.get("AWS_SECRET_KEY_ID")
        source_path = str(local_file_path.resolve())
        destination_path = f"{destination_dir}/{filename}"

        # LOGGING
        logging.info(f"Moving {source_path} to S3 bucket {bucket_name}...")
        logging.info(f"File will be saved in: {destination_path}")

        # CONNECT TO S3
        session = boto3.Session(aws_access_key_id=keyID, aws_secret_access_key=sKeyID,)
        s3 = session.resource("s3")

        # UPLOAD
        s3.Bucket(bucket_name).upload_file(
            source_path,
            destination_path,
            ExtraArgs={
                "ACL": "public-read",
                "CacheControl": "proxy-revalidate, max-age=300",
                "ContentType": content_type,
            },
        )

        logging.info(f"file uploaded to {destination_path}")
        logging.info(f"Full URL: https://{bucket_name}/{destination_path}")
    except Exception as e:
        logging.error(
            "Something went wrong when attempting to copy file" " to S3 bucket"
        )
        logging.exception(e)
        return
