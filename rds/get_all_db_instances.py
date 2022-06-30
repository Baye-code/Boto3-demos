import boto3
from pprint import pprint

available_regions = [
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

for region in available_regions:
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()
    if (response['DBInstances']):
        print("*"*100)
        pprint(response['DBInstances'])
        print("*"*100)
    else:
        print(f"no database available in the {region}")


# response = client.stop_db_instance(
#     DBInstanceIdentifier='database-instance-01',
#     DBSnapshotIdentifier='stop-snapshot001'
# )


# for region in available_regions:
#     rds = boto3.client('rds', region_name=region)
#     for dbinstance in rds.describe_db_instances():
#         print("{DBInstanceClass}".format(**dbinstance))