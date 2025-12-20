# Basic script to manage EC2 instances using CLI

import boto3
import argparse

ec2 = boto3.client("ec2")

#function to list the instances
def listEC2_Instances():
  resp = ec2.describe_instances()

  for reservation in resp["Reservations"]:
    for instance in reservation["Instances"]:
      instance_id = instance["InstanceId"]
      state = instance["State"]["Name"]
      
      print(f"Instance_ID: {instance_id}\nInstance_State: {state}\n\n")

#function to get instance_state
def get_instance_state(instance_id):
  resp = ec2.describe_instances(InstanceIds=[instance_id])
  state = resp["Reservations"][0]["Instances"][0]["State"]["Name"]
  return state

#function to start a stopped instance
def start_stopped_instance(instance_id):
  state = get_instance_state(instance_id)
  if state == "running":
    print(f"Instance with ID: {instance_id} already running\n")
    return

  ec2.start_instances(InstanceIds=[instance_id])
  print(f"Instance with ID: {instance_id} started!\n")

def stop_instance(instance_id):
  state = get_instance_state(instance_id)
  if (state == "stopped" or state == "stopping"):
    print(f"Instance with ID: {instance_id} already stopped\n")
    return

  ec2.stop_instances(InstanceIds=[instance_id])
  print(f"Instance with ID: {instance_id} stopped!\n")



if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument("--list", action="store_true")
  parser.add_argument("--start", action="store_true")
  parser.add_argument("--stop", action="store_true")
  parser.add_argument("--id")

  args = parser.parse_args()
  
  if args.list:
    listEC2_Instances()
    
  elif args.start:
    if args.id:
      start_stopped_instance(args.id)
    else:
      print("[ERROR] Please mention the Instance ID\n")

  elif args.stop:
    if args.id:
      stop_instance(args.id)
    else:
      print("[ERROR] Please mention the Instance ID\n")
