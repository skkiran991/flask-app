from flask import Flask, jsonify
import boto3

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