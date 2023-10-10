import boto3

# Get  service resource
import key_config as keys

dynamodb = boto3.resource('dynamodb',
                          region_name=keys.AWS_DEFAULT_REGION,
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          )

# Create DynamoDB table
table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
              'AttributeName': 'username',  # Use 'username' as the primary key
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',  # Define 'username' as an attribute
            'AttributeType': 'S'  # 'S' denotes a String data type
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until table exists
table.meta.client.get_waiter('table_exists').wait(TableName='users')


print(table.item_count)
