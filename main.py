import time

from flask import Flask, render_template, request, url_for, redirect,session, flash
from datetime import timedelta
from  database import insert, get_results, insert_in_users, get_email, get_password, get_name, get_temp_email
import secrets 
from OTP import user_otp


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(seconds=30)
app.secret_key = "wearetheworld"


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
            user_otp(email)
            return redirect(url_for('verifying_otp'))

    else:
        if "email" in session:
            return redirect(url_for("the_user"))

        return render_template("register.html")

@app.route('/otp-verification', methods=["POST", "GET"])
def verifying_otp():
    
    if request.method == "POST":
        user_fname = request.form["fname"]
        user_lname = request.form["lname"]
        password = request.form["password"]
        returned_email = get_temp_email

        user_otp = request.form["code"]
        returned_otp = user_otp[0]

        otp_time = user_otp[1]
        current_time = time.time()
        less_than_five = current_time - otp_time

        if less_than_five < 300 and user_otp == returned_otp:
            insert_in_users(user_fname, user_lname, returned_email, password)
            flash("Successfully Registered")

            return redirect(url_for("the_user"))

        elif less_than_five > 300:
            flash("Time Expired")

        else:
            flash("Wrong OTP")

    else:
        return redirect(url_for('otp_verification.html'))


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



