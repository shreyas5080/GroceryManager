import smtplib
import os
import secrets
import time

from dotenv import load_dotenv
from email.message import EmailMessage
from database import insert_in_otp, get_otp, delete_otp


def user_otp(user_email):
    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if not email or not password:
        raise ValueError("Email credentials are not configured in .env")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    message = EmailMessage()
    message["Subject"] = "Your OTP"
    message["From"] = email
    message["To"] = user_email

    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    insert_in_otp(user_email, otp)

    message.set_content(f"Your OTP is: {otp}")
    server.send_message(message)
    server.quit()

    return otp


def verify_otp(user_email, entered_otp):
    otp_data = get_otp(user_email)
    if not otp_data:
        return "Wrong OTP"

    stored_otp = otp_data[0]
    if stored_otp == entered_otp:
        delete_otp(user_email)
        return True

    return "Wrong OTP"

    