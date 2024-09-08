from flask import Blueprint, render_template

# Create the admin blueprint
admin_bp = Blueprint('admin', __name__,template_folder='templates/admin')

# Admin routes
@admin_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
