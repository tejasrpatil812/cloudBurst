import boto3
import json
import random
import botocore

config = json.load(open("config.json", "r"))
aws_session = boto3.Session(**config["aws"])


def get_aws_resource(resource: str):
    return aws_session.resource(resource)


def create_ec2_instance(ec2, configs):
    return ec2.create_instances(**configs)


if __name__ == "__main__":

    # Creating EC2 instance for Web Tier
    ec2 = get_aws_resource("ec2")
    # app_tier_instance = create_ec2_instance(ec2, config['app-tier'])
    web_tier_instance = create_ec2_instance(ec2, config["web-tier"])

    # Creating 2 SQS for request and responce
    sqs = get_aws_resource("sqs")
    queue = sqs.create_queue(QueueName="request-queue")
    print(queue.url)
    queue = sqs.create_queue(QueueName="response-queue")
    print(queue.url)

    # Creating 2 S3 buckets for input and output
    s3 = get_aws_resource("s3")
    random_suffix = random.randrange(start=1, stop=99, step=1)
    print(f"Random Suffix {random_suffix} being added to bucket's name.")
    input_bucket = s3.create_bucket(Bucket=f"input-bucket-{random_suffix}")
    input_bucket = s3.create_bucket(Bucket=f"output-bucket-{random_suffix}")
