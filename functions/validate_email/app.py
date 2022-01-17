import boto3

ses_client = boto3.client("ses")

def send_email(ses_client, commenter_email):
    charset = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                commenter_email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": charset,
                    "Data": "validation email",
                }
            },
            "Subject": {
                "Charset": charset,
                "Data": "validation email",
            },
        },
        Source="JS Comment Validator <jamesshapirocomments+athens@gmail.com>",
    )
    return response

def lambda_handler(event, context):
    print(f'{event=}')
    print(f'{context=}')
    if 'COMMENTER_EMAIL' in event:
        commenter_email = event['COMMENTER_EMAIL']
    response = send_email(ses_client, commenter_email)
    print(response)
    return