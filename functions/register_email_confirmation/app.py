import boto3
import os
import json

stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f'{event}=')
    token = event['queryStringParameters']['token']
    token = token.replace(' ','+')

    print(f'{token[:100]=}')

    response = stepfunctions_client.send_task_success(
        taskToken=token,
        output=json.dumps({"success": "success"})
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Comment verified, now pending approval from James!')
    }