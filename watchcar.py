from flask import Flask, redirect, request, jsonify, render_template
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
global vehicle
global code


client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info', 'read_location', 'read_odometer', 'control_security'],
    test_mode=True
)


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    global code
    code = request.args.get('code')
    # code = '11b7c847-b877-4632-82f0-a0598b35417b'
    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return redirect('/vehicle')


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    global vehicle

    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    resp = vehicle.info()

    # resp.update(vehicle.odometer())
    # resp['data']['location'] = (vehicle.location())
    return render_template('info.html', data=str(resp))


@app.route('/locker', methods=['POST'])
def locker():
    global access
    global vehicle
    lock = request.form['lock']
    mystring = '55'
    try:
        # vehicle_ids = smartcar.get_vehicle_ids(
        #     access['access_token'])['vehicles']

        # instantiate the first vehicle in the vehicle id list
        # vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
        vehicle.odometer()
    except Exception as e :
        mystring = str(e)
    # vehicle.lock()
    # my_res = ''
    # if lock == '1':
    #     my_res = vehicle.lock()
    # else:
    #     my_res = vehicle.unlock()
    return mystring
    # return 'script'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
