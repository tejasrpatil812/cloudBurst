# Project README

## Group Members

- Sreechandra Reddy Allala
  - Task: Sreechandra worked primarily on the autoscaling functionality of the application, by developing the logic and functionality that enables dynamic scaling of app-tier instances based on the depth of the request queue. He worked on building the logic for fetching the number of running instances, checking the request queue depth, and creating or terminating the instances based on the depth of request queue. He also ensured that the number of instances always stayed at a minimum of 1 instance and a maximum of 20 instances owing to the limitations of AWS free-tier. 
  
- Ananya Bist
  - Task: Ananya worked on implementing the web server component of the web-tier and establishing communication between the app-tier and web server through SQS queues. This involved configuring a Flask application capable of handling concurrent HTTP requests and sending them to the app-tier via the request-queue. She also implemented the necessary logic in the app-tier to receive, validate, and respond to these requests through the SQS queues.

- Tejas Patil
  - Task: Tejas focused on setting up our infrastructure using code. He created new Amazon Machine Images based on the provided App-tier AMI and designed instance templates for easy deployment. He also automated the execution of code on newly deployed instances, ensuring they started processing pending requests without manual intervention. Additionally, he handled tasks related to converting images and storing data in S3.

## Access Keys

The access key and the secret key for the root user are included in ./config.json, ./app-tier/config.json and ./web-tier/config.json.

However, if you would like to make any changes or use a different access key for the IAM user (credentials below), Here are the details: 
    - aws_access_key_id: AKIA3MM6OJSMIRZHDZ46
    - aws_secret_access_key: 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

The pem file is included in the root directory of the project (ssh_sri.pem)
## AWS Resources
- AWS Credentials:
    - Console sign-in link: https://782553205912.signin.aws.amazon.com/console
    - Username: IAM_user1
    - Password: CloudBurst123
- Web Tier URL: ec2-54-205-194-143.compute-1.amazonaws.com  
# Please note that the above URL is bound to change as we might stop/terminate the instance to avoid billing in free-tier
- SQS Queue:
  - Request Queue:
    - Name: request-queue
    - URL: https://sqs.us-east-1.amazonaws.com/782553205912/request-queue
  - Response Queue:
    - Name: response-queue
    - URL: https://sqs.us-east-1.amazonaws.com/782553205912/response-queue

## S3 Buckets

- Input Images Bucket: input-bucket-32
- Output Results Bucket: output-bucket-32
