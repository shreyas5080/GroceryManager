import smtplib
import os
import secrets
import time

from dotenv import load_dotenv
from email.message import EmailMessage
from database import insert_in_otp
from datetime import datetime

def sending_otp(user_email):
    load_dotenv()
    email = os.getenv("email")
    password = os.getenv("email_password")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    message = EmailMessage()

    message["Subject"] = "Your OTP"
    message["Fom"] = email

    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    
    message.set_content(f"Your OTP is: {otp}")

    insert_in_otp(user_email, otp)
    server.send_message(message)
    current_time = time.time()
    server.quit()

    dt = datetime.fromtimestamp(current_time)

    minute = dt.minute

    return otp, minute