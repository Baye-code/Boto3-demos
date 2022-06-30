import boto3

ec2 = boto3.resource('ec2')
instance_id = "i-0a81k3ndl29175220"
instance = ec2.Instance(instance_id)
instance.terminate()
