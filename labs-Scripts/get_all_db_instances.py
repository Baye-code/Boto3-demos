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

def group_create():
    groups = []
    for i in range(1, 16):
        group_name = "group"+str(i)
        groups.append(group_name)
    return groups

lab_groups = group_create()

i = 0

for region in available_regions:
    
    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()

    # pprint(response)
    # pprint(f"Region : ** {region} ** ")

    db_instances = list()

    if (response['DBInstances']):
        for res in response['DBInstances']:

            db_details = list()

            # if (response['DBInstances']):
            print("*"*100)
            pprint(f"Database {res['DBInstanceIdentifier']} Created at {res['InstanceCreateTime']}")
            print("*"*100)
            db_details.append(res['DBInstanceIdentifier'])
            db_details.append(res['InstanceCreateTime'])
            db_instances.append(db_details)
            print()
    else:
        print(f"no database available in the {region}")

    print("="*30)
    print(f"*** Region: {region} *** ")
    print("="*30)

    # pprint(db_instances)
    
    for db_detail in db_instances:
        pprint(f"Instance de {db_detail[0]}:  Created at --> {db_detail[1]} .")
    print()

    with open(lab_groups[i]+'-RDS-Lab.txt', 'w', encoding = 'utf-8') as f:
        f.write(f"{region}\n")
        f.write("================\n")
        for db_detail in db_instances:
            f.write(f"Database Instance {db_detail[0]} Created at --> {db_detail[1]}."+"\n")

    i+=1
    

# response = client.stop_db_instance(
#     DBInstanceIdentifier='database-instance-01',
#     DBSnapshotIdentifier='stop-snapshot001'
# )


# for region in available_regions:
#     rds = boto3.client('rds', region_name=region)
#     for dbinstance in rds.describe_db_instances():
#         print("{DBInstanceClass}".format(**dbinstance))

