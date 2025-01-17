import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# الاتصال بقاعدة البيانات (أو إنشاءها إذا لم تكن موجودة)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# استدعاء دالة إنشاء قاعدة البيانات عند تشغيل التطبيق لأول مرة
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(f"Received data: username={username}, email={email}, password={password}")

        # التحقق إذا كان البريد الإلكتروني موجودًا بالفعل
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        print(f"User lookup result: {user}")

        if user:
            return "Email already registered, please log in."

        # إضافة المستخدم الجديد إلى قاعدة البيانات
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()
        print("User added successfully.")
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error during signup: {e}")
        return "An error occurred during signup."

@app.route('/login', methods=['POST'])
def login():
    email = request.form['logemail']
    password = request.form['logpass']
    
    # التحقق من بيانات المستخدم في قاعدة البيانات
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
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
