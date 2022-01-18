import boto3
import os

ses_client = boto3.client("ses")

confirm_comment_endpoint = os.environ['CONFIRM_COMMENT_ENDPOINT']
deny_comment_endpoint = os.environ['CONFIRM_COMMENT_ENDPOINT']
unsubscribe_endpoint = os.environ['CONFIRM_COMMENT_ENDPOINT']

def send_email(ses_client, commenter_email, comment, token):
    charset = "UTF-8"
    html_email_content = f"""
        <html>
            <head></head>
            <h3>Do you want to submit this comment?</h3>
            <p>Comment: {comment}</p>
            <p><a href="{confirm_comment_endpoint}?token={token}">CONFIRM</a> or <a href="{confirm_comment_endpoint}?token={token}">DENY</a></p>
            <p>or</p>
            <p><a href="{unsubscribe_endpoint}">Unsubscribe Forever</p>
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
                "Data": "jamesshapiro.com Comment Validation",
            },
        },
        Source="JS Comment Validator <jamesshapirocomments+athens@gmail.com>",
    )
    return response

def lambda_handler(event, context):
    commenter_email = event['commenter_email']
    comment = event['comment']
    token = event['token']
    response = send_email(ses_client, commenter_email, comment, token)
    print(response)
    return