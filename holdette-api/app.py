from flask import Flask
from ConfigReader.Credentials import Credentials
app = Flask(__name__)
credentials = Credentials()

@app.route("/", methods=['GET'])
def main():
	stripe = credentials.get('stripe')
	return stripe['key']

if __name__ == '__main__':
	app.run()