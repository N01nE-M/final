from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("postgres://hphjpnuqpiwujp:4efbbcd564ac30568f3bc4f5d7cf266a446501de4e7632e4261c1cf3577917d6@ec2-34-204-121-199.compute-1.amazonaws.com:5432/dan6hi9t4c9a0s")

@app.route("/")
@login_required
def index():

    user_id = session["user_id"]

    rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)

    result = rows[0]["type"]
    username = rows[0]["username"]

    session["username"] = rows[0]["username"]
    session["fname"] = rows[0]["fname"]
    session["lname"] = rows[0]["lname"]
    session["type"] = rows[0]["type"]


    return render_template("index.html", result=result, username=username )

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change account settings."""

    if request.method == "POST":

        # validate if fields are all filled
        if not request.form.get("old_password") or not request.form.get("password") or not request.form.get("confirm_password"):
            return render_template("settings.html")

        # variable assignment
        old_password = request.form.get("old_password")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")


        # retrieve user data
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        # verify old password
        if len(user) != 1 or not pwd_context.verify((old_password), user[0]["hash"]):
            return apology("incorrect password")

        # confirm password change
        if password != confirm_password:
            return apology("passwords don't match")

        # update password in db
        hash = pwd_context.encrypt(password)
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", hash=hash, user_id=session["user_id"])

        return render_template("settings.html", success=1)

    else:
        return render_template("settings.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Update Profile"""

    if request.method == "POST":

        # variable assignment
        fname = request.form.get("fname")
        lname = request.form.get("lname")

        # retrieve user data

        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])


        db.execute("UPDATE users SET fname = :fname, lname = :lname WHERE id = :user_id", fname=fname, lname=lname, user_id=session["user_id"])

        return render_template("settings.html", succeed=1)

    else:
        return render_template("settings.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Input username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Input password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # remember username
        username = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        session["username"] = username[0]["username"]
        session["type"] = username[0]["type"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # verify username field is not empty
        if not request.form.get("username"):
            return apology("username is required")

        elif not request.form.get("fname") or not request.form.get("lname"):
            return apology("Enter First name and Last Name")
        # verify password field is not empty

        elif not request.form.get("password") or not request.form.get("confirm_password"):
            return apology("password fields should not be empty")

        # password confirmation
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords do not match")

        # if username exist in table
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) >= 1:
            return apology("username exists!")

        # add new user to database
        db.execute("INSERT INTO users (fname, lname, username, hash) VALUES (:fname, :lname, :username, :hash)",
                    fname=request.form.get("fname"),
                    lname=request.form.get("lname"),
                    username=request.form.get("username"),
                    hash=pwd_context.encrypt(request.form.get("password")))

        # automatically login new user
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]


        # show username
        username = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        session["username"] = username[0]["username"]


        # redirect to home page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route('/guest')
def guest():
     return render_template("index.html")
@app.route('/dist')
def dist():
     return render_template("dist.html")
@app.route('/INTP')
def intp():
    return render_template('INTP.html')
@app.route('/ENTP')
def entp():
    return render_template('ENTP.html')
@app.route('/INTJ')
def intj():
    return render_template('INTJ.html')
@app.route('/ENTJ')
def entj():
    return render_template('ENTJ.html')
@app.route('/ENFP')
def enfp():
    return render_template('ENFP.html')
@app.route('/ESFJ')
def esfj():
    return render_template('ESFJ.html')
@app.route('/ESFP')
def esfp():
    return render_template('ESFP.html')
@app.route('/ESTJ')
def estj():
    return render_template('ESTJ.html')
@app.route('/ESTP')
def estp():
    return render_template('ESTP.html')
@app.route('/INFJ')
def infj():
    return render_template('INFJ.html')
@app.route('/INFP')
def infp():
    return render_template('INFP.html')
@app.route('/ISFJ')
def isfj():
    return render_template('ISFJ.html')
@app.route('/ISFP')
def isfp():
    return render_template('ISFP.html')
@app.route('/ISTJ')
def istj():
    return render_template('ISTJ.html')
@app.route('/ISTP')
def istp():
    return render_template('ISTP.html')
@app.route('/ENFJ')
def enfj():
    return render_template('ENFJ.html')

@app.route("/result", methods=["GET", "POST"])
@login_required
def result():

    if request.method == "POST":

        # determine current user
        user_id = session["user_id"]

        #initialize variables
        E=I=S=N=F=T=J=P=0

        res = []

        # assign radiobutton names
        ei = ['ei1' , 'ei2', 'ei3' , 'ei4', 'ei5']
        ns = ['ns1' , 'ns2', 'ns3' , 'ns4', 'ns5']
        ft = ['ft1' , 'ft2', 'ft3' , 'ft4', 'ft5']
        jp = ['jp1' , 'jp2', 'jp3' , 'jp4', 'jp5']



        # calculate radio button response
        for i in range(5):
            ei[i] = request.form.get(f"EI{i+1}")

            if ei[i] == "E":
                E += 1
            elif ei[i] == "I":
                I += 1

            ns[i] = request.form.get(f"NS{i+1}")

            if ns[i] == "N":
                N += 1
            elif ns[i] == "S":
                S += 1

            ft[i] = request.form.get(f"FT{i+1}")

            if ft[i] == "T":
                T += 1
            elif ft[i] == "F":
                F += 1

            jp[i] = request.form.get(f"JP{i+1}")

            if jp[i] == "P":
                P += 1
            elif jp[i] == "J":
                J += 1

        if E < I:
            res.append("I")
        elif E > I:
            res.append("E")

        if N < S:
            res.append("S")
        elif N > S:
            res.append("N")

        if T < F:
            res.append("F")
        elif T > F:
            res.append("T")

        if J < P:
            res.append("P")
        elif J > P:
            res.append("J")


        if res and len(res) == 4:

            full_str = ''.join([str(elem) for elem in res])

            db.execute("UPDATE users SET type = :full_str WHERE id = :id", full_str=full_str, id=user_id)

            if full_str == 'INTP':
                return redirect('/INTP')
            elif full_str == 'ENTP':
                return redirect('/ENTP')
            elif full_str == 'ENTJ':
                return redirect('/ENTJ')
            elif full_str == 'ENFP':
                return redirect('/ENFP')
            elif full_str == 'ENFJ':
                return redirect('/ENFJ')
            elif full_str == 'INTJ':
                return redirect('/INTJ')
            elif full_str == 'INFJ':
                return redirect('/INFJ')
            elif full_str == 'ISFJ':
                return redirect('/ISFJ')
            elif full_str == 'ISTJ':
                return redirect('/ISTJ')
            elif full_str == 'ISTP':
                return redirect('/ISTP')
            elif full_str == 'ISFP':
                return redirect('/ISFP')
            elif full_str == 'INFP':
                return redirect('/INFP')
            elif full_str == 'ESFJ':
                return redirect('/ESFJ')
            elif full_str == 'ESFP':
                return redirect('/ESFP')
            elif full_str == 'ESTJ':
                return redirect('/ESTJ')
            elif full_str == 'ESTP':
                return redirect('/ESTP')
            else:
                return render_template("test.html")


        return render_template("test.html")

    else:
        return render_template("test.html")

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete Account"""

    if request.method == "POST":

        db.execute("DELETE FROM users WHERE id = :user_id", user_id=session["user_id"])


        return redirect('/logout')

    else:
        return render_template("settings.html")




