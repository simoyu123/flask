from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
         username = request.form["username"]
         password = request.form["password"]
         if password == "123":
             return "Hello" + username
         else:
             return "wrong password"
