from .GenericUserPool import UserPool

class ConsumerUserPool(UserPool):	
	def register(self, data):
		keys = set(data.keys())
		if len(set(self.required_attributes) - keys) > 0 or \
			'username' not in keys or \
			'password' not in keys:

			print("Missing required attributes")
			return self.ERROR, "Missing required fields."

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
			return self.USER_EXISTS, "User already registered."

		except Exception as e:
			print(e)
			return self.ERROR, "oops!"
		return resp, None
