import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from supabase_config import get_supabase_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


def create_users_table():
    supabase = get_supabase_client()

    # إنشاء الجدول إذا لم يكن موجودًا
    try:
        supabase.postgrest.rpc(
            "create_table",
            {
                "table_name": "users",
                "columns": [
                    {"name": "id", "type": "serial", "constraints": "PRIMARY KEY"},
                    {"name": "username", "type": "varchar(100)", "constraints": "NOT NULL"},
                    {"name": "email", "type": "varchar(100)", "constraints": "UNIQUE NOT NULL"},
                    {"name": "password", "type": "varchar(255)", "constraints": "NOT NULL"},
                ]
            }
        )
        print("Table 'users' created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # التحقق من البريد الإلكتروني
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    return "Email already registered, please log in."

                # إدخال المستخدم
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                            (username, email, hashed_password.decode('utf-8')))
                conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        return "Internal server error", 500

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['logemail']
    password = request.form['logpass']

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT password FROM users WHERE email = %s", (email,))
                user = cur.fetchone()
                if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                    session['user'] = email
                    return redirect(url_for('dashboard'))
                else:
                    return "Invalid email or password"
    except Exception as e:
        print(f"Error: {e}")
        return "Internal server error", 500

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    create_users_table()  # إنشاء الجدول تلقائيًا
    app.run(debug=True)
