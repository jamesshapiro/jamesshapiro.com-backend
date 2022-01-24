import boto3
import os

ses_client = boto3.client("ses")
dynamodb_client = boto3.client("dynamodb")

confirm_comment_endpoint = os.environ['CONFIRMATION_ENDPOINT']
unsubscribe_endpoint = os.environ['CONFIRMATION_ENDPOINT']

def send_email(ses_client, commenter_email, comment_validator_email, comment_text, token, my_ulid):
    token = token.replace('+','%2B')
    charset = "UTF-8"
    html_email_content = f"""
        <html>
            <head></head>
            <h3>Do you want to submit this comment?</h3>
            <p>Comment: {comment_text}</p>
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
                "Data": f"Validate JS Comment: {my_ulid[-6:]}",
            },
        },
        Source=f"JS Comments <{comment_validator_email}>",
    )
    return response

def lambda_handler(event, context):
    commenter_email = event['commenter_email']
    comment_validator_email = event['comment_validator_email']
    comment_text = event['comment_text']
    token = event['token']
    my_ulid = event['ulid']
    response = send_email(ses_client, commenter_email, comment_validator_email, comment_text, token, my_ulid)
    print(response)
    return {
        "post_id": "TEST_POST_ID",
        "comment_text": comment_text,
        "commenter_email": commenter_email,
        "commenter_approved": "false",
        "moderator_approved": "false"
    }