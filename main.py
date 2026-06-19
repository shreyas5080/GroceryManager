import time

from flask import Flask, render_template, request, url_for, redirect, session, flash
from datetime import timedelta
from database import insert, get_results, insert_in_users, get_email, get_password, get_name
from OTP import user_otp, verify_otp
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
        user_fname = request.form["fname"]
        user_lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        exiting_email = get_email(email)

        if exiting_email:
            flash("This email is already used")
            return redirect(url_for("register"))

        session["pending_registration"] = {
            "fname": user_fname,
            "lname": user_lname,
            "email": email,
            "password": password,
        }

        try:
            user_otp(email)
            flash("OTP sent to your email. Please enter it below.", "info")
        except Exception:
            flash("Unable to send OTP. Check email settings.", "error")
            return redirect(url_for("register"))

        return redirect(url_for("verifying_otp"))

    return render_template("register.html")


@app.route('/otp-verification', methods=["POST", "GET"])
def verifying_otp():
    pending = session.get("pending_registration")

    if not pending:
        flash("No pending registration found. Please start again.", "error")
        return redirect(url_for("register"))

    if request.method == "POST":
        entered_otp = request.form.get("code", "").strip()
        if not entered_otp:
            flash("Please enter the OTP.", "error")
            return render_template("otp_verification.html")

        verification = verify_otp(pending["email"], entered_otp)
        if verification is True:
            insert_in_users(
                pending["fname"],
                pending["lname"],
                pending["email"],
                pending["password"],
            )
            session.pop("pending_registration", None)
            session["email"] = pending["email"]
            flash("Registration successful. You are now logged in.", "success")
            return redirect(url_for("the_user"))

        flash(verification, "error")

    return render_template("otp_verification.html")


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



