import smtplib
import os
import secrets
import time

from flask import request
from dotenv import load_dotenv
from email.message import EmailMessage
from GroceryManWebsite import email_for_otp

def user_otp():
    load_dotenv()

    email = os.getenv("EMAIL")
    password = os.getenv("DB_PASSWORD")
    otp = ''.join(
        str(secrets.rangebelow(10) for _ in range(6))
        )

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls
    server.login(email, password)
    
    message = EmailMessage()

    message["Subject"] = "Your OTP"
    message["Fom"] = email

    
    message["To"] = email_for_otp

    message.set_content(f"Your OTP is: {otp}")

    server.send_message(message)

    server.quit()

    return otp


def expiration_time():
    

    otp_code = user_otp

            