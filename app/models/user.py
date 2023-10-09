from flask import Flask, request, jsonify
import uuid  # For generating user IDs

app = Flask(__name__)

# Simulated database (you should replace this with your database setup)
users_db = {}


@app.route('/register', methods=['POST'])
def register_user():
    # Extract user registration data from the request
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the username or email is already registered
    if username in users_db or email in users_db.values():
        return jsonify({'error': 'Username or email already exists'}), 400

    # Generate a unique user ID (you may use a library like uuid or a database-generated ID)
    user_id = str(uuid.uuid4())

    # Store user data in the database
    users_db[user_id] = {
        'username': username,
        'email': email,
        'password': password  # In a real app, you should hash the password
    }

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201


if __name__ == '__main__':
    app.run(debug=True)
