import boto3
from pprint import pprint

region = "us-east-1"

print(" ******** Deleting Amazon S3 Buckets: ******** ")

bucket_names = []

s3_resource = boto3.resource('s3',region_name=region)
iterator = s3_resource.buckets.all()

for bucket in iterator:
    # if str(bucket).startswith("saraya"):
    if "saraya" in str(bucket):
        print(f" ------ {bucket.name} ------ ")
        bucket_names.append(bucket)

print("*"*40)
    
for bk in bucket_names:
    # Deleting objects
    for s3_object in bk.objects.all():
        s3_object.delete()
    # Deleting objects versions if S3 versioning enabled
    for s3_object_ver in bk.object_versions.all():
        s3_object_ver.delete()

    print(f"S3 Bucket {bk} cleaned up")
    print(f"S3 Bucket {bk} deleted")
