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

		# Append image to data
		# npimg = np.fromfile(request.files['image'], np.uint8)
		# data['image'] = cv2.imdecode(npimg, cv2,COLOR_BGR2RGB)
		data['image'] = request.files['image']
		print(type(data['image']))
		# state, result = cloud.designerUploadProduct(data)
		return '200'

if __name__ == '__main__':
	app.run()