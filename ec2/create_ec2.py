import boto3

ec2 = boto3.resource('ec2')
instance = ec2.create_instances(ImageId='ami-824c4ee2', MinCount=1, MaxCount=1,
InstanceType='m5.xlarge',
Placement={'AvailabilityZone': 'us-east-2'},
)

print(instance[0])