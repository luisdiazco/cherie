from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from flask import Blueprint, flash, render_template, redirect, url_for, request
from botocore.exceptions import ClientError
import app.key_config as keys
import boto3
import logging

logging.basicConfig(level=logging.DEBUG)

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
login_bp = Blueprint("login", __name__)


@login_bp.route('/')
def login():
    return render_template("pages/signin_cherie.html")


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    print("HELLO")
    if request.method == 'POST':
        print("IN POST METHOD")
        user_id = str(uuid4())
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('users')

        try:

            # Check if user with this email already exists
            response = table.query(
                IndexName='EmailIndex',
                KeyConditionExpression=Key('email').eq(email)
            )
            if response.get('Items'):

                flash(
                    'Email already registered. Please use another email or login.', 'error')
                return redirect(url_for('auth.signin_cherie'))

            # @TODO: set up hashing
            response = table.put_item(
                Item={
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'password': password
                }
            )
            print("PRINTING RESPONSE: ", response)
            flash('Registration Complete. Please login to your account!', 'success')
            # assuming you have a 'login' route
            return redirect(url_for('auth.login'))

        except ClientError as e:
            flash(
                f"An error occurred: {e.response['Error']['Message']}", 'error')
            return render_template("pages/register.html")

        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", 'error')
            return render_template("pages/register.html")

    return render_template("pages/register.html")


@auth_bp.route('/auth', methods=['POST'])
def authentication():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('users')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )

        items = response['Items']
        username = items[0]['username']
        if password == items[0]['password']:
            return render_template("home.tml", username=username)
    return render_template('pages/signin_cherie.html')
