import pandas as pd
import boto3
import os
import sys
import json
from .UserPools.HoldetteConsumers import ConsumerUserPool

class Cloud():
	ERROR = -1
	SUCCESS = 0
	USER_EXISTS = 1
	def __init__(self):
		filename = 'configs.json'
		if not os.path.exists(filename):
			raise Valueself.ERROR('No such configuration file: {0}'.format(filename))

		with open(filename, 'r') as file:
			self.configs = json.load(file)

		self.iam = self.configs['iam-role']
		self.holdette_consumers = ConsumerUserPool(self.configs['holdette-consumers']['user-pool'])

	def registerConsumer(self, data):
		return self.holdette_consumers.register(data)
