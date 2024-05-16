from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def home():
    return render_template('index.html')  # Update to your homepage template name

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash("Passwords do not match.", 'error')
            return redirect('/register')  # Redirect back to registration page

        # Check if username or email already exists in the database
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", 'error')
            return redirect('/register')  # Redirect back to registration page

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", 'error')
            return redirect('/register')  # Redirect back to registration page

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(email=email, phone=phone, username=username, password=hashed_password)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')  # Update to your registration page template name

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query user from database based on username
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login, set user session
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials, show error message
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 561
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ultralegend404@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ultra001#1'

mail = Mail(app)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        # Check if username exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            # Generate a temporary password reset token (for demonstration)
            temp_token = secrets.token_urlsafe(16)  # Generate a temporary token

            # Save the token to the user record (in real use, store in a database)
            user.password_reset_token = temp_token
            db.session.commit()

            # Send password reset email
            reset_url = url_for('reset_password', token=temp_token, _external=True)
            msg = Message(subject='Password Reset Request',
                          recipients=[user.email],
                          body=f'Hi {user.username},\n\n'
                               f'Please click the following link to reset your password:\n'
                               f'{reset_url}\n\n'
                               f'If you did not request this, please ignore this email.\n\n'
                               f'Best regards,\nYour Website Team')
            mail.send(msg)

            flash("Password reset instructions sent to your email. Check your inbox.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Username not found. Please try again.", 'error')

    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')

    if request.method == 'POST':
        new_password = request.form['new_password']

        # Find user by reset token
        user = User.query.filter_by(reset_token=token).first()

        if user:
            # Hash the new password
            hashed_password = generate_password_hash(new_password)
            
            # Update user's password and reset token
            user.password = hashed_password
            user.reset_token = None
            db.session.commit()

            flash("Password reset successful. You can now log in with your new password.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Invalid or expired token. Please try again.", 'error')

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
