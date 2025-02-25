from flask import Flask
from config import SECRET_KEY
import routes

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register routes
app.add_url_rule('/agents', view_func=routes.agents_home)
app.add_url_rule('/start_learning', view_func=routes.start_learning, methods=['POST'])
app.add_url_rule('/quiz', view_func=routes.quiz)
app.add_url_rule('/submit_answer', view_func=routes.submit_answer, methods=['POST'])
app.add_url_rule('/results', view_func=routes.results)
app.add_url_rule('/study_plan', view_func=routes.study_plan)

if __name__ == '__main__':
    app.run(debug=True)
