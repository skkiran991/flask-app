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

S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

s3_client = boto3.client('s3', region_name=AWS_REGION)

@app.route('/list-bucket-content', defaults={'path': ''})
@app.route('/list-bucket-content/<path:path>', methods=['GET'])
def list_bucket_content(path):
    try:
        result = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=path, Delimiter='/')
        contents = []
        if 'CommonPrefixes' in result:
            contents += [prefix['Prefix'] for prefix in result['CommonPrefixes']]
        if 'Contents' in result:
            contents += [obj['Key'] for obj in result['Contents']]
        return jsonify({"content": contents})
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

Set Environment Variables

echo "export S3_BUCKET=your-bucket-name" >> ~/.bashrc
echo "export AWS_REGION=us-east-1" >> ~/.bashrc
source ~/.bashrc

Run the Flask Application

python3 app.py &

API Usage

List Top-Level Contents

curl http://your-ec2-ip:5000/list-bucket-content

Response:

{"content": ["dir1", "dir2", "file1", "file2"]}

List Directory Contents

curl http://your-ec2-ip:5000/list-bucket-content/dir1

Response:

{"content": []}

Troubleshooting

404 Error

Ensure Flask is running (ps aux | grep python).

Restart Flask if necessary (pkill -f flask; python3 app.py &).

Check security group rules to allow port 5000.

500 Error

Verify S3 bucket permissions.

Check environment variables are correctly set.

View Flask logs for errors (tail -f flask.log).

Future Improvements

Deploy using AWS Lambda instead of EC2.

Implement authentication for the API.

Deploy behind an Application Load Balancer with HTTPS.

Conclusion

This project successfully sets up an HTTP service to list S3 bucket contents using Flask, hosted on AWS EC2, and deployed via Terraform.
