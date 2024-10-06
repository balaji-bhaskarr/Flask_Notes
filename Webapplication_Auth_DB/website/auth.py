from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', '__name__')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('password1')

        print(email+' '+name+ ' '+ password+ ' '+confirm_password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account with this Email Id already exists.', category='error')
        elif len(email)<4:
            flash('Email must be greated than 4', category='error')
        elif len(name)<2:
            flash('Use full name', category='error')
        elif password!=confirm_password:
            flash('Passwords do not match', category='error')
        elif len(password)<8:
            flash('Password should have 8 or more characters', category='error')
        else:
            try:
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully', category='success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                print('Exception : '+str(e))
                flash('Failed to create account, please try again.', category='error')
                db.session.rollback()
    return render_template('signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect, try again!', category='error')
        else:
            flash('Account with this Email Id doesn\'t exist')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))