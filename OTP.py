import smtplib
import os
import secrets
import time

from dotenv import load_dotenv
from email.message import EmailMessage
from database import insert_in_otp


def user_otp(user_email):

    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("DB_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls
    server.login(email, password)
    
    message = EmailMessage()
    message["Subject"] = "Your OTP"
    message["Fom"] = email
    message["To"] = user_email

    otp = ''.join(
        str(secrets.rangebelow(10) for _ in range(6))
        )
        
    insert_in_otp(user_email, otp)
    
    message.set_content(f"Your OTP is: {user_otp}")
    server.send_message(message)

    current_time = time.time()

    return otp, current_time

    