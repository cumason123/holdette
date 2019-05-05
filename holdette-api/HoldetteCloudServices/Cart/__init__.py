class Cart():
	def __init__(self):
		self.products = {}

	def addProduct(self, product):
		keys = self.products.keys()
		pid = product['pid']
		stock = self.inStock(pid)

		if pid not in keys:
			if (stock):
				self.products[pid] = {
					'product': product,
					'quantity':1
				}
			else:
				raise ValueError('Out of stock') # Out of stock
		else:
			quantity = self.products[pid]['quantity']
			if stock - quantity > -1:
				self.products[pid]['quantity'] += 1
			else:
				raise ValueError('Out of stock')

	def stockQuantity(self, pid)
		raise NotImplementedError()

	def 
