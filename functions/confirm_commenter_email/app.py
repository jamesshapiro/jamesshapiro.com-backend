import boto3
import json
import ulid

stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f'{event}=')
    # TODO base64 encode/decode the token for safety
    token = event['queryStringParameters']['token']
    token = token.replace(' ','+')
    decision = event['queryStringParameters']['decision']
    
    message = 'Comment successfully rejected!'
    if decision == 'confirm':
        message = 'Comment verified, now pending approval from James!'
    
    response = stepfunctions_client.send_task_success(
        taskToken=token,
        output=json.dumps({"comment_ulid": str(ulid.new()), "decision": decision})
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }