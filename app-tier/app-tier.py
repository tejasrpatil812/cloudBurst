from helper import *
from image_classification import predict
import boto3
import time
import json
import os
import threading

config = json.load(open("./config.json","r"))
aws_session = boto3.Session(**config["aws"])

def get_aws_client(resource: str):
    return aws_session.client(resource)

processing_lock = threading.Lock()

def process_request(request):
    try:
        # Parsing request and storing the image for classification
        imagePath = parseRequest(request)

        # Running the ML model
        name, result = predict(imagePath)
        print(result)

        if result == "":
            print("Error: Unexpected error occured while classifying the image.")
            return

        #Storing content in S3 buckets
        s3_client = get_aws_client('s3')
        s3_client.upload_file(Filename=imagePath, Bucket=config["s3"]["input_bucket"]["name"], Key=imagePath.split("/")[-1])
        s3_client.put_object(Body=result, Bucket=config["s3"]["output_bucket"]["name"], Key=name)

        # Send response to queue
        sendResponseThroughQueue(sqs_client, config['sqs']['response_queue']['url'], result)
        print("Sent response: ",result)

        # Cleanup: Deleting message from queue and temp image file from local file system
        os.remove(imagePath)
        deleteMessageFromQueue(sqs_client, config['sqs']['request_queue']['url'], request)

        time.sleep(2)
                
    except Exception as e:
        print("Error: Failed to process message: ", e)

def main():
    print("App-tier runnning!!")
    # Initialize SQS client
    global sqs_client
    sqs_client = get_aws_client('sqs')
    # s3_client = get_aws_client('s3')

    while True:
        print("Polling for request....")
        # Poll the SQS queue for messages
        request = receiveMessageFromQueue(sqs_client, config['sqs']['request_queue']['url'])
        if request is not None:
            try:
                # Acquire the lock before processing the request
                processing_lock.acquire()

                # Process the request
                process_request(request)

            finally:
                # Release the lock after processing the request
                processing_lock.release()
            

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print("Exception: ", e)
