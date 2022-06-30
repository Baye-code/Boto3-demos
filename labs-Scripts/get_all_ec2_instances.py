from pprint import pprint
import re
import boto3
from botocore.exceptions import ClientError

lab_regions = [
    # "us-east-1",
    "us-west-1",
    "us-west-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1",
    "eu-west-3",
    "eu-north-1",
    "ap-southeast-1",
    "ap-northeast-1",
    "ap-southeast-2",
    "ap-northeast-3",
    "ap-northeast-2",
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

for region in lab_regions:

    ec2client = boto3.client('ec2',region_name=region)
    response = ec2client.describe_instances()

    instances = []
    creation_time = []
    

    # pprint(response)

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instance_details = []

            if (instance['State']['Name'] == 'running' or instance['State']['Name'] == 'stopped'):
                try:
                    if(instance['KeyName']):
                        instance_name = instance['KeyName'][0:-3]
                        # instances.append(instance_name)
                        instance_details.append(instance_name)
                        InstanceID=(instance['InstanceId'])
                        NetworkInterfaceID =(instance['NetworkInterfaces'][0]['NetworkInterfaceId'])
                        NetworkInterface_details = ec2client.describe_network_interfaces(NetworkInterfaceIds=[NetworkInterfaceID])
                        networkinterface_id_attachedtime = NetworkInterface_details['NetworkInterfaces'][0]['Attachment']['AttachTime']
                        # creation_time.append(networkinterface_id_attachedtime)
                        instance_details.append(str(networkinterface_id_attachedtime))
                        # pprint(networkinterface_id_attachedtime)
                        instances.append(instance_details)
                        
                except:
                    print("No Ec2 in this region")
                    continue
    
    # pprint(instances)

    print("="*30)
    print(f"*** Region: {region} *** ")
    print("="*30)
    
    for instance_detail in instances:
        pprint(f"Instance de {instance_detail[0]}:  Created at --> {instance_detail[1]} .")
    print()

    with open(lab_groups[i]+'-EC2-Lab.txt','w',encoding = 'utf-8') as f:
        f.write(f"{region}\n")
        f.write("================\n")
        for instance_detail in instances:
            f.write(f"instance {instance_detail[0]} created at {instance_detail[1]}."+"\n")

    i = i+1




   
