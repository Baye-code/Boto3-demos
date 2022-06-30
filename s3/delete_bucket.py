import boto3

s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket("my_first_bucket")
bucket.objects.all().delete()
bucket.delete()