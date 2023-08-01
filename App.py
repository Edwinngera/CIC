from flask import Flask, render_template, redirect, url_for, flash
from form import RegistrationForm, LoginForm, ProfileUpdateForm
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'edwin1234'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_app_db'

db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = db.cursor()
        username = form.username.data
        password = form.password.data

        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            flash('Username is already taken.', 'danger')
            return redirect(url_for('register'))

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        db.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = db.cursor()
        username = form.username.data
        password = form.password.data

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            flash('Login successful.', 'success')
            return redirect(url_for('profile'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        cursor = db.cursor()
        username = form.username.data
        password = form.password.data

        cursor.execute('UPDATE users SET password = %s WHERE username = %s', (password, username))
        db.commit()

        flash('Profile updated successfully.', 'success')

    return render_template('profile.html', form=form)

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
