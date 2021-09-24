from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import DynamicTemplateData, Mail

from ..config.settings import settings
from ..schemas.userSchema import User

sg = SendGridAPIClient(settings.sendgrid_key)
SENDER_EMAIL = "emekaallison4@gmail.com"


async def send_email(
    recipient: User, message: str, subject: str, action: str = None, url: str = None
):
    msg = Mail(
        from_email=(SENDER_EMAIL, "BizzBuzz Notification"),
        to_emails=recipient.email,
        subject=subject,
    )

    msg.template_id = "d-0a5bc2da6d9d41fdb734d78525c9e20e"

    message_action = action or "Continue to BizzBuzz"
    message_url = url or "https://bizzbuzz.com"

    msg.dynamic_template_data = {
        "name": recipient.first_name,
        "message": message,
        "action": message_action,
        "url": message_url,
    }

    try:
        response = sg.send(msg)
    except Exception as e:
        print(e)
