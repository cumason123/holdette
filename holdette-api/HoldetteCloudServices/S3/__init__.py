class Bucket():
	def __init__(self, bucket_name, iam_role):
		self.bucket_name = bucket_name
		self.iam_role = iam_role

		self.s3_client = boto3.client('s3', 
			aws_access_key_id = self.iam_role['access-key'], 
			aws_secret_access_key = self.iam_role['access-secret']
		)

	def upload_item(self, file_contents, username, product_name):
		if '*' in username or ''
		filename = '*'.join()
