from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from uuid import uuid4
from flask import Blueprint, flash, render_template, redirect, url_for, request, session, jsonify
import app.key_config as keys
import boto3
import logging
from app.s3_upload import upload_to_s3

home_bp = Blueprint("web", __name__)

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )


@home_bp.route('/home/<username>')
def home(username):
    user_has_listings = has_listings(username)
    return render_template("pages/home.html", username=username, has_listings=user_has_listings)


@home_bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user's session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


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

        # Ensure the user is logged in
        if 'username' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('auth.login'))

        # Process and upload images to S3
        uploaded_image_urls = []
        for file in request.files.getlist('photos'):
            if file.filename:
                # Upload the image to S3
                upload_result = upload_to_s3(
                    file, 'your-s3-bucket', session['username'], product_id)
                if upload_result:
                    uploaded_image_urls.append(upload_result['url'])

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
                    'images': uploaded_image_urls  # Store the image URLs in DynamoDB
                }
            )
            flash('Item listed successfully!', 'success')
            products = get_user_products(session['username'])
            return render_template("pages/listings.html", username=session['username'], products=products)
        except ClientError as e:
            logging.error(e)
            flash('Error listing item. Please try again later.', 'error')
            return render_template("pages/create_listing.html")

    return render_template("pages/create_listing.html")


@home_bp.route('/listings/<username>')
def listings(username):
    if 'username' not in session or session['username'] != username:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('auth.login'))

    products = get_user_products(username)
    return render_template("pages/listings.html", username=username, products=products)


@home_bp.route('/update_listing/<product_id>', methods=['POST'])
def update_listing(product_id):

    # Retrieve the form data
    edit_description = request.form['edit-description']
    edit_category = request.form['edit-category']
    edit_condition = request.form['edit-condition']
    edit_free_shipping = request.form.get('edit-free-shipping') == 'on'
    edit_size = request.form['edit-size']
    edit_price = int(request.form['edit-price'])

    # Get the DynamoDB table
    table = dynamodb.Table('products')

    # Update the item in the table
    try:
        response = table.update_item(
            Key={
                'product_id': product_id
            },
            # Include #sz for size
            UpdateExpression="set #desc = :desc, #cat = :cat, #cond = :cond, #ship = :ship, #sz = :size, #prc = :price",
            ExpressionAttributeNames={
                "#desc": "description",
                "#cat": "category",
                "#cond": "condition",
                "#ship": "free_shipping",
                "#sz": "size",
                "#prc": "price"
            },
            ExpressionAttributeValues={
                ':desc': edit_description,
                ':cat': edit_category,
                ':cond': edit_condition,
                ':ship': edit_free_shipping,
                ':size': edit_size,
                ':price': edit_price
            },
            ReturnValues="ALL_NEW"
        )

        flash('Listing updated successfully!', 'success')
        return redirect(url_for('web.listings', username=session['username']))
    except ClientError as e:
        print(f"Error: {e}")
        flash('Error updating listing. Please try again later.', 'error')
        return redirect(url_for('web.listings', username=session['username']))

# Create a route to delete a listing


@home_bp.route('/delete_listing/<string:product_id>', methods=['POST'])
def delete_listing(product_id):
    try:
        # Delete the listing from DynamoDB
        table = dynamodb.Table('products')
        response = table.delete_item(
            Key={'product_id': product_id}
        )

        # Check if the delete request was successful
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Error deleting listing'})

    except ClientError as e:
        return jsonify({'success': False, 'message': 'Error deleting listing'})

    return jsonify({'success': False, 'message': 'Unknown error'})


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


def get_user_products(username):
    table = dynamodb.Table('products')

    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    # Return the items if they exist; otherwise, return an empty list
    return response.get('Items', [])
