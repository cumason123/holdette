import uuid
def valid_product(prod):
	required_attributes = ['upid', 'vendor-username', 'image', 'price', 'stock']
	optional_attributes = ['description']

	keys = prod.keys()
	ret = {}

	for attribute in required_attributes:
		if (attribute not in keys):
			return {}
		ret[attribute] = prod[attribute]
		
	ret['upid'] = uuid.uuid1()
	return ret

		