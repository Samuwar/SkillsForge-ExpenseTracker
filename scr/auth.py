from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully!")
                return redirect(url_for('views.home'))
        flash("Incorrect login details!", category='error')
        return render_template("login.html", user=current_user)
    return render_template("login.html", user=current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = data.get('password')
        repassword = data.get('repassword')
        print(username)
        if password != repassword:
            flash("Enter the same password!", category='error')
        elif len(username) < 3:
            flash("Username must be greater than 2 characters", category='error')
        elif type(username[0]) == 'int':
            flash("Username must not start with integer", category='error')
        elif User.query.filter_by(username=username).all():
            print(User.query.filter_by(username=username))
            flash("Username already exists", category='error')
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password=password)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))