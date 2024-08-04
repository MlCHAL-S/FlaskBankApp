from flask import Blueprint, render_template

misc_bp = Blueprint('misc', __name__)


@misc_bp.route('/about')
def about():
    return render_template('about.html')


@misc_bp.route('/contact')
def contact():
    return render_template('contact.html')
