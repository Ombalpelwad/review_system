# Review System

A web application for submitting and managing user reviews. Built with Flask, SQLAlchemy, and Flask-Login.

## Features

- User registration and login
- Submit reviews with ratings and comments
- Admin dashboard for managing reviews
- View all reviews and average ratings

## Admin User Details

- **Username**: admin
- **Email ID**: admin@example.com
- **Password**: admin123

### Admin Role
The admin user has the following capabilities within the application:

- Access to the admin dashboard.
- Ability to view all reviews submitted by users.
- Approve or delete reviews.
- Manage user feedback and statistics.

### Initial Setup
When you run the `init_db.py` script, it checks if the admin user already exists in the database. If not, it creates the admin user with the above credentials. This ensures that you have an admin account ready to manage the application right after the database is initialized.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (for database)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd review_system
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## Usage

- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- Navigate to `http://127.0.0.1:5000/admin` in your web browser to access the admin page.
- for admin use admin details for login.
- Use the admin credentials provided above to log in to the admin dashboard.
  

## License

This project is licensed under the MIT License.
