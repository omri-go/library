from flask import Flask
from database import mydatabase

app = Flask(__name__)
dbms = mydatabase.mydatabase()

@app.route("/")
def home_view():
		return f"<h1>Welcome to Geeks for Geeks</h1>{dbms.test()}"
