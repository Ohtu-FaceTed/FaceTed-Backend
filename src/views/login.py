from . import views as app
from ..models import db, Admin
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user, current_user


@app.route("/801fc31", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("admLogin.html")

    form = request.form
    pw = form['password']
    username = form['username']
    user = Admin.query.filter_by(username = username).first()
    
    if not user:
         return render_template("admLogin.html", form = form,
                               error = "No such username or password")

    if not bcrypt.check_password_hash(user.password, pw):
        return render_template("admLogin.html", form = form,
                               error = "No such username or password")


    print("User " + user.name + " was identified")
    login_user(user)
    return redirect(url_for("index"))

#logout handler
@app.route("/auth/logout")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))