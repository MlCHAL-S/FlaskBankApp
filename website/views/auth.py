from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from website import db
from website.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        date_of_birth_str = request.form['date_of_birth']
        pesel_number = request.form['pesel_number']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phone_number']
        account_type = request.form['account_type']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        initial_balance = request.form['initial_balance']

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('auth.signup'))

        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('auth.signup'))

        new_user = User(
            full_name=full_name,
            date_of_birth=date_of_birth,
            pesel_number=pesel_number,
            address=address,
            email=email,
            phone_number=phone_number,
            account_type=account_type,
            balance=initial_balance
        )

        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            session['logged_in'] = True
            session['email'] = email
            flash("Account created successfully!", "success")
            return redirect(url_for('user.user'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the account. Please try again.", "danger")
            print(e)

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.get_by_email(email)

        if user and user.check_password(password):
            session['logged_in'] = True
            session['email'] = email
            flash('You have successfully logged in!', category='success')
            return redirect(url_for('user.user'))
        else:
            flash('Invalid Credentials. Try again!', category='danger')
            return redirect(url_for('auth.login'))

    return render_template('home.html')


@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('You have successfully logged out!', category='success')
    return redirect(url_for('auth.login'))
