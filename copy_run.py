import os

# Helper script that can-
# 1. Copy file to web-tier or app-tier EC2 instance (using web/app option)
# 2. Run workoad_generator or multithreaded_workload_generator for testing (using run/multirun option)

ec2 = input("web/app/run/multirun?: ")

#TODO : Update the url to current instance
web = "ec2-54-205-194-143.compute-1.amazonaws.com"
app = "ec2-3-81-19-57.compute-1.amazonaws.com"

# To run workload genrators
if ec2=="run" or ec2=="multirun":
     num = int(input("num requests?"))
     if ec2=="run":
         os.system(f"python workload_generator.py --num_request {num} --url http://{web}:8000/upload --image_folder app-tier/data/imagenet-100-updated/imagenet-100/")
     else:
         os.system(f"python multithreaded_workload_generator.py --num_request {num} --url http://{web}:8000/upload --image_folder app-tier/data/imagenet-100-updated/imagenet-100/")     
else:
    # To copy files
    file = input("file: ")

    #Note - If file is empty it copies entire directory (web-tier or app-tier) recursively
    if ec2=="web":
        dest = f"ubuntu@{web}:~/"
        if not file=="":
            dest += "web-tier"
        file = "web-tier/"+file
    elif ec2 == "app":
        dest = f"ubuntu@{app}:~/"
        if not file=="":
            dest += "app-tier"
        file = "app-tier/"+file
    else:
        print("Invalid option")
        exit()

    os.system(f"scp -i ~/.ssh/ssh_sri.pem -r {file} {dest}")

