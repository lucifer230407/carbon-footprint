import pandas as pd
import numpy as np

def detect_anomaly(current_value, history):
    mean = np.mean(history)
    std = np.std(history)

    z_score = (current_value - mean) / std

    if abs(z_score) > 2:
        return True, round(z_score, 2)   # Anomaly
    else:
        return False, round(z_score, 2)  # Normal
