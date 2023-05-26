# stock-monitoring-platform
The code starts by importing the necessary modules and libraries: Flask, request, jsonify, render_template, PyMongo, ObjectId, jwt, datetime, and requests.

The Flask application is created using app = Flask(__name__).

The MongoDB connection URI and the secret key for JWT token encoding are set in the application's configuration using app.config['MONGO_URI'] and app.config['SECRET_KEY'].

An instance of PyMongo is created using mongo = PyMongo(app) to establish a connection with the MongoDB database.

The base URL for the Alpha Vantage API and the default API key are defined.

The /register endpoint is defined as a route using @app.route('/register', methods=['POST']). Inside the route function, the user registration logic is implemented. It checks if the provided username already exists, creates a new user document in the MongoDB database, and returns a response with the registered user's details.

The /login endpoint is defined as a route using @app.route('/login', methods=['POST']). Inside the route function, the user login logic is implemented. It checks the provided username and password, generates a JWT token using the secret key, and returns the token in the response.

The /watchlist endpoint is defined as a route using @app.route('/watchlist', methods=['GET']). It allows users to retrieve their watchlist of stock symbols. The route function checks the authenticity of the JWT token, retrieves the user's watchlist from the database, and returns it as a JSON response.

The /watchlist endpoint is also defined as a route using @app.route('/watchlist', methods=['POST']). It allows users to update their watchlist of stock symbols. The route function checks the authenticity of the JWT token, retrieves the symbols from the request JSON data, and updates the user's watchlist in the database.

The /dashboard endpoint is defined as a route using @app.route('/dashboard', methods=['GET']). It displays the dashboard with the latest stock prices for the symbols in the user's watchlist. The route function checks the authenticity of the JWT token, retrieves the user's watchlist from the database, fetches the stock prices using the Alpha Vantage API, and renders the dashboard.html template with the stock prices as the context.

The authenticate_token() function is defined to authenticate the JWT token. It checks the token from the request headers, decodes it using the secret key, retrieves the current user's details from the database, and stores the user ID in the g object for later use.

The get_stock_price() function is defined to fetch the latest stock price for a given symbol using the Alpha Vantage API. It sends a GET request to the API, retrieves the JSON response, and extracts the stock price from the response data.

The last part of the code checks if the script is being run directly (if __name__ == '__main__':). If so, it starts the Flask application with debug mode enabled using app.run(debug=True).

The register_user() function is defined to demonstrate how to register a user by sending a POST request to the /register endpoint using the requests library. It sets the URL, data (username and password), sends the request, and prints the response JSON.

To run the code and test the functionality, make sure you have MongoDB installed and running. Install the required dependencies (Flask, Flask-PyMongo, and requests). Then, execute the script, and it will start the Flask application on http://localhost:5000.

You can test the functionality using tools like curl, Postman, or by making HTTP requests from your code. For example, you can call the register_user() function to register a user, and then proceed with other operations like login, updating watchlist, and accessing the dashboard.
