import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash, usd

from helpers import apology, login_required, lookup

# Configure application
application = Flask(__name__)

# Ensure templates are auto-reloaded
application.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
application.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
application.config["SESSION_FILE_DIR"] = mkdtemp()
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)


@application.route("/")
def index():
    return render_template("index.html")

@application.route("/about")
def about():
    return render_template("about.html")


@application.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@application.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@application.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fields wasn't left blank
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("password_confirmation"):
            return apology("must provide password confirmation", 403)
        elif request.form.get("password") != request.form.get("password_confirmation"):
            return apology("must match password and password confirmation", 403)

        # Crypt password
        hash_password = generate_password_hash(request.form.get("password"))

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@application.route("/schedule")
@login_required
def  schedule():
    events = [
    {
        'class' : 'Individual class',
        'date' : '2021-11-22'
    },
    {
        'class' : 'Group class',
        'date' : '2021-11-23'
    }
    ]
    return render_template("schedule.html", events = events)

@application.route("/torequest", methods=["GET", "POST"])
def torequest():

    if request.method == "POST":

        # Ensure name was submitted
        if not request.form.get("full_name"):
            return apology("must provide name", 403)

        # Ensure phone or email was submitted
        elif not request.form.get("phone") and not request.form.get("email"):
            return apology("must provide phone or email", 403)

        full_name = request.form.get("full_name")
        surname = full_name[0:full_name.find(' ')]
        name = full_name[(full_name.find(' ') + 1):full_name.find(' ', (full_name.find(' ') + 1),len(full_name))]
        patronymic = full_name[(full_name.find(' ', (full_name.find(' ') + 1),len(full_name)) + 1):len(full_name)]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/")

@application.route("/staff", methods=["GET", "POST"])
@login_required
def staff():
    return render_template("staff.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    application.errorhandler(code)(errorhandler)
    
if __name__ == "__main__":
   application.run(host='0.0.0.0')