from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from uuid import uuid4
from flask import Blueprint, flash, render_template, redirect, url_for, request, session
import app.key_config as keys
import boto3
import logging

home_bp = Blueprint("web", __name__)

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )


s3 = boto3.client('s3',
                  aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                  region_name=keys.AWS_DEFAULT_REGION)


@home_bp.route('/home/<username>')
def home(username):
    user_has_listings = has_listings(username)
    return render_template("pages/home.html", username=username, has_listings=user_has_listings)


@home_bp.route('/listings/<username>')
def listings(username):
    products = get_user_products(username)
    return render_template("pages/listings.html", username=username, products=products)


@home_bp.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        # Retrieve form data
        description = request.form['description']
        category = request.form['category']
        condition = request.form['condition']
        size = request.form['size']
        free_shipping = 'free_shipping' in request.form
        price = request.form['price']

        # Generate a unique product ID using uuid
        product_id = str(uuid4())

        table = dynamodb.Table('products')

        # Ensure the user is logged in (session contains username)
        if 'username' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('auth.login'))

        # Add the new product to the table
        try:
            table.put_item(
                Item={
                    'product_id': product_id,
                    'username': session['username'],
                    'description': description,
                    'category': category,
                    'condition': condition,
                    'size': size,
                    'free_shipping': free_shipping,
                    'price': price,
                }
            )
            flash('Item listed successfully!', 'success')
            return redirect(url_for('web.home', username=session['username']))
        except ClientError as e:
            logging.error(e)
            flash('Error listing item. Please try again later.', 'error')
            return render_template("pages/create_listing.html")

    return render_template("pages/create_listing.html")


@home_bp.route('/about')
def about():
    return render_template("pages/about.html")


def has_listings(username):
    table = dynamodb.Table('products')

    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    # Check if any items were returned
    return 'Items' in response and len(response['Items']) > 0


def get_user_products(username):
    table = dynamodb.Table('products')

    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    # Return the items if they exist; otherwise, return an empty list
    return response.get('Items', [])
