import boto3

# Get  service resource
import key_config as keys

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )

# Create DynamoDB table
dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )

# Create DynamoDB table for products
products_table = dynamodb.create_table(
    TableName='products',
    KeySchema=[
        {
            'AttributeName': 'product_id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'product_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the products table exists
products_table.meta.client.get_waiter(
    'table_exists').wait(TableName='products')

print(products_table.item_count)
