import re
import bcrypt
from flask import redirect, url_for, render_template, request, session
from db import get_db_connection

# دالة التسجيل
def signup(request):
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        # هاش للباسورد
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            with get_db_connection() as conn:
                with conn.cursor(buffered=True) as cur:
                    # التحقق من وجود الإيميل
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                    if cur.fetchone():
                        return "Email already registered, please log in."

                    # إدخال البيانات
                    cur.execute("INSERT INTO users (username, full_name, email, password) VALUES (%s, %s, %s, %s)", 
                                (username, full_name, email, hashed_password.decode('utf-8')))
                    conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            return "Internal server error", 500

        return redirect(url_for('signin_page'))

    return render_template('signup.html')

# دالة تسجيل الدخول
def signin(request):
    if request.method == 'POST':
        email_or_username = request.form['logemail']
        password = request.form['logpass']

        # التحقق إذا كان المدخل هو بريد إلكتروني
        if re.match(r"[^@]+@[^@]+\.[^@]+", email_or_username):
            identifier = "email"
        else:
            identifier = "username"

        try:
            with get_db_connection() as conn:
                with conn.cursor(buffered=True) as cur:
                    # اختيار الاستعلام حسب النوع (إيميل أو يوزر نيم)
                    if identifier == "email":
                        cur.execute("SELECT password FROM users WHERE email = %s", (email_or_username,))
                    else:
                        cur.execute("SELECT password FROM users WHERE username = %s", (email_or_username,))

                    user = cur.fetchone()
                    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                        session['user'] = email_or_username
                        return redirect(url_for('dashboard'))
                    else:
                        return "Invalid email/username or password", 401  # Unauthorized

        except Exception as e:
            print(f"Error: {e}")
            return "Internal server error", 500

    return render_template('signin.html')
