import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from config_agent import logger

def generate_synthetic_data(n_samples=100):
    np.random.seed(42)
    
    # Generate more realistic data with proper distributions
    quiz_scores = np.random.normal(10, 3, n_samples).clip(0, 15)  # Mean=10, SD=3
    time_per_question = np.random.normal(90, 30, n_samples).clip(30, 180)  # Mean=90s, SD=30s
    
    # Define proficiency thresholds based on percentiles
    score_threshold_high = np.percentile(quiz_scores, 70)
    score_threshold_low = np.percentile(quiz_scores, 30)
    time_threshold_high = np.percentile(time_per_question, 30)  # Faster times are better
    time_threshold_low = np.percentile(time_per_question, 70)
    
    # Determine levels based on both score and time
    levels = []
    for score, time in zip(quiz_scores, time_per_question):
        if score >= score_threshold_high and time <= time_threshold_high:
            levels.append('high')
        elif score <= score_threshold_low or time >= time_threshold_low:
            levels.append('low')
        else:
            levels.append('intermediate')
    
    return pd.DataFrame({
        'quiz_score': quiz_scores,
        'time_per_question': time_per_question,
        'level': levels
    })

def train_ml_model():
    try:
        # Generate synthetic training data
        df = generate_synthetic_data()
        
        # Split features and target
        X = df[['quiz_score', 'time_per_question']]
        y = df['level']
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model with optimized hyperparameters
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model accuracy: {accuracy:.2f}")
        
        return model, scaler
    except Exception as e:
        logger.error(f"Error training ML model: {str(e)}")
        return None, None

def assess_proficiency(model, scaler, correct_count, total_questions, total_time):
    try:
        if not all(isinstance(x, (int, float)) for x in [correct_count, total_questions, total_time]):
            raise ValueError("Invalid input types for proficiency assessment")
            
        if total_questions == 0:
            return "unknown"
            
        avg_time = total_time / total_questions
        
        # Scale the features
        features = np.array([[correct_count, avg_time]])
        features_scaled = scaler.transform(features)
        
        # Get prediction and probabilities
        prediction = model.predict(features_scaled)
        probabilities = model.predict_proba(features_scaled)
        
        # Log confidence level
        confidence = np.max(probabilities)
        logger.info(f"Prediction confidence: {confidence:.2f}")
        
        return prediction[0]
    except Exception as e:
        logger.error(f"Error assessing proficiency: {str(e)}")
        return "unknown"
