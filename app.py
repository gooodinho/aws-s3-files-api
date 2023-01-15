import boto3
import logging
import mimetypes

from flask import Flask, request, jsonify
from botocore.exceptions import ClientError


app = Flask(__name__)

AWS_HEADERS_UPLOAD = ('Secret-Key', 'Key-Id', 'Bucket-Name', 'File-Name', 'Content-Type')
AWS_HEADERS_DOWNLOAD = ('Secret-Key', 'Key-Id', 'Bucket-Name', 'File-Download-Path')
AWS_HEADERS_DELETE = ('Secret-Key', 'Key-Id', 'Bucket-Name')

def create_s3_client(key_id: str, secret_key: str):
    """Create s3 boto3 client with credentials: aws_access_key_id, aws_secret_access_key"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id = key_id,
        aws_secret_access_key = secret_key
    )
    return s3_client


@app.route('/<file_name>', methods=["GET"])
def download_file(file_name: str):
    if all(aws_header in request.headers.keys() for aws_header in AWS_HEADERS_DOWNLOAD):
        """Download file from aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name, File-Download-Path. Optional header: File-Location"""
        secret_key = request.headers['Secret-Key']
        key_id = request.headers['Key-Id']
        bucket_name = request.headers['Bucket-Name']
        file_download_path = request.headers['File-Download-Path']
        file_location = request.headers.get('File-Location', None)

        # Check if 'File-Location' header exist. If it exist file is downloaed from passed folder, if not downloaded from the root directory.
        if file_location:
            object_key = f"{file_location}{file_name}"
        else:
            object_key = f"{file_name}"

        s3_client = create_s3_client(key_id, secret_key)

        try:
            s3_client.download_file(bucket_name, object_key, file_download_path)
        except Exception as e:
            logging.error(e)
            return jsonify({"error": "Error has occurred while file was downloading"})
        return jsonify({"Status": "File was successfully downloaded"})
    else:
        return jsonify({"error": "You're missing one of the following: 'Secret-Key', 'Key-Id', 'Bucket-Name', 'File-Download-Path'"})


@app.route('/delete-file/<file_name>', methods=['DELETE'])
def delete_file(file_name: str):
    """"Delete file from aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name. Optional header: File-Location"""
    if all(aws_header in request.headers.keys() for aws_header in AWS_HEADERS_DELETE):
        secret_key = request.headers['Secret-Key']
        key_id = request.headers['Key-Id']
        bucket_name = request.headers['Bucket-Name']
        file_location = request.headers.get('File-Location', None)

        # Check if 'File-Location' header exist. If it exist file is deleted from passed folder, if not deleted from the root directory.
        if file_location:
            object_key = f"{file_location}{file_name}"
        else:
            object_key = f"{file_name}"

        s3_client = create_s3_client(key_id, secret_key)

        try:
            s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        except Exception as e:
            logging.error(e)
            return jsonify({"error": "Error has occurred while file was deleting"})
        return jsonify({"Status": "File was successfully deleted from bucket"})
    else:
        return jsonify({"error": "You're missing one of the following: 'Secret-Key', 'Key-Id', 'Bucket-Name'"})


@app.route('/upload-file', methods=["POST", "PUT"])
def upload_file():
    """Upload binary file to aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name, Content-Type, File-Name."""
    # Check if part of required headers exists
    if all(aws_header in request.headers.keys() for aws_header in AWS_HEADERS_UPLOAD):
        secret_key = request.headers['Secret-Key']
        key_id = request.headers['Key-Id']
        bucket_name = request.headers['Bucket-Name']
        file_name = request.headers['File-Name']
        contet_type = request.headers['Content-Type']

        mtype = mimetypes.guess_extension(contet_type)

        object_key = f"{file_name}{mtype}"

        s3_client = create_s3_client(key_id, secret_key)

        try:
            response = s3_client.put_object(Body=request.data, Bucket=bucket_name, Key=object_key)
        except ClientError as e:
            logging.error(e)
            return jsonify({"error": "ClientError has occurred"})   
        return jsonify(response)
    else:
        return jsonify({"error": "You're missing one of the following headers: 'Secret-Key', 'Key-Id', 'Bucket-Name', 'File-Name', 'Content-Type'"})



if __name__ == '__main__':
    app.run()