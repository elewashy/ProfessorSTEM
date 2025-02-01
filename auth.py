import re
import bcrypt
from flask import redirect, url_for, render_template, request, session, flash
from db import get_db_connection

def signup(request):
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            with get_db_connection() as conn:
                with conn.cursor(buffered=True) as cur:
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                    if cur.fetchone():
                        flash("Email already registered, please log in.", "error")
                        return redirect(url_for('signup_page'))

                    cur.execute("INSERT INTO users (username, full_name, email, password) VALUES (%s, %s, %s, %s)", 
                                (username, full_name, email, hashed_password.decode('utf-8')))
                    conn.commit()

                    flash("You have successfully registered!", "success")
                    
        except Exception as e:
            print(f"Error: {e}")
            flash("Internal server error", "error")
            return redirect(url_for('signup_page'))

        return redirect(url_for('signin_page'))

    return render_template('signup.html')

def signin(request):
    if request.method == 'POST':
        email_or_username = request.form['logemail']
        password = request.form['logpass']

        if re.match(r"[^@]+@[^@]+\.[^@]+", email_or_username):
            identifier = "email"
        else:
            identifier = "username"

        try:
            with get_db_connection() as conn:
                with conn.cursor(buffered=True) as cur:

                    if identifier == "email":
                        cur.execute("SELECT password FROM users WHERE email = %s", (email_or_username,))
                    else:
                        cur.execute("SELECT password FROM users WHERE username = %s", (email_or_username,))

                    user = cur.fetchone()
                    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                        session['user'] = email_or_username
                        flash("Login successful!", "success")
                        return redirect(url_for('dashboard'))
                    else:
                        flash("Invalid email/username or password", "error")
                        return redirect(url_for('signin_page')) 
        except Exception as e:
            print(f"Error: {e}")
            flash("Internal server error. Please try again later.", "error")
            return redirect(url_for('signin_page'))
    return render_template('signin.html')
