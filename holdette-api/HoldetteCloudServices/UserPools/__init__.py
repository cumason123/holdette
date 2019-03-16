import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
from .Errors import Error

class UserPoolAPI():
	error = Error()
	def __init__(self, pool_dict, iam_dict):
		try:
			self.client_id = pool_dict['app-client']['id']
			self.client_secret = pool_dict['app-client']['secret']
			self.pool_id = pool_dict['pool-id']
			self.required_attributes = pool_dict['pool-required-attributes']
			self.client = boto3.client('cognito-idp', 
				aws_access_key_id=iam_dict['access-key'], 
				aws_secret_access_key=iam_dict['access-secret'],
				region_name='us-east-1'
				)
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
	

	def register(self, data):
		keys = set(data.keys())
		if len(set(self.required_attributes) - keys) > 0 or \
			'username' not in keys or \
			'password' not in keys:

			print("Missing required attributes")
			return self.error.ERROR, "Missing required fields."

		# Get first index because data will be in the format of a list
		user_attributes = [{'Name':key,'Value':data[key][0]} for key in keys if (key != 'username' and key != 'password')]
		username = data['username'][0]
		password = data['password'][0]
		try:
			hashCode = self.getSecretHash(username)
			resp = self.client.sign_up(
				ClientId=self.client_id,
				SecretHash=hashCode,
				Username=username,
				Password=password,
				UserAttributes=user_attributes)
			print(resp)

		except self.client.exceptions.UsernameExistsException as e:
			print(e)
			return self.error.USER_EXISTS, "User already registered."

		except Exception as e:
			print(e)
			return self.error.ERROR, "Oops! Unknown error, please recheck fields!"

		return resp, None


	def login(self, username, password):
		try:
			resp = self.client.admin_initiate_auth(
				UserPoolId=self.pool_id,
				ClientId=self.client_id,
				AuthFlow='ADMIN_NO_SRP_AUTH',
				AuthParameters={
					'USERNAME': username,
					'SECRET_HASH': self.getSecretHash(username),
					'PASSWORD': password
				})
			
		except self.client.exceptions.NotAuthorizedException as e:
			return self.error.INVALID_CREDENTIALS, "The username or password is incorrect"

		except Exception as e:
			print(e)
			return self.error.ERROR, "Internal Server Error"
			
		return resp, None



