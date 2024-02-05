from flask import Flask, request, jsonify
import boto3
import base64
import json
import time

app = Flask(__name__)
config = json.load(open("./config.json", "r"))

# Initialize SQS client
sqs_client = boto3.client("sqs", **config["aws"])

results = {}


@app.route("/", methods=["GET"])
def hello():
    return "Hello!"


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong"


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "myfile" not in request.files:
            return "Request key 'myfile' not found. Image not uploaded to request", 400

        # Handle file upload logic here
        uploaded_files = request.files.getlist("myfile")
        if len(uploaded_files) > 1:
            return "Request key 'myfile' invalid. Expecting one Image per request", 400

        filename = uploaded_files[0].filename.split("/")[-1].split(".")[0]
        print("request received for ", filename)

        # Send the message to request SQS queue
        sendMessageToQueue(uploaded_files)
        print(f"image queued, waiting for server response for {filename}")

        # Read message from response SQS queue
        return receiveMessagefromQueue(filename)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


def sendMessageToQueue(files):
    for file in files:
        filename = file.filename
        bytes = base64.b64encode(file.read())

        sqs_client.send_message(
            QueueUrl=config["sqs"]["request_queue"]["url"],
            MessageAttributes={
                "ImageName": {"DataType": "String", "StringValue": filename}
            },
            MessageBody=bytes.decode("ascii"),
        )


def receiveMessagefromQueue(expectedFile):
    while True:
        # Keep trying to read messages till we get the result for the request
        msg = sqs_client.receive_message(
            QueueUrl=config["sqs"]["response_queue"]["url"],
            AttributeNames=["All"],
            MaxNumberOfMessages=1,
            MessageAttributeNames=["All"],
            VisibilityTimeout=5,
            WaitTimeSeconds=20,  # Long polling - the maximum time, in seconds, that a Rec
        )
        if "Messages" in msg:
            message_body = msg["Messages"][0]["Body"]
            print(f"Message Received: {message_body}")
            if message_body == "" or len(message_body.split(",")) != 2:
                print(
                    f"Error: unexpected message received ({message_body}).\nTrying again!"
                )
                continue
            file, result = message_body.split(",")
            results[file] = result

            sqs_client.delete_message(
                QueueUrl=config["sqs"]["response_queue"]["url"],
                ReceiptHandle=msg["Messages"][0]["ReceiptHandle"],
            )

        # check if we got the result and return
        if expectedFile in results.keys():
            return results[expectedFile]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", debug=True, threaded=True)
