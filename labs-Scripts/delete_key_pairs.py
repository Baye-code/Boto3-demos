# from attr import Attribute
from botocore.exceptions import ClientError
import boto3
from pprint import pprint

available_regions = [
    # "us-east-2",
    "us-west-1",
    "us-west-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "eu-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-southeast-1",
    "ap-southeast-2",
    "sa-east-1"
]

key_pair_info = "saraya"

for region in available_regions:

    EC2_RESOURCE = boto3.resource('ec2', region_name=region)
    ec2client = boto3.client('ec2',region_name=region)
    response = ec2client.describe_instances()

    key_pairs = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            try:
                # if(instance['KeyName']):
                key_name = instance['KeyName']
                key_pairs.append(str(key_name))
            except ClientError as e:
                pprint(e)
                continue

    print("*****************************")
    print(f"region:  **** {region} ****")
    print("*****************************")

    for kp in key_pairs:
        if (key_pair_info in kp):
            try:
                key_pair = EC2_RESOURCE.KeyPair(kp)
                key_pair.delete()
                print(f'SSH key "{kp}" successfully deleted')
            except ClientError as e:
                pprint(e)
                continue