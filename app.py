import os
from flask import Flask, render_template, request, redirect, url_for, session
from auth import signin, signup
from db import get_db_connection
from config_agent import SECRET_KEY
import routes

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return signup(request)

@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    return signin(request)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html') 

@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session or session.get('role') != 'user':
        return redirect(url_for('home'))
    return render_template('user_dashboard.html') 

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

app.add_url_rule('/user_training', view_func=routes.user_training)
app.add_url_rule('/start_learning', view_func=routes.start_learning, methods=['POST'])
app.add_url_rule('/quiz', view_func=routes.quiz)
app.add_url_rule('/submit_answer', view_func=routes.submit_answer, methods=['POST'])
app.add_url_rule('/results', view_func=routes.results)
app.add_url_rule('/study_plan', view_func=routes.study_plan)

if __name__ == "__main__":
    app.run(debug=True)
