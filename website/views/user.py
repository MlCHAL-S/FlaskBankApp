from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from website.models import User, Transaction
from website import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def home():
    return render_template('home.html')


@user_bp.route('/user', methods=['GET', 'POST'])
def user():
    email = session.get('email')
    user = User.get_by_email(email) if email else None

    if user:
        recent_transactions = Transaction.query.filter(
            (Transaction.sender_id == user.id) | (Transaction.recipient_id == user.id)
        ).order_by(Transaction.timestamp.desc()).limit(5).all()

        return render_template('user.html', user=user, recent_transactions=recent_transactions)
    else:
        flash('You are not logged in or user not found!', 'danger')
        return redirect(url_for('auth.login'))


@user_bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user = User.get_by_email(session.get('email'))

        if user:
            if 'full_name' in request.form and request.form['full_name']:
                user.full_name = request.form['full_name']
            if 'email' in request.form and request.form['email']:
                user.email = request.form['email']
            if 'address' in request.form and request.form['address']:
                user.address = request.form['address']
            if 'phone_number' in request.form and request.form['phone_number']:
                user.phone_number = request.form['phone_number']

            try:
                session['email'] = request.form['email']
                db.session.commit()
                flash("Your details have been updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while updating your details. Please try again.", "danger")
                print(e)

    return redirect(url_for('user.user'))


@user_bp.route('/transfer', methods=['POST'])
def transfer():
    if request.method == 'POST':
        sender = User.get_by_email(session.get('email'))
        recipient_email = request.form['recipient_email']
        amount = float(request.form['amount'])

        if recipient_email == session.get('email'):
            flash("Cannot send money to yourself.", "danger")
        else:
            if sender and amount > 0:
                recipient = User.get_by_email(recipient_email)
                if recipient:
                    if sender.balance >= amount:
                        sender.balance -= amount
                        recipient.balance += amount

                        transaction = Transaction(
                            sender_id=sender.id,
                            recipient_id=recipient.id,
                            amount=amount
                        )

                        db.session.add(transaction)

                        try:
                            db.session.commit()
                            flash("Transfer successful!", "success")
                        except Exception as e:
                            db.session.rollback()
                            flash("An error occurred during the transfer. Please try again.", "danger")
                            print(e)
                    else:
                        flash("Insufficient balance for the transfer.", "danger")
                else:
                    flash("Recipient not found.", "danger")
            else:
                flash("Invalid transfer amount.", "danger")

    return redirect(url_for('user.user'))


@user_bp.route('/transactions', methods=['GET'])
def transactions():
    email = session.get('email')
    user = User.get_by_email(email)

    if user:
        page = request.args.get('page', 1, type=int)
        transactions = Transaction.query.filter(
            (Transaction.sender_id == user.id) | (Transaction.recipient_id == user.id)
        ).order_by(Transaction.timestamp.desc()).paginate(page=page, per_page=10)

        return render_template('all_transactions.html', user=user, transactions=transactions)
    else:
        flash('You are not logged in or user not found!', 'danger')
        return redirect(url_for('auth.login'))
