import boto3

# ---- WARNING: Hardcoding credentials is insecure. Use environment variables or AWS profiles for production. ----
aws_access_key_id = 'AKIA342CEX24I2HPKON6'
aws_secret_access_key = 'VuynnRg/qGONemTbsOgdftu/C1hqjXnWd+dixmI0'
aws_region = 'us-east-1'  # Change to your preferred region

# Create a session using explicit credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Example: Connect to S3 and list buckets
s3 = session.client('s3')
response = s3.list_buckets()

print('Existing S3 buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
