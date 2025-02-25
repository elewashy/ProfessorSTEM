from flask import Flask
from config_agent import SECRET_KEY
import routes

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register routes

if __name__ == '__main__':
    app.run(debug=True)
