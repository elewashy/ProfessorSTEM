import time
import google.generativeai as genai
from config_agent import logger, CENTRAL_API_KEY, MATH_API_KEY, SCIENCE_API_KEY

# Configure Gemini clients
try:
    genai.configure(api_key=CENTRAL_API_KEY)
    central_model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

    genai.configure(api_key=MATH_API_KEY)
    math_model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

    genai.configure(api_key=SCIENCE_API_KEY)
    science_model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

except Exception as e:
    logger.error(f"Error initializing Generative AI models: {str(e)}")
    raise

class SubjectAgent:
    def __init__(self, model):
        self.model = model
        
    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            time.sleep(0.5)
            return response.text
        except genai.exceptions.ApiError as e:
            logger.error(f"API Error: {str(e)}")
            return f"API Error: {e}"
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return f"Unexpected Error: {str(e)}"

class CentralAgent:
    def __init__(self):
        self.math_agent = SubjectAgent(math_model)
        self.science_agent = SubjectAgent(science_model)
        self.ml_model, self.scaler = self._init_ml()

    def _init_ml(self):
        from ml_model import train_ml_model
        return train_ml_model()

    def generate_quiz(self, topic, grade):
        if not isinstance(topic, str) or not isinstance(grade, int):
            raise ValueError("Invalid topic or grade format")
            
        prompt = f"""
        Generate a 15-question MCQ Exam on {topic} for grade {grade}.
        Format each question exactly like:
        [Question X] What is the question text? | Option 1 | Option 2 | Option 3 | Option 4 | Correct Answer

        Example:
        [Question 1] What is 2+2? | 3 | 4 | 5 | 6 | 4

        Make questions progressively harder and include:
        1. Basic recall questions (33%)
        2. Understanding/application questions (33%)
        3. Analysis/problem-solving questions (34%)
        """
        return self.math_agent.generate_content(prompt)

    def parse_quiz(self, quiz_text):
        if not isinstance(quiz_text, str):
            logger.error("Invalid quiz text format")
            return []
            
        try:
            questions = []
            for line in quiz_text.split("\n"):
                if line.strip() and "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 6:
                        question_text = parts[0]
                        if "[Question" in question_text:
                            question_text = question_text.split("]", 1)[1].strip()
                        
                        questions.append({
                            "question": question_text,
                            "options": parts[1:-1],
                            "answer": parts[-1]
                        })
            return questions
        except Exception as e:
            logger.error(f"Error parsing quiz: {str(e)}")
            return []

    def assess_proficiency(self, correct_count, total_questions, total_time):
        from ml_model import assess_proficiency
        return assess_proficiency(
            self.ml_model, 
            self.scaler, 
            correct_count, 
            total_questions, 
            total_time
        )
