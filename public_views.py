from flask import Blueprint, render_template

# Create the public blueprint
public_bp = Blueprint('public', __name__, template_folder='templates/public')

# Public routes
@public_bp.route('/')
def index():
    return render_template('index.html')

@public_bp.route('/about')
def about():
    return render_template('about.html')
