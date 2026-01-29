import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "carbon_model.pkl"))

def predict_carbon(distance, electricity, calories, waste):
    X = [[distance, electricity, calories, waste]]
    return float(model.predict(X)[0])
