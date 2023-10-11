from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from flask import Blueprint, flash, render_template, redirect, url_for, request, session

import app.key_config as keys
import boto3
import logging
import bcrypt
import base64

logging.basicConfig(level=logging.DEBUG)

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )


auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/')
def login():
    return render_template("pages/signin_cherie.html")


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        if not isinstance(password, str):
            password = str(password)

        table = dynamodb.Table('users')

        # check if username already exists
        username_response = table.query(
            KeyConditionExpression=Key('username').eq(username)
        )

        # check if email already exists
        email_response = table.scan(
            FilterExpression=Attr('email').eq(email)
        )

        if username_response.get('Items'):
            flash('Username already taken. Please choose another username.', 'error')
            return redirect(url_for('auth.register'))

        if email_response.get('Items'):
            flash('Email already registered. Please use another email or login.', 'error')
            return redirect(url_for('auth.register'))

        # Hash the password using Flask-Bcrypt
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Add the new user to the table
        response = table.put_item(
            Item={
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': hashed_pw
            }
        )

        flash('Registration Complete. Please login to your account!', 'success')
        return redirect(url_for('auth.login'))

    return render_template("pages/register.html")


@auth_bp.route('/auth', methods=['POST'])
def authentication():
    if request.method == 'POST':
        # This could be email or username
        identifier = request.form['login']
        password = request.form['password']

        table = dynamodb.Table('users')

        # Use scan operation to filter by email or username
        response = table.scan(
            FilterExpression=(Attr('email').eq(identifier)) | (
                Attr('username').eq(identifier))
        )

        if response['Items']:
            user = response['Items'][0]

            # Decode the password attribute from Binary to bytes
            stored_password_bytes = user['password'].value
            stored_password = stored_password_bytes.decode('utf-8')

            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # Store user info in session
                session['username'] = user['username']
                session['email'] = user['email']
                # Redirect to the user's home page with their username
                return redirect(url_for('web.home', username=user['username']))

        flash('Invalid login credentials. Please try again.', 'error')

    return render_template('pages/signin_cherie.html')
