import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import urllib.request as req
import json
from jwt.algorithms import RSAAlgorithm
import jwt
from jose import jwt as jt, jwk as jk
import re
from Errors import Error

class UserPool():
	error = Error()
	def __init__(self, pool_dict, iam_dict):
		try:
			self.client_id = pool_dict['app-client']['id']
			self.client_secret = pool_dict['app-client']['secret']
			self.pool_id = pool_dict['pool-id']
			self.required_attributes = pool_dict['pool-required-attributes']
			self.pool_region = pool_dict['pool-region']
			self.keys_url = 'https://cognito-idp.{0}.amazonaws.com/{1}/.well-known/jwks.json'.format(self.pool_region, self.pool_id)
			self.client = boto3.client('cognito-idp', 
				aws_access_key_id=iam_dict['access-key'], 
				aws_secret_access_key=iam_dict['access-secret'],
				region_name=self.pool_region
				)
			# https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json
			response = req.urlopen(self.keys_url)
			self.keys = json.loads(response.read())['keys']
			# Assumption, encryption kids don't change therefore its cached
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

		return self.error.SUCCESS, resp


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
		print(resp)
		return self.error.SUCCESS, resp

	def validate_access_token(self, bearer_token):
		"""
		@returns: (Error, string) where upon success the first value will be the decrypted
			token, otherwise it will be an Error value. String will be errmsg if the first value is Error, and None otherwise.
		"""

		# TODO Timezone auth expiration issues?
		try:
			headers = jt.get_unverified_headers(bearer_token)

			key_index = -1
			print(headers)
			kid = headers['kid']
			for i in range(len(self.keys)):
				if kid == self.keys[i]['kid']:
					key_index = i
					break

			if key_index == -1:
				return self.error.INVALID_KID, 'Invalid Token. Unknown kid id.'

			jwkValue = self.keys[key_index]

			publicKey = RSAAlgorithm.from_jwk(json.dumps(jwkValue))
			decoded_token = jwt.decode(bearer_token, publicKey, algorithm=jwkValue['alg'])
			return self.error.SUCCESS, decoded_token

		except jwt.exceptions.ExpiredSignatureError as e:
			return self.error.EXPIRED_TOKEN, 'Expired token. Please refresh session.'

		except Exception as e:
			print(e)
			return self.error.CORRUPTED_TOKEN, 'Corrupted Token or internal server error.'

		
		


