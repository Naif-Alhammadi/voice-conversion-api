from flask import Flask, render_template,request, redirect, session, jsonify
from flask_session import Session


from helper import login_required
from helper import robot
from helper import slow_down
from helper import speed_up


import os
from dotenv import load_dotenv
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

from werkzeug.security import generate_password_hash, check_password_hash


# load the weather API key
load_dotenv()

app = Flask(__name__)


# secure the session data
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if session.get("user_id") is not None:
        return redirect("/conversion")
    return render_template("index.html")


@app.route("/mainpage")
def mainpage():
    return render_template("index.html")


@app.route("/weather")
@login_required
def weather():
    return jsonify({"weatherAPI": os.getenv("WEATHER_API")})


@app.route("/preferred-mode", methods=["GET", "POST"])
def preferred_mode():
    if request.method == "POST":

        # available modes
        modes = ["default", "light", "dark"]

        # check if user is logged in
        if session.get("user_id") is not None:

            # the chosen mode
            user_preferred_mode = request.get_json("mode")
            mode = user_preferred_mode["mode"]

            # check if mode is in the available modes list
            if mode in modes:

                # connect to the data base
                connection = psycopg2.connect(os.getenv("DATABASE_URL"))
                cur = connection.cursor(cursor_factory=RealDictCursor)

                # update the user preferred mode in the database
                cur.execute("UPDATE users SET preferred_mode = %s WHERE user_id = %s", (mode, str(session["user_id"])))
            
                connection.commit()
                cur.close()
                connection.close()

                return jsonify({"mode": mode})
            return jsonify("error")


        # if user is not logged in yet and wants to change the preferred mode
        else:
            user_preferred_mode = request.get_json("mode")
            mode = user_preferred_mode["mode"]
            if mode in modes:
                return jsonify({"mode": mode})
            return jsonify("erorr")


    elif request.method == "GET":

        # check if user is logged in
        if session.get("user_id") is not None:

            # connect to the data base
            connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            cur = connection.cursor(cursor_factory=RealDictCursor)
        
            # query for the existing mode
            cur.execute("SELECT preferred_mode FROM users WHERE user_id = %s", str(session["user_id"]))
            mode = cur.fetchone()
        
        
            connection.commit()
            cur.close()
            connection.close()

            return jsonify({"mode": mode["preferred_mode"]})
            
        return jsonify("log in first")            


@app.route("/profile-pic", methods=["GET", "POST"])
@login_required
def profile_pic():
    if request.method == "POST":

        # connect to the data base
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = connection.cursor(cursor_factory=RealDictCursor)

        # take the file from http body
        picture = request.files["picture"]

        # add the folder path if not exists
        os.makedirs(os.path.join("static", "uploads", "profile_pictures"), exist_ok=True)

        # take the path with the image
        path = os.path.join(os.path.join("static", "uploads", "profile_pictures"), picture.filename)

        # save the image
        picture.save(path)

        # update the database
        cur.execute("UPDATE users SET user_profile_picture = %s WHERE user_id = %s", (path, session["user_id"]))

        connection.commit()
        cur.close()
        connection.close()

        # return the path of the image
        return jsonify({
            "path": path
        })

    
    elif request.method == "GET":

        # connect to the data base
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = connection.cursor(cursor_factory=RealDictCursor)

        # query if the user has an existence image path
        cur.execute("SELECT user_profile_picture FROM users WHERE user_id = %s", str(session["user_id"]))

        pic_url = cur.fetchone()


        connection.commit()
        cur.close()
        connection.close()

        return jsonify({"path": pic_url["user_profile_picture"]})


