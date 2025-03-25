from flask import Flask, render_template,request
import sqlite3
import hashlib
app = Flask(__name__)

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
             return "Hello" + user[0]
         else:
             return "login failed"

if __name__ == "__main__":
    app.run(debug=True)
