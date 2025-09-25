import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()

def send_email_via_sendgid_api(
    recipients: list[str], subject: str, message: str, message_type: str
):
    if message_type == "info":
        sending_email = os.getenv("INFO_EMAIL")
    else:
        raise NameError(f"No such message_type --> {message_type}")

    mail = Mail(
        Email(sending_email),
        To(recipients[0]),
        subject,
        Content("text/html", message),
    )

    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SG_API_EMAIL_KEY"))
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        print(
            f"=====Completed Sendgrid API email send\n==== status: {response.status_code}\n==== message-id: {response.headers['X-Message-Id']}"
        )
    except Exception as e:
        raise InterruptedError({"message": e})