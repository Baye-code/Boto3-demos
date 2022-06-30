from attr import Attribute
import boto3
from pprint import pprint
from botocore.exceptions import ClientError

available_regions = [
    # "us-east-1",
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
    "ap-southeast-2",
    "sa-east-1"
]

print("----------------------------")

for region in available_regions:

    rds_db_itentifiers = []
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()        

    if (response['DBInstances']):
        for res in response['DBInstances']:
            # print("*"*70)
            db_identifier = res['DBInstanceIdentifier']
            # pprint(db_identifier)
            # print("*"*70)
            if (res['DBInstanceStatus'] != 'available' or res['DBInstanceStatus'] == 'available'):
                rds_db_itentifiers.append(db_identifier)
    else:
        print(f"no database available in the {region}")

    
    print(f"region:  **** {region} ----")
    print("****************************")
    
    for db_id in rds_db_itentifiers:

        # Stop Db Instance first
        # client.stop_db_instance(
        #     DBInstanceIdentifier=db_id
        # )

        try:
            # Modify Db Instance
            client.modify_db_instance(
                DBInstanceIdentifier=db_id,
                DeletionProtection=False
            )

            # Delete Database Instance
            client.delete_db_instance(
                DBInstanceIdentifier=db_id,
                SkipFinalSnapshot=True,
            )
        except ClientError as e:
            pprint(e)
            continue

        # waiter = client.get_waiter('db_instance_deleted')
        # waiter.wait(
        #     DBInstanceIdentifier=db_id,
        #     WaiterConfig={
        #     # 'Delay': 180,
        #     'MaxAttempts': 2
        #     }  
        # )

        print(f" Deleting DB with Identifier -> {db_id}")
        print("-"*70)
        # print("-"*70)
