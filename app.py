from flask import Flask, render_template,request

app = Flask(__name__,static_folder='./static',template_folder='./templates')

@app.get("/<name>")
def home(name):
    return render_template('index.html',name=name)

@app.post("/square")
def square():
    payload = request.get_json()
    sqr = payload["number"]**2
    return {"square":sqr}

if __name__ == "__main__":
    app.run()
