from pprint import pprint
from time import sleep
import boto3
from botocore.exceptions import ClientError

lab_regions = [
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

instance_sg_default = ["default", "launch"]

for region in lab_regions:

    ec2client = boto3.client('ec2',region_name=region)
    EC2_RESOURCE = boto3.resource('ec2', region_name=region)

    response = ec2client.describe_instances()

    instance_ids = []
    instance_sgs  = []

    print("*****************************")
    print(f"region:  **** {region} ****")
    print("*****************************")

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if ((instance['State']['Name'] == 'stopped') or (instance['State']['Name'] == 'running')):
                instance_id = (instance["InstanceId"])
                # pprint(instance_id)
                print()
                # pprint(instance)
                instance_ids.append(instance_id)
                instance_sg = instance["SecurityGroups"]
                for sg in instance_sg: 
                    if(not(instance_sg_default[0] in sg['GroupName'])
                                            or 
                    not(instance_sg_default[1] in sg['GroupName'])):
                        instance_sgs.append(sg)
                
                    SECURITY_GROUP_ID = sg['GroupId']
                    security_group = EC2_RESOURCE.SecurityGroup(SECURITY_GROUP_ID)
                    try:
                        security_group.delete()
                        print(f'Security Group {SECURITY_GROUP_ID} has been deleted')
                    except ClientError as e:
                        print(e)
                        print()
                        print(f'Security Group {SECURITY_GROUP_ID} Associated within a VPC or an Instance :( ')
                        print("Deletion Not Possible")
                        print("x"*70)
                        continue


    for security_group in instance_sgs:
        print(f' - Security Group {security_group}')
    
    print("*****************************")
    
    for instance_id in instance_ids:
        # Do a dryrun first to verify permissions
        try:
            ec2client.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            print()
            pprint(f"Moving and deleting instance with id {instance_id}")
            print("*"*70)
            # instance = ec2resource.Instance(instance_id)
            # instance.stop()
            # instance.wait_until_stopped()
            # instance.modify_attribute(
            #     DisableApiTermination={
            #         'Value': True
            # })
            # Stop the instance
            ec2client.stop_instances(InstanceIds=[instance_id])
            # Modify the instance
            ec2client.modify_instance_attribute(
                    InstanceId=instance_id, 
                    Attribute='disableApiTermination', 
                    Value='False')
            waiter=ec2client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
            response = ec2client.terminate_instances(InstanceIds=[instance_id], DryRun=False)
            pprint(f"TerminatingInstances: {response['TerminatingInstances']}")
            print("-"*70)
            print("-"*70)
        except ClientError as e:
            pprint(e)
            continue

    # sleep(30)
    
    # print("Attempt to delete Security Group Again After Instance Termination")

    # for sg in instance_sgs:
    #     # pprint(sg)
    #     SECURITY_GROUP_ID = sg['GroupId']
    #     security_group = EC2_RESOURCE.SecurityGroup(SECURITY_GROUP_ID)
    #     try:
    #         security_group.delete()
    #         print(f'Security Group {SECURITY_GROUP_ID} has been deleted Succesfully')
    #     except ClientError as e:
    #         print(e)
    #         print()
    #         print(f'Security Group {SECURITY_GROUP_ID} Associated within a VPC or an Instance :( ')
    #         print("Deletion Not Possible")
    #         print("x"*70)
    #         continue

