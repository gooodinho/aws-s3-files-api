# API to upload files in binary mode and download to AWS S3 Bucket

## Endpoints:
- **"/\<file_name>" ["GET"]** - Download file from aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name, File-Download-Path. Optional header: File-Location.

**Secret-Key, Key-Id** required to create s3 client with credentials. 

**Bucket-Name** defines in which bucket the data should be loaded.

**File-Download-Path** defines where the downloaded file will be saved.

If **File-Location** is used, file is downloaed from passed folder, if not downloaded from the root directory.

**file_name** url parameter should contain file name with file extention.

- **"/delete-file/<file_name>" ["DELETE"]** - Delete file from aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name. Optional header: File-Location.

**Secret-Key, Key-Id** required to create s3 client with credentials. 

**Bucket-Name** defines in which bucket the file should be deleted.

If **File-Location** is used, file will be deleted in the passed directory. If not file will be deleted in the root directory of the bucket.

**file_name** url parameter should contain file name with file extention.

- **"/upload-file" ["POST", "PUT"]** - Upload binary file to aws s3 bucket. Required headers: Secret-Key, Key-Id, Bucket-Name, Content-Type, File-Name.

**Secret-Key, Key-Id** required to create s3 client with credentials. 

**Bucket-Name** defines in which bucket the file should be deleted.

**Content-Type** defines with what extention the file will be saved.

**File-Name** defines where the file should be saved in the bucket and under which key. If require to save file NOT in the root directory of the bucket pass "dir/filename.ext"

## To get your aws iam credentials, you need to create access keys in IMA console (https://console.aws.amazon.com/iam/).


