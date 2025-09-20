import boto3

# Create a session using the profile 'myprofile'
session = boto3.Session(profile_name='myprofile')

# Example: Connect to S3 and list buckets
s3 = session.client('s3')
response = s3.list_buckets()

print('Existing S3 buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
