import uuid
import time
import os
import boto3
class Bucket():
	def __init__(self, bucket_name, iam_role):
		self.bucket_name = bucket_name
		self.iam_role = iam_role

		self.s3_client = boto3.client('s3', 
			aws_access_key_id = self.iam_role['access-key'], 
			aws_secret_access_key = self.iam_role['access-secret']
		)

	def upload_item(self, image, vendor):
		filename = str(time.time()).replace('.', '') + str(uuid.uuid4()).replace('-', '')
		filename = os.path.join(vendor, unique_identifier)
		self.s3_client.upload_fileobj(image, 'holdette-products', filename)