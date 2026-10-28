import os

from dotenv import load_dotenv

from flask import Flask, render_template,request, redirect, session, jsonify


from helper import login_required

from flask_session import Session
from helper import robot
from helper import slow_down
from helper import speed_up

# load the weather API key
load_dotenv()

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if session.get("user_id") is not None:
        return render_template("homepage.html")
    return render_template("index.html")

@app.route("/weather")
@login_required
def weather():
    return jsonify({"weatherAPI": os.getenv("WEATHER_API")})

@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        user_data = request.get_json()
        if not user_data["name"] or not user_data["email"] or not user_data["password"] or not user_data["verifypasswrod"]:
            return jsonify("please fill all fileds")
        session["user_id"] = 1
        return jsonify({
            "redirect": "True",
            "location": "/homepage"
        })

    return render_template("index.html")

@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    return render_template("homepage.html")


@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
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
        
    return jsonify({"process_success": outter_path})