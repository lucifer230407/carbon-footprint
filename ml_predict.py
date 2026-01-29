import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "future_emission_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_future(travel_km, electricity, fuel):
    X_new = np.array([[travel_km, electricity, fuel]])
    return round(float(model.predict(X_new)[0]), 2)
