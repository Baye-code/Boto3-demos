import boto3

s3_resource = boto3.resource("s3")
bucket = s3_resource.create_bucket(
        Bucket="my_first_bucket", 
        CreateBucketConfiguration=
        {
        'LocationConstraint': 'us-east-2'})
print(bucket)

with open('~/test_file.txt', 'rb') as uploaded_data:
    bucket.put_object(Body=uploaded_data)
