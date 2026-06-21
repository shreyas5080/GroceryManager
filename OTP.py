import smtplib
import os
import secrets
import time

from dotenv import load_dotenv
from email.message import EmailMessage
<<<<<<< HEAD
from database import insert_in_otp
from datetime import datetime
=======
from database import delete_otp, insert_in_otp
>>>>>>> 7bc9a78eebc3698f2ceff81413330f9acafe852a


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
<<<<<<< HEAD
    email = os.getenv("email")
    password = os.getenv("email_password")
=======

    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if not email or not password:
        raise ValueError("Email credentials are not configured in .env")
>>>>>>> 7bc9a78eebc3698f2ceff81413330f9acafe852a

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)

    message = EmailMessage()

    message["Subject"] = "Your OTP"
    message["Fom"] = email

<<<<<<< HEAD
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    
    message.set_content(f"Your OTP is: {otp}")

    insert_in_otp(user_email, otp)
    server.send_message(message)

    current_time = time.time()
    dt = datetime.fromtimestamp(current_time)

    minute = dt.minute

    return otp, minute
=======
    
    message["To"] = user_email
    if type(user_otp) is int:
        message.set_content(f"Your OTP is: {user_otp}")

        server.send_message(message)

        server.quit()
>>>>>>> 7bc9a78eebc3698f2ceff81413330f9acafe852a

    else:
        server.quit()
