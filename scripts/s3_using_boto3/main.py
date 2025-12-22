import boto3
import os
import argparse
from datetime import datetime, timezone, timedelta


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

#function to list objects in a bucket
def list_bucket_objects(bucket):

        resp = s3.list_objects_v2(Bucket=bucket)
        #count = sum(1 for _ in bucket.objects.all())           #Not really needed. Could cost for the number of calls if there are many objects
        if 'Contents' in resp:
                for obj in resp.get('Contents', []"):
                        print(f"Key: {obj["Key"]}\n")
        else:
                print(f"[ERROR] Specified bucket is empty!!!\n")
                return

#function to download a file from s3
def download_file(bucket, key):
        s3.download_file(bucket, key, key)
        print(f"{key} Downloaded from Bucket {bucket}\n")

#function to delete old files
def s3_cleanup(bucket, days):
        cutoff = datetime.now(timezone.utc) - timedelta(days=days) #AWS stores S3 modifications in UTC
        resp = s3.list_objects_v2(Bucket=bucket)
        for obj in resp.get('Contents',[]):
                if obj["LastModified"] < cutoff:
                        s3.delete_object(Bucket=bucket, Key=obj['Key'])
                        print(f"Deleted object {obj['Key']} from Bucket {bucket}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--bucket", help="Bucket name")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--file", help="File to be uploaded")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--key", help="oject key to be downloaded from s3 bucket")
    parser.add_argument("--days", type=int)
    parser.add_argument("--cleanup", action="store_true")

    args = parser.parse_args()

    if args.upload:
         upload_file(args.bucket, args.file)
    elif args.list:
         list_bucket_objects(args.bucket)
    elif args.download:
         download_file(args.bucket, args.key)
    elif args.cleanup:
         s3_cleanup(args.bucket, args.days)