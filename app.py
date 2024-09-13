from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
    redirect,
)
from flask_cors import CORS
import json, uuid
from script import get_locations, generate_map_string
from datetime import datetime, timedelta
from db_functions import *
from constant import *
import traceback
import os

app = Flask(__name__)
app.jinja_env.auto_reload = True
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TEMPLATES_AUTO_RELOAD"] = True
CORS(app)


def is_valid_session(session_id):
    user = get_user_by_session_id(session_id)

    if user:
        username = user["username"]
        current_location = user["current_location"]
        expiration_time = user["session_expiration"]
        if datetime.now() < expiration_time:
            return True, username, current_location
    return False, False, False


@app.route("/", methods=["GET"])
def index():
    return render_template("login.html", message="Please login to start session!")


@app.route("/addloc", methods=["GET"])
def addloc():
    session_id = request.cookies.get("session_id")
    valid_id, username, current_loc = is_valid_session(session_id)
    if valid_id:
        _, locations = get_locations("csv_data/*.csv")
        return render_template(
            "addloc.html",
            session_id=session_id,
            username=username,
            page_name="Add New Location",
            current_location=current_loc,
            locdtls=locations.to_dict(orient="records"),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/register", methods=["GET"])
def register():
    return render_template("signup.html", message="Please add account!")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = get_one_user(username, password)
    if user:
        _, locations = get_locations("csv_data/*.csv")
        return render_template(
            "map.html",
            session_id=user["session_id"],
            username=username,
            current_location=user["current_location"],
            page_name="Map",
            locations=locations["desc"].values.tolist(),
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


@app.route("/register_loc", methods=["POST"])
def register_loc():
    session_id = request.cookies.get("session_id")
    valid_id, username, current_loc = is_valid_session(session_id)
    if valid_id:
        location_name = request.form.get("location_name")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        description = request.form.get("description")
        file = request.files.get("image_path")
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        response = add_new_location(
            {
                "location_name": location_name,
                "latitude": float(latitude),
                "longitude": float(longitude),
                "description": description,
                "image_path": file_path,
            }
        )
        if response["success"]:

            _, locations = get_locations("csv_data/*.csv")
            return render_template(
                "locations.html",
                session_id=session_id,
                username=username,
                page_name="Locations",
                current_location=current_loc,
                alllocs=get_all_locations(),
                locations=locations["desc"].values.tolist(),
            )
        else:
            return render_template(
                "addloc.html",
                session_id=session_id,
                username=username,
                page_name="Add New Location",
                current_location=current_loc,
            )

    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/map", methods=["GET"])
def map():
    session_id = request.cookies.get("session_id")
    valid_id, username, current_loc = is_valid_session(session_id)
    if valid_id:
        _, locations = get_locations("csv_data/*.csv")
        return render_template(
            "map.html",
            session_id=session_id,
            username=username,
            page_name="Map",
            current_location=current_loc,
            locations=locations["desc"].values.tolist(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/location", methods=["GET"])
def location():
    session_id = request.cookies.get("session_id")
    valid_id, username, current_loc = is_valid_session(session_id)
    if valid_id:
        _, locations = get_locations("csv_data/*.csv")
        return render_template(
            "locations.html",
            session_id=session_id,
            username=username,
            page_name="Locations",
            current_location=current_loc,
            alllocs=get_all_locations(),
            locations=locations["desc"].values.tolist(),
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/search", methods=["GET"])
def search():
    session_id = request.cookies.get("session_id")
    valid_id, username, current_loc = is_valid_session(session_id)
    if valid_id:
        _, locations = get_locations("csv_data/*.csv")
        return render_template(
            "search.html",
            session_id=session_id,
            username=username,
            page_name="Search",
            locations=locations["desc"].values.tolist(),
            users=get_all_users(),
            current_location=current_loc,
        )
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.get("/get_map/<source>/<destination>")
def get_map(source, destination):
    session_id = request.cookies.get("session_id")
    valid_id, _, _ = is_valid_session(session_id)
    if valid_id:
        filename, _ = generate_map_string(source, destination)
        return render_template(filename)


@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.headers["Session-Id"]
    valid_id, _, _ = is_valid_session(session_id)
    if valid_id:
        delete_session(session_id)
        return jsonify({"message": "User logged Out Successfully!"})
    return jsonify({"message": "Unauthorized Access Denied!"})


@app.route("/set_loc", methods=["POST"])
def set_loc():
    session_id = request.cookies.get("session_id")
    valid_id, _, _ = is_valid_session(session_id)
    print(session_id)
    if valid_id:
        data = request.get_json()
        location = data.get("location")
        response = update_user_location_by_session_id(session_id, location)
        return jsonify(response)
    else:
        return render_template("login.html", message="Unauthorized Access Denied!")


@app.route("/delete_loc/<loc_id>", methods=["GET"])
def delete_loc(loc_id):
    session_id = request.cookies.get("session_id")
    valid_id, _, _ = is_valid_session(session_id)
    if valid_id:
        res = delete_location(loc_id)
        if res["success"]:
            return redirect(url_for("location"))


if __name__ == "__main__":
    app.run(debug=True)
