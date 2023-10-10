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


@auth_bp.route('/signin-cherie')
def signin_cherie():
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
                print('ITEM ALREADY IN TABLE')
                flash(
                    'Email already registered. Please use another email or login.', 'error')
                return redirect(url_for('signin_cherie'))

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
            return redirect(url_for('signin_cherie'))

        except ClientError as e:
            flash(
                f"An error occurred: {e.response['Error']['Message']}", 'error')
            return render_template("pages/register.html")

        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", 'error')
            return render_template("pages/register.html")

    return render_template("pages/register.html")
