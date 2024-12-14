from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Feedback, User
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_home():
    if not current_user.is_admin:
        flash('Access denied. Admin only area.', 'danger')
        return redirect(url_for('user.home'))
    return render_template('admin/admin_home.html')

@admin_bp.route('/reviews')
@login_required
def view_all_reviews():
    if not current_user.is_admin:
        return redirect(url_for('user.home'))
    
    all_reviews = Feedback.query.all()
    total_users = User.query.filter_by(is_admin=False).count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0
    
    return render_template('admin/all_reviews.html', 
                         reviews=all_reviews, 
                         total_users=total_users,
                         avg_rating=avg_rating) 