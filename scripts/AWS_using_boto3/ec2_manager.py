# Basic script to manage EC2 instances using CLI

import boto3

ec2 = boto3.client("ec2")

#function to list the instances
def listEC2_Instances():
  resp = ec2.describe_instances()

  for reservation in resp["Reservations"]:
    for instance in reservation["Instances"]:
      instance_id = instance["InstanceId"]
      state = instance["State"]["Name"]
      
      print(f"Instance_ID: {instance_id}\nInstance_State: {state}")


if __name__ == "__main__":
  listEC2_Instances()
