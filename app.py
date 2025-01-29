import os
from flask import Flask, render_template, request, redirect, url_for, session
from auth import signin, signup
from db import get_db_connection

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return signup(request)

@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    return signin(request)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

if __name__ == "__main__":
    app.run(debug=True)
