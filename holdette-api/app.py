from flask import url_for, request
from flask_api import FlaskAPI, status, exceptions
from HoldetteCloudServices import Cloud
import cv2
import io
import numpy as np
app = FlaskAPI(__name__)
cloud = Cloud()

@app.route("/register/consumers", methods=['POST'])
def registerConsumer():
	"""
	Endpoint registers consumer users
	"""
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, result = cloud.consumerRegister(data)

		if state == Cloud.error.SUCCESS:
			return result, status.HTTP_200_OK

		elif state == Cloud.error.ERROR:
			return {'Error': result}, status.HTTP_400_BAD_REQUEST

		elif state == Cloud.error.USER_EXISTS:
			return {'Error':result}, status.HTTP_200_OK

		else:
			return state, status.HTTP_400_BAD_REQUEST
			
		return result, status.HTTP_200_OK

@app.route("/register/designers", methods=['POST'])
def registerDesigner():
	"""
	Endpoint registers designer users
	"""
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, result = cloud.designerRegister(data)

		if state == Cloud.error.SUCCESS:
			return result, status.HTTP_200_OK

		elif state == Cloud.error.ERROR:
			return {'Error': result}, status.HTTP_400_BAD_REQUEST

		elif state == Cloud.error.USER_EXISTS:
			return {'Error':result}, status.HTTP_200_OK
		
		else:
			return result, status.HTTP_400_BAD_REQUEST

@app.route("/login", methods=['POST'])
def loginConsumer():
	"""
	Endpoint signs in consumers

	:param username: key for the username of this consumer
	:param password: key for the password of this consumer
	:returns: dict containing the access-token which expires after 1 hour
	"""
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, result = cloud.consumerLogin(data)

		if state == Cloud.error.SUCCESS:
			return result, status.HTTP_200_OK

		if state == Cloud.error.INVALID_CREDENTIALS:
			return {'Error': 'Unknown username or password'}, status.HTTP_200_OK

		elif state == Cloud.error.ERROR:
			return {'Error': result}, status.HTTP_400_BAD_REQUEST

		else:
			return result, status.HTTP_400_BAD_REQUEST

@app.route("/upload-product", methods=['POST'])
def uploadProduct():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)

		
		data['image'] = request.files['image']
		state, result = cloud.designerUploadProduct(data)
		return '200'

if __name__ == '__main__':
	# username = input('Please give username')
	# password = input('Please give password')
	# cloud.setCreds(username, password)
	app.run()