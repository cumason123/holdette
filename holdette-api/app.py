from flask import url_for, request
from flask_api import FlaskAPI, status, exceptions
from HoldetteCloudServices import Cloud

app = FlaskAPI(__name__)
cloud = Cloud()

@app.route("/register/consumers", methods=['POST'])
def registerConsumer():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, errmsg = cloud.consumerRegister(data)

		if state == Cloud.error.ERROR:
			return {'Error': errmsg}, status.HTTP_400_BAD_REQUEST

		elif state == Cloud.error.USER_EXISTS:
			return {'Error':errmsg}, status.HTTP_200_OK
			
		return state, status.HTTP_200_OK

@app.route("/register/designers", methods=['POST'])
def registerDesigner():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, errmsg = cloud.designerRegister(data)

		if state == Cloud.error.ERROR:
			return {'Error': errmsg}, status.HTTP_400_BAD_REQUEST

		elif state == Cloud.error.USER_EXISTS:
			return {'Error':errmsg}, status.HTTP_200_OK
			
		return state, status.HTTP_200_OK

@app.route("/login", methods=['POST'])
def loginConsumer():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, errmsg = cloud.consumerLogin(data)

		if state == Cloud.error.INVALID_CREDENTIALS:
			return {'Error': 'Unknown username or password'}, status.HTTP_200_OK
		elif state == Cloud.error.ERROR:
			return {'Error': errmsg}, status.HTTP_400_BAD_REQUEST
		else:
			return state, status.HTTP_200_OK

@app.route("/", methods=['GET'])
def main():
	return "Hello WOrld"

if __name__ == '__main__':
	app.run('0.0.0.0')