@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))

        cur = connection.cursor(cursor_factory=RealDictCursor)

        # take user login info from a json file
        user_data = request.get_json()

        # check if all fileds are filled
        if not user_data["name"] or not user_data["email"] or not user_data["password"] or not user_data["verifypassword"]:
            return jsonify({"message": "please fill all fileds"})

        # check if the password match the verifypassword
        if user_data["password"] != user_data["verifypassword"]:
            return jsonify({"message": "please check your verifypassword"})

        # hash user's password
        hash_password = generate_password_hash(user_data["password"])

        # insert user info to a database
        try:
            cur.execute("INSERT INTO users (user_name, user_email, hash_password) VALUES (%s, %s, %s)", (user_data["name"], user_data["email"], hash_password))
            connection.commit()


        except psycopg2.IntegrityError:
            connection.rollback()
            return jsonify({"message": "you are already logged in!"})


        cur.execute("SELECT user_id FROM users WHERE user_name = %s AND hash_password = %s", (user_data["name"], hash_password))
        user = cur.fetchone()
        session["user_id"] = user["user_id"]


        cur.close()
        connection.close()


        return jsonify({
            "redirect": "True",
            "location": "/conversion"
        })

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # if user submit a form
    if request.method == "POST":

        # take user's data
        register = request.get_json("email")
        email = register["email"]
        password = register["password"]

        # connect to the database
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = connection.cursor(cursor_factory=RealDictCursor)

        # query for all emails
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        # search for every user in users
        for user in users:

            # if email of a user is found
            if email == user["user_email"]:
                # query about the hash password of the user
                cur.execute("SELECT hash_password FROM users WHERE user_email = %s", (email,))
                hash_password = cur.fetchone()["hash_password"]

                # check if the hash password does match the password
                if check_password_hash(hash_password, password):

                    # close the connection of the database
                    connection.close()
                    cur.close()
                    session["user_id"] = user["user_id"]

                    return jsonify({"message": "success"})

                # if the hash password does not match the password
                else:

                    # close the connection of the database
                    connection.close()
                    cur.close()
                    return jsonify({"message": "password is not correct"})

        # if the email does not owned by any of the users

        # close the connection of the database
        connection.close()
        cur.close()
        return jsonify({"message": "email not found"})

    # if user search for the register page
    return render_template("login.html")


@app.route("/conversion", methods=["GET", "POST"])
@login_required
def homepage():
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT user_name FROM users WHERE user_id = %s", str(session["user_id"]))
    user_name = cur.fetchone()


    cur.execute("SELECT * FROM transactions WHERE user_id = %s", (session["user_id"],))
    transactions_query = cur.fetchall()
    transactions = list()
    for transaction in transactions_query:
        transactions.append(transaction)


    connection.close()
    cur.close()

    return render_template("conversion.html", user_name=user_name["user_name"], transactions=transactions)


@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor(cursor_factory=RealDictCursor)

    
    file = request.files["file"]
    convert = request.form.get("convertTo")
    value = request.form.get("value")

    if not value:
        value = "0"

    if not value.isdigit():
        return jsonify("process_failed")
    

    os.makedirs("static/uploads/audios", exist_ok=True)
    path = os.path.join("static", "uploads", "audios", file.filename)
    outter_path = os.path.join("static", "uploads", "edited_audios", f"edited_{convert}_{value}.wav")
    file.save(path)
    if convert == "speed_up":
        s = speed_up(int(value), path, outter_path)


    elif convert == "slow_down":
        slow_down(int(value), path, outter_path)

    elif convert == "rotter_pbot":
        robot(path, outter_path)

    cur.execute("INSERT INTO transactions(transaction_url, transaction_description, transaction_date, user_id) VALUES(%s, %s, %s, %s)", (f"edited_{convert}_{value}.wav", convert, datetime.now(), str(session["user_id"])))
    
    connection.commit()
    connection.close()
    cur.close()
        
    return jsonify({"process_success": outter_path})


@app.route("/history")
def history():

    # connect to the data base
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor(cursor_factory=RealDictCursor)

    # query for all the transactions
    cur.execute("SELECT * FROM transactions WHERE user_id = %s", (session["user_id"],))
    transactions_query = cur.fetchall()

    # fill it with each transaction
    transactions = list()
    for transaction in transactions_query:
        transactions.append(transaction)

    # close the connection
    connection.close()
    cur.close()

    return render_template("history.html", transactions=transactions)