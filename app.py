from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson import ObjectId
import jwt
import datetime
import requests

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://XXX:YYYY@cluster0.qqtvhqw.mongodb.net/?w=majority'
app.config['SECRET_KEY'] = '4c07817a2183e8a23436db279bfeb18ec3c37714'

mongo = PyMongo(app)

API_BASE_URL = 'https://www.alphavantage.co/query?'
DEFAULT_API_KEY = 'RRK65D0961Y9N5Q5'


# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username is already taken
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user document in the database
    user_id = mongo.db.users.insert_one({'username': username, 'password': password, 'watchlist': []}).inserted_id

    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201


# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username exists and the password matches
    user = mongo.db.users.find_one({'username': username, 'password': password})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate JWT token
    token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token}), 200


# Retrieve User's Watchlist
@app.route('/watchlist', methods=['GET'])
def get_watchlist():
    error = authenticate_token()
    if error:
        return error

    user_id = ObjectId(g.user['user_id'])
    watchlist = mongo.db.users.find_one({'_id': user_id}, {'_id': 0, 'watchlist': 1})
    if watchlist:
        return jsonify(watchlist['watchlist']), 200
    else:
        return jsonify([]), 200


# Update User's Watchlist
@app.route('/watchlist', methods=['POST'])
def update_watchlist():
    error = authenticate_token()
    if error:
        return error

    data = request.get_json()
    symbols = data.get('symbols')

    user_id = ObjectId(g.user['user_id'])
    # Update user's watchlist in the database
    mongo.db.users.update_one({'_id': user_id}, {'$set': {'watchlist': symbols}}, upsert=True)

    return jsonify({'message': 'Watchlist updated successfully'}), 200


# Fetch Stock Prices for User's Watchlist
@app.route('/dashboard', methods=['GET'])
def dashboard():
    error = authenticate_token()
    if error:
        return error

    user_id = ObjectId(g.user['user_id'])
    user = mongo.db.users.find_one({'_id': user_id}, {'_id': 0, 'watchlist': 1})
    if user:
        symbols = user['watchlist']
        stock_prices = {}

        for symbol in symbols:
            stock_price = get_stock_price(symbol)
            stock_prices[symbol] = stock_price

        return render_template('dashboard.html', stock_prices=stock_prices)
    else:
        return render_template('dashboard.html', stock_prices={})


def authenticate_token():
    token = request.headers.get('Authorization', '').split(' ')[1]
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        g.user = {'user_id': str(current_user['_id'])}
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    return None


def get_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': DEFAULT_API_KEY
    }
    response = requests.get(API_BASE_URL, params=params)
    data = response.json()
    stock_price = data.get('Time Series (1min)', {}).get('1. open')
    return stock_price


if __name__ == '__main__':
    app.run(debug=True)

def register_user():
    url = 'http://localhost:5000/register'
    data = {
        'username': 'myusername',
        'password': 'mypassword'
    }

    response = requests.post(url, json=data)
    print(response.json())


# Run the register_user function
register_user()


