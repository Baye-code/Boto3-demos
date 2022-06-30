from pprint import pprint
import boto3
from botocore.exceptions import ClientError

lab_regions = [
    "us-east-1",
    "us-east-2",
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
    # "ap-southeast-2",
    "sa-east-1"
]


for region in lab_regions:

    ec2client = boto3.client('ec2',region_name=region)
    response = ec2client.describe_instances()

    instance_ids = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if (instance['State']['Name'] == 'running'):
                instance_id = (instance["InstanceId"])
                print("*"*50)
                pprint(instance_id)
                print("*"*50)
                print()
                instance_ids.append(instance_id)
                # ec2_resource.stop_instances(InstanceIds=[instance_id])

    for instance_id in instance_ids:
        # Do a dryrun first to verify permissions
        try:
            ec2client.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            pprint(f"Server: {response['ResponseMetadata']['HTTPHeaders']['server']}")
            pprint(f"HTTPStatusCode: {response['ResponseMetadata']['HTTPStatusCode']}")
            pprint(f"StoppingInstances: {response['StoppingInstances']}")
            print("-"*70)
            print("-"*70)
        except ClientError as e:
            pprint(e)

