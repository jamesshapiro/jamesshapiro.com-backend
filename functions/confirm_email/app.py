import boto3
import json

stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f'{event}=')
    # TODO base64 encode/decode the token for safety
    token = event['queryStringParameters']['token']
    token = token.replace(' ','+')

    response = stepfunctions_client.send_task_success(
        taskToken=token,
        output=json.dumps({"success": "success"})
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Comment verified, now pending approval from James!')
    }