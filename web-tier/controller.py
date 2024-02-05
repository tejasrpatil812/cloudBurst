import boto3
import time
import json

# Load config file
config = json.load(open("config.json", "r"))

# SQS queue URL
queue_url = config["sqs"]["request_queue"]["url"]

# Minimum and maximum number of instances
min_instances = 1
max_instances = 20

current_instance_number = 1

# Initialize SQS and EC2 clients
aws_session = boto3.Session(**config["aws"])
ec2 = aws_session.resource("ec2")
sqs_client = aws_session.client("sqs")

instance_ids = []


def create_ec2_instance(ec2, configs, instance_number):
    configs["TagSpecifications"][0]["Tags"][0]["Value"] = f"app-tier{instance_number}"
    return ec2.create_instances(**configs)


def fetch_running_instance_ids(ec2):
    global instance_ids
    instance_ids = [
        instance.id
        for instance in ec2.instances.filter(
            Filters=[
                {"Name": "instance-state-name", "Values": ["running", "pending"]},
                {"Name": "tag:Name", "Values": ["app-tier*"]},
            ]
        )
    ]
    print(f"Currently {len(instance_ids)} app-tier instances running")


def get_queue_depth():
    # Get the approximate number of messages in the SQS queue
    requests = sqs_client.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
    )

    return int(requests["Attributes"]["ApproximateNumberOfMessages"])


def scale_instances(num_instances):
    global instance_ids
    global current_instance_number
    current_instances = len(instance_ids)
    if current_instances < num_instances:
        diff = num_instances - current_instances
        print(f"Creating {num_instances - current_instances} new instances")
        for i in range(diff):
            resp = create_ec2_instance(
                ec2, config["app-tier"], instance_number=current_instance_number + 1
            )
            current_instance_number += 1
            instance_ids.append(resp[0].id)
    elif current_instances > num_instances:
        print(f"Terminating {current_instances - num_instances} instances")
        ec2.instances.filter(InstanceIds=instance_ids[num_instances:]).terminate()
        instance_ids = instance_ids[:num_instances]
        current_instance_number = num_instances
    else:
        print("Demand already met, No scaling required")


def main():
    try:
        fetch_running_instance_ids(ec2)
        while True:
            # Get the number of messages in the SQS queue
            queue_depth = get_queue_depth()
            # queue_depth = int(input("Enter queue depth: "))
            print("Queue depth: ", queue_depth)
            # Scale instances based on the queue depth
            if queue_depth == 0:
                scale_instances(min_instances)
            elif queue_depth > 0 and queue_depth <= max_instances:
                scale_instances(queue_depth)
            else:
                scale_instances(max_instances)

            # Wait for 20 seconds before checking again
            time.sleep(20)

    except KeyboardInterrupt:
        print("Controller interrupted, exiting...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
