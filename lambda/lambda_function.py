import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('todos')

def lambda_handler(event, context):
    method = event['httpMethod']
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    if method == 'GET':
        response = table.scan()
        todos = response.get('Items', [])
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(todos)
        }

    elif method == 'POST':
        body = json.loads(event['body'])
        todo = {
            'id': str(uuid.uuid4()),
            'text': body['text'],
            'completed': False,
            'createdAt': datetime.utcnow().isoformat()
        }
        table.put_item(Item=todo)
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps(todo)
        }

    elif method == 'PUT':
        body = json.loads(event['body'])
        todo_id = body['id']
        completed = body['completed']
        table.update_item(
            Key={'id': todo_id},
            UpdateExpression='SET completed = :c',
            ExpressionAttributeValues={':c': completed}
        )
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Updated'})
        }

    elif method == 'DELETE':
        body = json.loads(event['body'])
        table.delete_item(Key={'id': body['id']})
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Deleted'})
        }

    return {
        'statusCode': 400,
        'headers': headers,
        'body': json.dumps({'message': 'Invalid request'})
    }