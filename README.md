Flask S3 Bucket Content Listing Service

Overview

This project implements an HTTP service using Flask to expose an API endpoint that lists the contents of an S3 bucket. The service is hosted on an EC2 instance and allows users to retrieve the content of the specified path in the bucket.

Features

Lists top-level contents of the S3 bucket.

Lists contents of a specified directory within the S3 bucket.

Returns results in JSON format.

Infrastructure Setup (Terraform)

Prerequisites

Terraform installed on your local machine.

AWS CLI configured with necessary credentials.

An S3 bucket created to store files.

Steps

Initialize Terraform:

terraform init

Validate Terraform configuration:

terraform validate

Apply Terraform configuration to create infrastructure:

terraform apply --auto-approve

This will create:

An S3 bucket.

An IAM role with permissions to access the bucket.

An EC2 instance to host the Flask app.

Deploying Flask Application

Connect to EC2 instance

ssh -i your-key.pem ubuntu@your-ec2-public-ip

Install Dependencies

sudo apt update -y
sudo apt install python3-pip -y
pip3 install flask boto3

Create the Flask App (app.py)

from flask import Flask, jsonify
import boto3
import os
from botocore.exceptions import ClientError

app = Flask(__name__)

# Load configuration from environment variables
BUCKET_NAME = "one2n-s3-bucket"

# Initialize S3 client
s3_client = boto3.client("s3")


def list_s3_objects(prefix=""):
    """List objects in S3 bucket with a given prefix."""
    try:
        if prefix and not prefix.endswith("/"):
            prefix += "/"

        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        contents = []
        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if key != prefix:
                    contents.append(key[len(prefix) :].split("/")[0])

        # Remove duplicates and sort
        contents = sorted(set(contents))

        return {"content": contents}

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/list-bucket-content", defaults={"path": ""}, methods=["GET"])
@app.route("/list-bucket-content/<path:path>", methods=["GET"])
def list_bucket_content(path):
    """API Endpoint to list S3 bucket contents."""
    result = list_s3_objects(prefix=path)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

Set Environment Variables

echo "export S3_BUCKET=your-bucket-name" >> ~/.bashrc
echo "export AWS_REGION=us-east-1" >> ~/.bashrc
source ~/.bashrc

Or In my case I have use it on woking terminal
export AWS_ACCESS_KEY_ID="your access key"
export AWS_SECRET_KEY_ID="your secret key "
export AWS_REGION_ID="region"
export BUCKET_NAME="Bucket name"

Run the Flask Application

python3 main.py & or 
nohup python main.py 

API Usage

List Top-Level Contents

curl http://your-ec2-ip:5000/list-bucket-content

Response:

{"content": ["dir1", "dir2", "file1", "file2"]}

List Directory Contents

curl http://your-ec2-ip:5000/list-bucket-content/dir1

Response:

{"content": []}

curl http://your-ec2-ip:5000/list-bucket-content/dir2

Response:

{"content": ["file1", "file2"]}

Troubleshooting

404 Error

Ensure Flask is running (ps aux | grep python).

Restart Flask if necessary (pkill -f flask; python3 main.py &).

Check security group rules to allow port 5000.

500 Error

Verify S3 bucket permissions.

Check environment variables are correctly set.

View Flask logs for errors (tail -f flask.log).

You can see terraform.tf file in code.

Another approch 

Deploy using AWS Lambda with Api Gateway instead of EC2.

Implement authentication for the API.

Deploy behind an Application Load Balancer with HTTPS.

Conclusion

This project successfully sets up an HTTP service to list S3 bucket contents using Flask, hosted on AWS EC2, and deployed via Terraform.
