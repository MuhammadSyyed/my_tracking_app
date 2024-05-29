from flask import Flask, render_template, request, jsonify
from script import get_locations, generate_map_string
from flask_cors import CORS

app = Flask(__name__, static_folder="./static", template_folder="./templates")
CORS(app=app)

@app.get("/")
def home():
    _, locations = get_locations("csv_data/*.csv")
    return render_template("main.html", locations=locations["desc"].values.tolist())


@app.post("/get_map")
def get_map():
    data = request.get_json()
    mymap = generate_map_string(data["current"],data["destination"])
    return jsonify({"map":mymap})


if __name__ == "__main__":
    app.run(debug=True)
