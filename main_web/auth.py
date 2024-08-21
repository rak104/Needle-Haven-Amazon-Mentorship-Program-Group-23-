import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from flask_mail import Message
from flask_mail import Mail

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('signup-1.html')

@bp.route('/register_customer', methods=('GET', 'POST'))
def register_customer():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']

        db = get_db()
        error = None

        # Validation checks
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not first_name:
            error = 'First Name is required.'
        elif not last_name:
            error = 'Last Name is required.'
        elif not date_of_birth:
            error = 'Date of Birth is required.'

        if error is None:
            try:
                # Insert data into the database
                db.execute(
                    "INSERT INTO user (username, password_hash, email, first_name, last_name, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, first_name, last_name, date_of_birth),
                )
                db.commit()
                send_welcome_email(email, username)
                return redirect(url_for('auth.login'))  # Redirect to homepage after successful registration
            except db.IntegrityError:
                error = f"User {username} is already registered."
        flash(error)

    return render_template('signup-customer.html')  # Ensure you have a corresponding template

@bp.route('/register_store', methods=('GET', 'POST'))
def register_store():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phone_number']
        description = request.form['description']

        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not address:
            error = 'Address is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not description:
            error = 'Description is required.'

        if error is None:
            try:
                message = "Store Registration"
                message_body =  f"Store name: {name}\n"+ f"Store Password: {password}\n"+ f"Store Adress:{address}\n"+f"Store email:{email}\n"+ f"Store phone_number:{phone_number}\n"+f"Store description:{description}\n"
                send_store_email(message,message_body)
                conf = "Please wait for our confirmation!"
                flash(conf)
            except db.IntegrityError:
                error = f"User {name} is already registered."
                flash(error)

    return render_template('signup-store.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        # Check if the user is a regular user or a store
        user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        store = db.execute(
                'SELECT * FROM Store WHERE name = ?', (username,)
        ).fetchone()

        if user is not None:
            if not check_password_hash(user['password_hash'], password):
                error = 'Incorrect password.'
            else:
                session.clear()
                session['user_id'] = user['id']
                session['user_type'] = 'user'  # Save user type in session
                db.execute(
                    'UPDATE user SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],)
                )
                return redirect(url_for('blog.index'))
        elif store is not None:
            if not check_password_hash(store['password_hash'], password):
                error = 'Incorrect password.'
            else:
                session.clear()
                session['store_id'] = store['id']
                session['user_type'] = 'store'  # Save user type in session
                return redirect(url_for('blog.index'))
        else:
            error = 'Incorrect username.'
        
        flash(error)

    return render_template('login.html')


@bp.before_app_request
def load_a_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@bp.route('/logout')
def logout():
    # Clear the session
    session.clear()

    # Redirect to the login page or homepage
    return redirect(url_for('auth.login'))  # Assuming you have a common login page for both users and stores


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.signin'))
        return view(**kwargs)
    return wrapped_view

def send_welcome_email(to, username):
    with current_app.app_context():
        msg = Message("Welcome to Our Service", recipients=[to])
        msg.body = f"Hi {username},\n\nWelcome to Needle Haven We're glad to have you with us.\n\nBest Regards,\nDev Team"
        mail = Mail(current_app)  # Ensure mail is configured properly in your app
        mail.send(msg)


def send_store_email(message,message_body):
    with current_app.app_context():
        msg = Message(message, recipients=["needlehaven@hotmail.com"])
        msg.body = message_body
        mail = Mail(current_app)  # Ensure mail is configured properly in your app
        mail.send(msg)
