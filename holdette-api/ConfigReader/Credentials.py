import pandas as pd
import os
class Credentials():
	def __init__(self, config_filename = 'config.csv'):
		data = pd.read_csv(config_filename)
		self.df = data
	
	def get(self, api_name):
		data = self.df.apply(lambda row: row if row['api_name'] == api_name else None, axis=1).dropna().to_dict()
		return {'key':data['key'][0], 'secret':data['secret'][0], 'api':data['api_name'][0]}

	def getall(self):
		return self.df.dropna().to_dict()