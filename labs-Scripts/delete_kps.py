# from attr import Attribute
from botocore.exceptions import ClientError
import boto3
from pprint import pprint

available_regions = [
    "us-east-2",
    # "us-east-1"
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

    key_pairs = EC2_RESOURCE.key_pairs.all()
    kps = []

    print("*****************************")
    print(f"region:  **** {region} ****")
    print("*****************************")

    for kp in key_pairs:
        # pprint(kp)
        if (key_pair_info in kp.key_name):
            kps.append(kp.key_name)
    
    for k in kps:
        try:
            key_pair = EC2_RESOURCE.KeyPair(k)
            key_pair.delete()
            print(f'SSH key "{k}" successfully deleted')
        except ClientError as e:
            pprint(e)
            print(" Not Able to delete Key Pairs :( ")
            continue