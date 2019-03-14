import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

class UserPool():
	ERROR = -1
	SUCCESS = 0
	USER_EXISTS = 1
	def __init__(self, pool_dict):
		try:
			self.client_id = pool_dict['app-client']['id']
			self.client_secret = pool_dict['app-client']['secret']
			self.pool_id = pool_dict['pool-id']
			self.pool_arn = pool_dict['pool-arn']
			self.required_attributes = pool_dict['pool-required-attributes']
			self.client = boto3.client('cognito-idp', 'us-east-1')
		except ValueError as e:
			print(e)
			raise ValueError('Check fields in configuration file')

		

	def getSecretHash(self, username):
		"""
		Creates hmac token using a client's username

		@param username: String representing client's username
		@returns: hmac encoded token using username, client id and client secret
		"""
		msg = username + self.client_id
		dig = hmac.new(str(self.client_secret).encode('utf-8'), 
			msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
		d2 = base64.b64encode(dig).decode()
		return d2	

	def login(username, password):
		try:
			resp = client.admin_initiate_auth(
				UserPoolId=self.pool_id,
				ClientId=self.client_id,
				AuthFlow='ADMIN_NO_SRP_AUTH',
				AuthParameters={
					'USERNAME': username,
					'SECRET_HASH': get_secret_hash(username),
					'PASSWORD': password
				},
				ClientMetadata={
					'username': username,
					'password': password
				})
		except client.exceptions.NotAuthorizedException as e:
			return None, "The username or password is incorrect"
		except Exception as e:
			print(e)
			return None, "Unknown error"
		return resp, None
	
	def register(self, data):
		raise NotImplementedError()

	def login(self, data):
		raise NotImplementedError()



