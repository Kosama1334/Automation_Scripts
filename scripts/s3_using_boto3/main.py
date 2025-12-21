import boto3
import os
import argparse


s3 = boto3.client("s3")

#function to upload file to s3
def upload_file(bucket, file_path):

    if os.path.exists(file_path):
        key = os.path.basename(file_path)

        s3.upload_file(file_path, bucket, key)
        print(f"file {key} uploaded to bucket {bucket}!\n#####OK#####\n")

        return

    else:
        print(f"[ERROR] File not found!\n Please Check the path specified\n#####ERROR#####\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--bucket", help="Bucket name")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--file", help="File to be uploaded")

    agrs = parser.parse_args()

    if args.upload:
        upload_file(args.bucket, args.file)