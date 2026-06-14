from flask import Flask, render_template, request, url_for, redirect,session, flash
from datetime import timedelta
from  groceryManDatabase import get_connection, insert, get_results, insert_in_users, get_email, get_password, get_name 


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(seconds=30)
app.secret_key = "wearetheworld"


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("homepage.html")


@app.route("/result")
def print_groceries():
    if "email" in session:
        email = session["email"]

        result = get_results(email)
        return render_template("print_grocery.html", results=result)
    else:

        return render_template("operations.html")


@app.route("/add", methods=["POST", "GET"])
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

        else:
            insert_in_users(user_fname, user_lname, email, password)
            return redirect(url_for('login'))

    else:
        if "email" in session:
            return redirect(url_for("the_user"))

        return render_template("register.html")


@app.route("/user", methods=["POST", "GET"])
def the_user():
    if "email" not in session:
        return redirect(url_for("login"))

    else:
        email = session["email"]
        get_name = get_name(email)
        flash("You are logged in!")
        return render_template("users.html", user_name=get_name)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        if "email" in session:
            flash("You have been logged out", "info")
            session.pop("email")
            return redirect(url_for("login.html"))
        else:
            flash('You are not logged in yet! ')
            return redirect(url_for("login"))
    else:
        return render_template('logout.html')


if __name__ == "__main__":
   app.run(debug=True)



