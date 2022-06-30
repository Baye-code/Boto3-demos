from pprint import pprint
import re
import boto3
from botocore.exceptions import ClientError

region = "us-east-1"

# def group_create():
#     groups = []
#     for i in range(1, 16):
#         group_name = "group"+str(i)
#         groups.append(group_name)
#     return groups

# lab_groups = group_create()

print(" ******** Listing Amazon S3 Buckets: ******** ")

bucket_names = []

s3_resource = boto3.resource('s3',region_name=region)
iterator = s3_resource.buckets.all()

for bucket in iterator:
    # if str(bucket).startswith("saraya"):
    if "saraya" in str(bucket):
        print(f" ------ {bucket.name} ------ ")
        bucket_names.append(bucket)

print("*"*40)

with open('Check-S3-Lab.txt','w',encoding = 'utf-8') as f:
    f.write("================\n")
    f.write("Available buckets \n")
    f.write("================\n")
    f.write("\n")
    for bucket_name in bucket_names:
        f.write(f"{str(bucket_name)}\n")





   
