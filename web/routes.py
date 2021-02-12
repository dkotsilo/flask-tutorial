from flask import Flask, redirect, url_for, render_template, request, session, flash
#from web import app
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "fsdgdfgfdg21fds"
app.permanent_session_lifetime = timedelta(minutes=4)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))


	def __init__(self, name, email):
		self.name = name
		self.email = email




# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return render_template("inidex.html", content={"a":2, "b":"hello"})


# @app.route("/admin")
# def admin():
# 	return redirect(url_for("user", name="Admin")) # Now we when we go to /admin we will redirect to user with the argument "Admin!
#permanent_session_lifetime
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent_session_lifetime = True
		user = request.form["nm"]
		session["user"] = user
		flash(f"Login Sacceful, {user}", "info")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("You already loged in")
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
	email = None
	if "user" in session:
		user = session["user"]

		if request.method == "POST":
			email = request.form["email"]
			session['email'] = email
			flash("Email was saved")
		else:
			if "email" in session:
				email = session["email"]
		return render_template("user.html", email=email)
	else:
		flash("You are not logged in")
		return redirect(url_for("login"))


# def user():
# 	email = None
#     if "user" in session:
#     	user = session["user"]
# 		if request.method == "POST":
# 			email = request.form["email"]
# 			session['email'] = email
# 		else:
# 			email = session["email"]
#         return render_template("user.html", user=user)
#     else:
# 		flash("You already loged in")
#         return redirect(url_for("login"))


@app.route("/logout")
def logout():
	flash(f"You have been logged out!, {user}", "info")
	session.pop("user", None)
	session.pop("email", None)
	return redirect(url_for("login"))

#from web import app
if __name__ =="__main__":
	db.create_all()
    app.run(debug=True)
