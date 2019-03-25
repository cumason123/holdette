import pandas as pd
import boto3
import os
import sys
import json
from .UserPools import UserPool
from .Products import Product
from .Errors import Error
# from UserPools import UserPool
# from Products import Product
# from Errors import Error


class Cloud():
	error = Error()

	def __init__(self):
		filename = 'configs.json'
		if not os.path.exists(filename):
			raise Valueself.ERROR('No such configuration file: {0}'.format(filename))

		with open(filename, 'r') as file:
			self.configs = json.load(file)
		
		self.iam = self.configs['iam-role']
		self.holdette_consumers = UserPool(self.configs['holdette-consumers']['user-pool'], self.configs['iam-role'])
		self.holdette_designers = UserPool(self.configs['holdette-designers']['user-pool'], self.configs['iam-role'])
		
		self.s3_client = boto3.client('s3', 
			aws_access_key_id = self.iam['access-key'], 
			aws_secret_access_key = self.iam['access-secret']
		)

	def consumerRegister(self, data):
		return self.holdette_consumers.register(data)

	def consumerLogin(self, data):
		if 'username' not in data.keys() or 'password' not in data.keys():
			return self.error.INVALID_CREDENTIALS, 'missing username or password fields'
		return self.holdette_consumers.login(data['username'][0], data['password'][0])

	def designerRegister(self, data):
		return self.holdette_designers.register(data)

	def designerLogin(self, username, password):
		raise NotImplementedError()

	def designerUploadProduct(self, data):
		return self.holdette_designers.validate_access_token(data['access-token'])
# if 'username' not in data.keys() or 'access-key' not in data.keys():
# 	return self.error.INVALID_CREDENTIALS, 'Missing access key or username'

# state, result = self.holdette_designers.validate_access_token(data['access-token'])
# if state == self.error.SUCCESS:
# 	assert(result[''])
# 	try:
# 		product = Product(data)
# 	except AssertionError():

# self.s3_client.

# return state, result




