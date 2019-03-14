from flask import url_for, request
from flask_api import FlaskAPI, status, exceptions
from HoldetteCloudServices import Cloud

app = FlaskAPI(__name__)
cloud = Cloud()

@app.route("/register-consumer", methods=['POST'])
def registerConsumer():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
		state, errmsg = cloud.registerConsumer(data)

		if state == Cloud.ERROR:
			return {'Error': errmsg}, status.HTTP_400_BAD_REQUEST
		elif state == Cloud.USER_EXISTS:
			return {'Error':errmsg}, status.HTTP_200_OK
		return state, status.HTTP_200_OK

@app.route("/", methods=['GET'])
def main():
	return "Hello WOrld"

if __name__ == '__main__':
	app.run()