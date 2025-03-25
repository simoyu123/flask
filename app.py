from flask import Flask, render_template,request,session
import sqlite3
import hashlib
app = Flask(__name__)
app.secret_key = "any random string"
con = sqlite3.connect("login.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS LOGIN
                (USERNAME TEXT PRIMARY KEY NOT NULL,
                 PASSWORD TEXT NOT NULL
)""")
con.commit()
con.close()

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
         con = sqlite3.connect("login.db")
         cur = con.cursor()
         hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
         cur.execute("INSERT INTO LOGIN (USERNAME,PASSWORD) VALUES (?,?)",
                        (request.form["username"],hash))    
         con.commit()
         con.close()
         return"SIGNUP SUCCESS"
      
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
         con = sqlite3.connect("login.db")
         cur = con.cursor()
         hash = hashlib.sha256(request.form["password"].encode()).hexdigest()                
         cur.execute("SELECT USERNAME FROM LOGIN WHERE USERNAME=? AND PASSWORD=?",
                    (request.form["username"],hash))
         user = cur.fetchone()
         if user:
             session["username"] = request.form["username"]
             return render_template("welcome.html")
         else:
             return "login failed"

@app.route("/w")
def welcome():
    return render_template("welcome.html")

@app.route("/logout")
def logout():
    session.pop("username",None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
