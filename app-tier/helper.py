import boto3
import json
import base64


'''
   SQS QUEUE Helper functions
'''
def receiveMessageFromQueue(sqs, queue_url):
    message = None
    try:
        # Receive message from SQS queue
        message = sqs.receive_message(
                        QueueUrl=queue_url,
                        AttributeNames=[
                            'All'
                        ],
                        MaxNumberOfMessages=1,
                        MessageAttributeNames=[
                            'All'
                        ],
                        VisibilityTimeout=5,
                        WaitTimeSeconds=20  # Long polling - the maximum time, in seconds, that a Rec
                    )
        if 'Messages' not in message:
            return None
        
    except Exception as error:
        print("Error: Couldn't receive messages from queue :%s", error)

    return message

def deleteMessageFromQueue(sqs, queue_url, message):
    try:
        if 'Messages' in message:
            message = message['Messages'][0]
            if "ReceiptHandle" in message:
                receipt_handle = message['ReceiptHandle']
                # Delete received message from queue
                response = sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )

                # Check the response for success
                if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("Message deleted successfully")
                else:
                    print("Failed to delete message. Error response:", response)
    except Exception as e:
        print("Error: Unexpected error while deleting messages from queue :%s", e)

def sendResponseThroughQueue(sqs_client, sqs_url, result):
    response = None
    try:
        response = sqs_client.send_message(
                    QueueUrl=sqs_url,
                    MessageBody=result
                )
    except Exception as error:
            print("Error: Couldn't send message to queue: %s", error)
            
    return response

def isFilenameValid(name):
    if len(name) > 0:
        name = name.rsplit('.', 1)
        if(len(name)>1):
            return name[1].lower() in ['jpg', 'jpeg', 'png']
    return False

def parseRequest(request):
    try:
        imagepath = ""
        if "Messages" in request:
            message = request['Messages'][0]
            if "MessageAttributes" in message:
                msgAttr = message['MessageAttributes']
                name = msgAttr['ImageName']['StringValue']
                body = message['Body']

                if not isFilenameValid(name) or len(body) == 0:
                    raise Exception("Invalid image file")
                imagepath = "/home/ubuntu/app-tier/images/" + name
                print(f"Storing image at {imagepath}")
                image = base64.b64decode(str.encode(body))
                with open(imagepath, 'wb') as file:
                    file.write(image)
                    file.close()
            else:
                print(f"No MessageAttributes in the message {message}\n\n")
        return imagepath
    except ValueError:
        print("Error: Failed to parse message: ", request['Messages'][0])
    except Exception as error:
        print("Error: Couldn't parse messages :%s", error)