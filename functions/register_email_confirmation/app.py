import boto3
import os

ses_client = boto3.client("ses")

confirm_comment_endpoint = os.environ['CONFIRM_COMMENT_ENDPOINT']

def send_email(ses_client, commenter_email, token):
    charset = "UTF-8"
    html_email_content = f"""
        <html>
            <head></head>
            <h1 style='text-align:center'>This is the heading</h1>
            <p>Hello, world</p>
            <p>Please click <a href="{confirm_comment_endpoint}?token={token}">here</a>
            </body>
        </html>"""
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                commenter_email,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": charset,
                    "Data": html_email_content,
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
    commenter_email = event['commenter_email']
    token = event['token']
    response = send_email(ses_client, commenter_email, token)
    print(response)
    return