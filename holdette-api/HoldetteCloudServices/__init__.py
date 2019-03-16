import pandas as pd
import boto3
import os
import sys
import json
from .UserPools import UserPoolAPI

class Cloud():
	error = UserPoolAPI.error
	def __init__(self):
		filename = 'configs.json'
		if not os.path.exists(filename):
			raise Valueself.ERROR('No such configuration file: {0}'.format(filename))

		with open(filename, 'r') as file:
			self.configs = json.load(file)
		
		self.iam = self.configs['iam-role']
		self.holdette_consumers = UserPoolAPI(self.configs['holdette-consumers']['user-pool'], self.configs['iam-role'])
		self.holdette_designers = UserPoolAPI(self.configs['holdette-designers']['user-pool'], self.configs['iam-role'])

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


