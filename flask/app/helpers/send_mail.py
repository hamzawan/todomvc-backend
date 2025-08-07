from flask import current_app
from flask_mail import Message


def send_verification_email(to_email, verification_link):
    mail = current_app.mail
    msg = Message(
        subject="Verify Your Email Address",
        recipients=[to_email],
        body=f"Please verify your email by clicking the link: {verification_link}",
        html=f"<p>Please verify your email by clicking the link:</p><a href='{verification_link}'>Verify Email</a>"
    )
    mail.send(msg)
    print(f"{msg} --- Sending email to {to_email} with link {verification_link}")
    