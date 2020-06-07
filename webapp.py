from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = "m2398c57we282739nc8472938r7m3xr9c9238rcn729837rxm"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    uto = db.Column(db.String(100))
    ufrom = db.Column(db.String(100))
    m = db.Column(db.String(100))

    def __init__(self,uto,ufrom,m):
        self.uto = uto
        self.ufrom=ufrom
        self.m=m

class Account():
    def __init__(self,name,password):
        self.name=name
        self.password = password

accounts = []


@app.route("/")
def tohome():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    if "name" in session:
        if session["name"] == "admin":
            return render_template("view.html",values=users.query.all(),u=accounts)
    return redirect(url_for("user"))

@app.route("/user",methods=["POST","GET"])
def user():
    if "name" in session:
        name = session["name"]
        if request.method == "POST":
            try:
                u = request.form["nm"]
                if u != u.replace(" ",""):
                    return render_template("upage.html",usr=name,values=users.query.all(),message="There should be no spaces in the recipient's username.")
                m = request.form["mm"]
                if u != "":
                    for userr in accounts:
                        if u==userr.name:
                            if u==name:
                                return render_template("upage.html",usr=name,values=users.query.all(),message="You can't send a message to yourself!")
                            db.session.add(users(u,name,m))
                            db.session.commit()
                            return render_template("upage.html",usr=name,values=users.query.all(),message=None)
                    return render_template("upage.html",usr=name,values=users.query.all(),message="There is no account with that username.")
                else:
                    return render_template("upage.html",usr=name,values=users.query.all(),message="Recipent's username should not be empty.")
            except KeyError:
                for item in users.query.all():
                    if item.uto == name:
                        users.query.filter_by(uto=name).delete()
                        db.session.commit()
        return render_template("upage.html",usr=name,values=users.query.all(),message=None)
    return redirect(url_for("login"))

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        uname = request.form["ln"].replace(" ","")
        upass = request.form["lp"]
        for acc in accounts:
            if acc.name == uname:
                if acc.password == upass:
                    session["name"] = uname
                    return redirect(url_for("user"))
        return render_template("login.html",message="Username or password is incorrect!")
    elif "name" in session:
        return redirect(url_for("user"))
    return render_template("login.html",message=None)

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        uname = request.form["sn"]
        if uname != uname.replace(" ",""):
            return render_template("signup.html",message="There should be no spaces in your username.")
        upass = request.form["sp"]
        if uname != "":
            a = [x for x in accounts if x.name == uname]
            if len(a)<1:
                accounts.append(Account(uname,upass))
                session["name"] = uname
                return redirect(url_for("user"))
            else:
                return render_template("signup.html",message="An account with that username already exists!")
        else:
            return render_template("signup.html",message="Username has to have atleast 1 character.")
    return render_template("signup.html",message=None)

@app.route("/logout")
def logout():
    session.pop("name",None)
    return render_template("logout.html")

if __name__=="__main__":
    db.create_all()
    app.run()
