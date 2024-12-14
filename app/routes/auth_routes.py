from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User, Feedback
from app.forms import LoginForm, RegisterForm
from app import db
from flask_migrate import Migrate

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.submit_review'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'warning')
            return render_template('register.html', form=form)
            
        # Check if email exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please login instead.', 'warning')
            return redirect(url_for('auth.login'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.view_reviews'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful! You can now submit feedback.', 'success')
            return redirect(url_for('user.submit_review'))
        flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_home():
    if not current_user.is_admin:
        flash('Access denied. Admin only area.', 'danger')
        return redirect(url_for('user.home'))
    
    pending_reviews = Feedback.query.filter_by(is_approved=False)\
                                  .order_by(Feedback.created_date.desc()).all()
    approved_reviews = Feedback.query.filter_by(is_approved=True)\
                                   .order_by(Feedback.created_date.desc()).all()
    total_users = User.query.filter_by(is_admin=False).count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating))\
                          .filter(Feedback.is_approved==True)\
                          .scalar() or 0
    
    return render_template('admin/admin_dashboard.html', 
                         pending_reviews=pending_reviews,
                         approved_reviews=approved_reviews,
                         total_users=total_users,
                         avg_rating=round(avg_rating, 2))

@admin_bp.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.home'))
    
    review = Feedback.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully.', 'success')
    return redirect(url_for('admin.admin_home'))

@admin_bp.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.home'))
    
    review = Feedback.query.get_or_404(review_id)
    
    if request.method == 'POST':
        review.rating = request.form.get('rating', type=int)
        review.comment = request.form.get('comment')
        db.session.commit()
        flash('Review updated successfully.', 'success')
        return redirect(url_for('admin.admin_home'))
        
    return render_template('admin/edit_review.html', review=review)

@admin_bp.route('/approve_review/<int:review_id>', methods=['POST'])
@login_required
def approve_review(review_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.home'))
    
    review = Feedback.query.get_or_404(review_id)
    review.is_approved = True
    db.session.commit()
    flash('Review approved successfully.', 'success')
    return redirect(url_for('admin.admin_home'))

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    # Get approved reviews and calculate average rating
    approved_reviews = Feedback.query.filter_by(is_approved=True).all()
    avg_rating = db.session.query(db.func.avg(Feedback.rating))\
                          .filter(Feedback.is_approved==True)\
                          .scalar() or 0
    
    return render_template('user/home.html', 
                         reviews=approved_reviews,
                         avg_rating=round(avg_rating, 2))

@user_bp.route('/submit-review', methods=['GET', 'POST'])
@login_required
def submit_review():
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = request.form.get('comment')
        
        feedback = Feedback(
            rating=rating, 
            comment=comment, 
            user_id=current_user.id,
            is_approved=False  # New reviews start as unapproved
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your review! It will be visible after approval.', 'success')
        return redirect(url_for('user.home'))
    
    return render_template('user/submit_review.html')

