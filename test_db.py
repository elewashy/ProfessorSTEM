import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host="sql8.freesqldatabase.com",
        database="sql8759562",
        user="sql8759562",
        password="9NFjgHHJlI",
        port=3306
    )
    print("✅ Connected to the database successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
