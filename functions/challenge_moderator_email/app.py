import boto3
import os

ses_client = boto3.client("ses")

confirm_comment_endpoint = os.environ['CONFIRMATION_ENDPOINT']

def send_email(ses_client, commenter_email, comment_validator_email, moderator_email, comment_text, token, my_ulid):
    token = token.replace('+','%2B')
    charset = "UTF-8"
    html_email_content = f"""
        <html>
            <head></head>
            <h3>Do you want to approve this comment?</h3>
            <p>By: {commenter_email}</p>
            <p>Comment: {comment_text}</p>
            <p><a href="{confirm_comment_endpoint}?token={token}&decision=confirm">CONFIRM</a> or <a href="{confirm_comment_endpoint}?token={token}&decision=deny">DENY</a></p>
            </body>
        </html>"""
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                moderator_email,
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
                "Data": f"Moderate JS Comment: {my_ulid[-6:]}",
            },
        },
        Source=f"JS Comments <{comment_validator_email}>",
    )
    return response

def lambda_handler(event, context):
    commenter_email = event['commenter_email']
    comment_validator_email = event['comment_validator_email']
    moderator_email = event['moderator_email']
    comment_text = event['comment_text']
    my_ulid = event['ulid']
    token = event['token']
    response = send_email(ses_client, commenter_email, comment_validator_email, moderator_email, comment_text, token, my_ulid)
    print(response)
    return