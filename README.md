# 🌍 Carbon Footprint Tracker

A full-stack Django web application that helps users track, analyze, and reduce their personal carbon emissions — powered by ML-based predictions and intelligent anomaly detection.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat&logo=django&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?style=flat&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📌 Overview

Carbon Footprint Tracker is a data-driven Django application that allows users to log daily activities, calculate their CO₂ emissions, and receive intelligent insights through an ML-powered anomaly detection system. The app features a dynamic dashboard with real-time visualizations, a chatbot assistant, and emission forecasting — all in one place.

---

## ✨ Features

- **Activity Logging** — Log daily activities across transport, energy, food, and lifestyle categories
- **CO₂ Emission Calculation** — Automatic emission estimates per activity using established emission factors
- **ML Predictions** — Emission forecasting using trained TensorFlow/scikit-learn models
- **Anomaly Detection** — Z-score based statistical analysis to flag unusual emission spikes (4-tier severity system)
- **Interactive Dashboard** — Plotly + Chart.js visualizations including trend graphs, anomaly scatter plots, and daily breakdowns
- **Chatbot Assistant** — Integrated chat interface for sustainability tips and Q&A
- **User Authentication** — Secure registration, login, and per-user data isolation
- **REST API** — JSON endpoint for anomaly data at `/emissions/anomaly-check/`
- **Responsive UI** — Clean HTML/CSS frontend, mobile-friendly

---

## 🗂️ Project Structure

```
carbon-footprint/
├── activities/          # Activity models and emission factor logic
├── carbon_tracker/      # Django project settings and root URLs
├── chatbot/             # Chatbot module
├── dashboard/           # Dashboard views, anomaly detection logic
├── emissions/           # EmissionLog models, API endpoint
├── ml/                  # ML models and prediction scripts
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── users/               # User auth (register, login, profile)
├── manage.py
├── requirements.txt
├── Procfile             # Deployment config (Gunicorn)
├── anomaly_detection.py
├── ml_predict.py
└── config.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Django REST Framework |
| ML / Data | TensorFlow 2.20, Keras, scikit-learn, NumPy, pandas, SciPy |
| Visualization | Plotly, Chart.js, Matplotlib |
| Database | SQLite (dev) / PostgreSQL (prod via psycopg2) |
| Frontend | HTML5, CSS3, JavaScript |
| Deployment | Gunicorn, Procfile |
| Auth | Django built-in auth |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/lucifer230407/carbon-footprint.git
cd carbon-footprint
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python3 manage.py migrate
```

### 5. (Optional) Add test data

```bash
python3 add_test_data.py
```

### 6. Start the development server

```bash
python3 manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## 📊 Anomaly Detection

The dashboard includes an intelligent **Anomaly Detection Report** powered by Z-score statistical analysis.

### Severity Levels

| Severity | Condition | Indicator |
|----------|-----------|-----------|
| Critical | Z > 4.0 | 🔴 Extreme spike |
| High | 3.0 < Z ≤ 4.0 | ⚠️ Major spike |
| Moderate | 2.5 < Z ≤ 3.0 | 🟡 Noticeable spike |
| Normal | Z ≤ 2.5 | ✅ Within range |

### Configuration

Thresholds can be adjusted in `dashboard/views.py`:

```python
HEALTHY_EMISSION_TARGET = 2.5   # kg CO₂/day
def detect_anomaly(value, history, threshold=2.5):  # Z-score cutoff
```

### Verify the system

```bash
python3 verify_anomalies.py
```

---

## 🔌 API Endpoint

```
GET /emissions/anomaly-check/
```

Returns a JSON response with anomaly data for the authenticated user.  
**Authentication required.**

---

## 🧪 Running Tests

```bash
python3 manage.py test
python3 test_predictions.py
python3 test_anomalies.py
python3 verify_anomalies.py     # 7 automated system checks
```

---

## 🚀 Deployment

The project includes a `Procfile` for Gunicorn-based deployment (e.g., Heroku, Railway):

```
web: gunicorn carbon_tracker.wsgi
```

For production, configure:
- `DEBUG = False` in `settings.py`
- PostgreSQL connection via `psycopg2-binary`
- Environment variables via `python-dotenv`

---

## 📈 Performance

- Anomaly calculation: < 50ms per user
- Single DB query per dashboard load
- Scales efficiently to 100k+ emission entries

---

## 🔐 Security

- All views require user authentication
- Users only see their own data
- CSRF protection on all forms
- Database queries parameterized (no SQL injection)

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👤 Author

**Himanshu Jangra**  
B.E. CSE (AI/ML) — Chitkara University  
GitHub: [@lucifer230407](https://github.com/lucifer230407)

---

## 📄 License

This project is licensed under the MIT License.
