import smtplib
import os
import secrets
import time

from dotenv import load_dotenv
from email.message import EmailMessage
from database import delete_otp, insert_in_otp


def user_otp(user_email):

    otp_dict = {'otp': ''.join(
        str(secrets.rangebelow(10) for _ in range(6))
        ),
        'time': time.time()
        }
    insert_in_otp(user_email, otp_dict['otp'])
    current_time = time.time()
    
    if current_time - otp_dict["time"] > 300:
        delete_otp(user_email)
        return 'Time Expired'

    elif otp_dict["otp"] == user_otp:
        return int(otp_dict['otp'])

    else:
        return "Wrong OTP"
    

def sending_otp(user_email):
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
    if type(user_otp) is int:
        message.set_content(f"Your OTP is: {user_otp}")

        server.send_message(message)

        server.quit()

    else:
        server.quit()
