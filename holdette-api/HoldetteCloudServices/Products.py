import uuid
class Product(dict):
	def __init__(self, data):
		required_attributes = ['upid', 'vendor-username', 'image', 'price', 'stock']
		optional_attributes = ['description']

		keys = data.keys()

		for attribute in required_attributes:
			assert(attribute in keys)
			self[attribute] = data[attribute]
			
		self['upid'] = uuid.uuid1()


		