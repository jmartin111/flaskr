from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello(greeting="hello flaskr"):
    style = "color:orange;text-align:center"
    return f"<h1 style={style}>{greeting}</h1>"


app.run(debug=True)
