import time

from flask import Flask, render_template, request, url_for, redirect,session, flash
from datetime import timedelta
from datetime import datetime

from  database import insert, get_results, insert_in_users, get_email, get_password, get_name, delete_otp
from OTP import sending_otp
from functools import wraps


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(seconds=30)
app.secret_key = "wearetheworld"

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "email" not in session:
            flash("Please login first", "error")
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "email" not in session:
            flash("Please Login")
            return redirect(url_for("login"))
            
        return f(*args, **kwargs)

    return decorated
    

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("homepage.html")


@app.route("/result")
@login_required
def print_groceries():
    if "email" in session:
        email = session["email"]

        result = get_results(email)
        return render_template("print_grocery.html", results=result)
    else:

        return render_template("operations.html")


@app.route("/add", methods=["POST", "GET"])
@login_required
def add():
    if "email" in session:
        if request.method == "POST":

            item_name = request.form["item_name"]
            item_quantity = request.form["item_quantity"]

            email = session["email"]
            int_quantity = int(item_quantity)
            insert(item_name, int_quantity, email)

            return redirect(url_for('print_groceries'))
        else:
            return render_template("operations.html")
    else:

        return render_template("homepage.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db_results = get_email(email)
        db_pass_res = get_password(email)

        session["email"] = email
        session["password"] = password

        if db_results is None:
            flash("Email not found")

        else:
            if password == db_pass_res[0]:
                return redirect(url_for('the_user'))
            else:
                flash("Password incorrect")

    else:
        if "email" in session:
            email = session["email"]
            get_user = get_name(email)
            return redirect(url_for("the_user", user_name=get_user))

    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        email = request.form["email"]    
        exiting_email = get_email(email)

        if exiting_email:

            flash("This email is already used")
            return redirect(url_for("register"))

        else:  
            session['user_fname'] = request.form["fname"]
            session['user_lname'] = request.form["lname"]
            session['email'] = email
            session[' password'] = request.form["password"]

            returned_function = sending_otp(email)
            session['otp'] = returned_function[0]
            session['time'] = returned_function[1]

            
            return redirect(url_for('verifying_otp'))
                            

    else:
        if "email" in session:
            return redirect(url_for("the_user"))

        return render_template("register.html")

@app.route('/otp-verification', methods=["POST", "GET"])
def verifying_otp():
    
    if request.method == "POST":

        us_otp = request.form["user_otp"]
        
        returned_otp = session.get('otp')
        otp_time = session.get('time')

        current_time = time.time()
        dt = datetime.fromtimestamp(current_time)
        
        the_minute = dt.minute
        less_than_five = the_minute - otp_time 

        if less_than_five < 5 and us_otp == returned_otp:
            
            fname = session.get('user_fname')
            lname = session.get('user_lname')
            email = session.get('email')
            password = session.get('password')

            insert_in_users(fname, lname, email, password)
            
            flash("Successfully Registered")
            delete_otp(email)
            session.pop('otp')
            session.pop('time')

            return redirect(url_for('the_user'))

        elif less_than_five > 300:
            flash("Time Expired")
            return redirect(url_for('verifying_otp'))

        else:
            flash("Wrong OTP")
            return redirect(url_for('verifying_otp'))

    else:
        email = session.get('email')
        return render_template('otp_verification.html')


@app.route("/user", methods=["POST", "GET"])
@login_required
def the_user():
    email = session["email"]
    get_user= get_name(email)
    flash("You are logged in!")
    return render_template("users.html", user_name=get_user)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        if "email" in session:
            flash("You have been logged out", "info")
            session.pop("email")
            return redirect(url_for("login"))
        else:
            flash('You are not logged in yet! ')
            return redirect(url_for("login"))
    else:
        return render_template('logout.html')


if __name__ == "__main__":
   app.run(debug=True)



