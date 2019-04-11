import werkzeug
def valid_product(prod):
	required_attributes = ['username', 'image', 'price', 'stock', 
		'description', 'sizes', 'title', 'tags']
	# stock and sizes
	keys = prod.keys()
	ret = {}
	# TODO: More sanitization
	for attribute in required_attributes:
		if (attribute not in keys):
			return None
	if not (type(prod['image']) == werkzeug.datastructures.FileStorage):
		return None

	return prod

