import boto3
import json

stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print(f'{event}=')
    # TODO base64 encode/decode the token for safety
    token = event['queryStringParameters']['token']
    token = token.replace(' ','+')
    decision = event['queryStringParameters']['decision']

    if decision == 'confirm':
        response = stepfunctions_client.send_task_success(
            taskToken=token,
            output=json.dumps({"success": "success"})
        )
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps('Comment verified, now pending approval from James!')
        }
    else:
        response = stepfunctions_client.send_task_failure(
            taskToken=token,
            error='User Rejected Comment',
            cause='User Rejected Comment'
        )
        print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Comment successfully rejected!')
    }