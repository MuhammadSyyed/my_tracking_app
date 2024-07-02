from flask import Flask, render_template, request, jsonify, send_from_directory
import json, uuid
from datetime import datetime, timedelta
from db_functions import *
from constant import *
import traceback

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True


def is_valid_session(session_id):
    user = get_user_by_session_id(session_id)

    if user:
        username = user["username"]
        current_location = user["current_location"]
        expiration_time = user["session_expiration"]
        if datetime.now() < expiration_time:
            return True, username,current_location
    return False, False,False


@app.route("/", methods=["GET"])
def index():
    return render_template("login.html", message="Please login to start session!")


@app.route("/register", methods=["GET"])
def register():
    return render_template("signup.html", message="Please add account!")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = get_one_user(username, password)
    if user:
        return render_template(
            "map.html",
            session_id=user["session_id"],
            username=username,
            current_location=user["current_location"],
            page_name="Map",
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    response = add_new_user(username, password)
    if response["success"]:
        return render_template(
            "login.html", message="Account Added Successfully! Please Login."
        )
    else:
        return render_template("signup.html", message=response["message"])


@app.route("/map", methods=["GET"])
def map():
    session_id = request.cookies.get("session_id")
    valid_id, username,current_loc = is_valid_session(session_id)
    if valid_id:
        return render_template(
            "map.html",
            session_id=session_id,
            username=username,
            page_name="Map",
            current_location=current_loc
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.headers["Session-Id"]
    valid_id, _ ,_= is_valid_session(session_id)
    if valid_id:
        delete_session(session_id)
        return jsonify({"message": "User logged Out Successfully!"})
    return jsonify({"message": "Unauthorized Access Denied!"})


if __name__ == "__main__":
    app.run(debug=True)
