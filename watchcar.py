from flask import Flask, redirect, request, jsonify
import smartcar
from flask_cors import CORS
import os

os.environ["CLIENT_ID"] = "98c99428-1311-4bf6-b49c-9138cb2e2d8f"
os.environ["CLIENT_SECRET"] = "4108367c-d570-45c0-980a-d7bda65df183"
os.environ["REDIRECT_URI"] = "https://watchcarapp.com/exchange"


app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info','read_location'],
    test_mode=True
)


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    # resp = dict(vehicle.info() + vehicle.location())
    #
    # print(resp)

    return jsonify(vehicle.info())


if __name__ == "__main__":
    app.run(host='0.0.0.0')