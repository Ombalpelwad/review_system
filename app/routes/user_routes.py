from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Feedback
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_home'))
    return render_template('user/home.html')

@user_bp.route('/submit-review', methods=['GET', 'POST'])
@login_required
def submit_review():
    if current_user.is_admin:
        return redirect(url_for('admin.admin_home'))
        
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        feedback = Feedback(rating=rating, comment=comment, user_id=current_user.id)
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('user.home'))
    
    return render_template('user/submit_review.html') 