import boto3
import json

stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f'{event}=')
    # TODO base64 encode/decode the token for safety
    token = event['queryStringParameters']['token']
    token = token.replace(' ','+')
    decision = event['queryStringParameters']['decision']

    message = 'Comment rejected by moderator.'
    if decision == 'confirm':
        message = 'Comment approved by moderator'

    response = stepfunctions_client.send_task_success(
        taskToken=token,
        output=json.dumps({"decision": decision})
    )
    print(response)
    return {
        'statusCode': 200,
        'body': message
    }