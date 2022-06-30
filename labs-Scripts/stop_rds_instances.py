import boto3
from pprint import pprint

available_regions = [
    # "us-east-1",
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

for region in available_regions:

    rds_db_itentifiers = []
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()
    if (response['DBInstances']):
        for res in response['DBInstances']:
            print("*"*70)
            db_identifier = res['DBInstanceIdentifier']
            pprint(db_identifier)
            print("*"*70)
            if (res['DBInstanceStatus'] == 'available'):
                rds_db_itentifiers.append(db_identifier)
    else:
        print(f"no database available in the {region}")

    
    for db_id in rds_db_itentifiers:

        client.stop_db_instance(
            DBInstanceIdentifier=db_id
        )

        print(f" Stopping DB with Identifier -> {db_id}")
        print("-"*70)
        print("-"*70)
