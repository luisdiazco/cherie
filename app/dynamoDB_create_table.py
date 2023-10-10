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
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'  # 'S' denotes a String. This will be a UUID.
        },
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'EmailIndex',
            'KeySchema': [
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        }
    ]
)

# Wait until table exists
table.meta.client.get_waiter('table_exists').wait(TableName='users')


print(table.item_count)
