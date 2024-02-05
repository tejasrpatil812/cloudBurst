Setup -
1. Before running the setup.py
    a. Add key-pair in EC2 instance page (current: "personal")
    b. Update KeyName in config.json file if not using "personal" keyname
    c. Create a security group with inbound rules for SSH and Custom TCP on port 8000.
    d. Update the security group id in the config.json file.
    e. Update config.json with your access_key_id and secret_access_key.
    f. Update config file path in setup.py

2. Run setup.py: This will create 2 EC2, 2 SQS and 2 S3 buckets in your account

3. Update the queue urls and s3 bucket names in the config files.

4. A **web-tier** instance (a general Ubuntu Instance).
    a. copy web-tier to /home/Ubuntu
    b. pip install boto3 and pip install Flask
    c. run app.py

5. A **app-tier** instance (later auto-scale group).
    a. copy app-tier (all python files and config.json) to /home/ubuntu/app-tier
    b. pip install boto3
    c. mkdir images in app-tier
    d. Take an image of the instance. This is the AMI used for creating the scaling app-tier instances by the controller. 
    e. Update web-tier config.json with that AMI ID.


**Note-**
Update the access keys, and resource urls in both the config files 

**SSH command**
ssh  -i /path/to/ssh/key.pem  ubuntu@<instance-dns-name>.compute-1.amazonaws.com

**To Copy:**
scp -i /path/to/ssh/key.pem  -r /path/to/local/file ubuntu@<instance-dns-name>.compute-1.amazonaws.com:/home/ubuntu/<app-tier or web-tier>/
