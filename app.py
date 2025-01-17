import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# اتصال بقاعدة البيانات
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))  # رابط الاتصال موجود كمتغير بيئي
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # التحقق إذا كان البريد الإلكتروني موجودًا بالفعل
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if user:
        conn.close()
        return "Email already registered, please log in."

    # إضافة المستخدم الجديد إلى قاعدة البيانات
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['logemail']
    password = request.form['logpass']

    conn = get_db_connection()
    cur = conn.cursor()
    
    # التحقق من بيانات المستخدم
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = email
        return redirect(url_for('dashboard'))
    return "Invalid email or password"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
