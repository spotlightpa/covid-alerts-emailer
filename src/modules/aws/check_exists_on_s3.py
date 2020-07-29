import logging
import boto3
import os
import botocore


def check_exists_on_s3(bucket_name: str, path: str,) -> bool:
    """
    Checks where a file already exists at a specific path of an S3 bucket.

    Note: Requires AWS credentials to be provided in a .env file stored in root project directory under AWS_KEY_ID
    and AWS_SECRET_KEY_ID or credentials must be stored at ~/.aws/credentials like so:

        [default]
            aws_access_key_id=AKIAIOSFODNN7EXAMPLE
            aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    Args:
        bucket_name (str): Name of bucket where files should be copied to.
        path (str): path of file stored in S3 bucket.

    Returns:
        bool: True if file exists, false if it doesn't
    """

    # GET ENV VARS
    keyID = os.environ.get("AWS_KEY_ID")
    sKeyID = os.environ.get("AWS_SECRET_KEY_ID")

    # CONNECT TO S3
    session = boto3.Session(aws_access_key_id=keyID, aws_secret_access_key=sKeyID,)
    s3 = session.resource("s3")

    try:
        s3.Object(bucket_name, path).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logging.info(f"Path {path} does not exist on {bucket_name}")
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        # The object does exist.
        logging.info(f"Path {path} exists on {bucket_name}")
        return True
