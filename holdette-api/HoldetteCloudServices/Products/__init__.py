import uuid
def valid_product(prod):
	required_attributes = ['username', 'image', 'price', 'stock', 
		'description', 'sizes', 'title', 'tags']
	# stock and sizes
	keys = prod.keys()
	ret = {}
	print(prod)
	for attribute in required_attributes:
		if (attribute not in keys):
			return None
	print('Image Type: ')
	print(prod['image'])

	prod['upid'] = uuid.uuid1()
	return prod

		