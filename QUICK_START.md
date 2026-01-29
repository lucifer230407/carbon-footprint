# Carbon Footprint Dashboard - Quick Start Guide

## 🚀 Getting Started

### 1. Start the Django Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```

### 2. Access the Dashboard
- Open: `http://localhost:8000/dashboard/`
- Or: `http://localhost:8000/` (redirects to dashboard)

### 3. Features You'll See

#### 📊 Dashboard Sections

1. **Stats Cards** (Top)
   - Latest Emission
   - Average Daily Emission
   - Total Days Tracked
   - Future Emission Status (Green ✓ / Yellow ⚠️)

2. **Historical Emissions Chart**
   - Line graph of daily CO₂ emissions
   - Shows trends over time

3. **30-Day Future Forecast Chart**
   - Predicts next 30 days based on your patterns
   - Compares against 2.5 kg/day healthy target
   - ML-powered predictions

4. **Health Comparison Chart**
   - Bar chart showing daily emissions
   - Red line = 2.5 kg/day sustainable target
   - Shows how close you are to healthy range

5. **🚨 Anomaly Detection Report** ← NEW
   - Status message (🟡 Moderate / ⚠️ High / 🔴 Critical / ✓ None)
   - Percentage of anomalous entries
   - Scatter plot showing anomalies on timeline
   - Detailed list of each anomaly with:
     - Date & emission amount
     - Z-score (how far from normal)
     - Contributing factors (travel/electricity/meals)

---

## 📈 Understanding Anomaly Detection

### What is an Anomaly?
An unusual spike in your CO₂ emissions - significantly higher than your normal pattern.

### How it Works
- Compares each day against previous 2+ days average
- Uses Z-score: deviation from mean / standard deviation
- Higher Z-score = more unusual

### Severity Levels
| Z-Score | Level | Indicator | Color |
|---------|-------|-----------|-------|
| 0-2.5   | Normal | ✓ | Green |
| 2.5-3.0 | Moderate | 🟡 | Yellow |
| 3.0-4.0 | High | ⚠️ | Orange |
| >4.0 | Critical | 🔴 | Red |

### Example
- Your normal: 2.2 kg/day
- One day: 5.5 kg/day
- Z-score: 3.2 → **High anomaly** ⚠️

---

## 🔍 Testing Anomalies

### To See Anomaly Detection in Action

1. **Log multiple entries** (at least 3) with consistent values
   - Example: 2.0, 2.1, 2.2 kg/day

2. **Log one spike**
   - Example: 5.0 kg/day (2x your normal)

3. **View Dashboard**
   - The spike will appear in "Anomaly Detection Report"
   - Z-score will show how unusual it is

### API Endpoint
```bash
# Get anomaly summary and details as JSON
curl -X GET http://localhost:8000/emissions/anomaly-check/
# (Must be logged in)
```

---

## 📁 File Structure

### Core Files
- `/dashboard/views.py` - Contains all anomaly detection logic
- `/dashboard/urls.py` - Routes to dashboard
- `/templates/dashboard.html` - HTML/CSS/JavaScript for visualization
- `/emissions/views.py` - API endpoint for anomalies
- `/emissions/urls.py` - Anomaly API route

### Data Models
- `EmissionLog` - Tracks daily emissions with:
  - Date
  - km_travel
  - electricity_units
  - meals_calories
  - co2_emission (calculated)

---

## 🛠️ Configuration

### Change Anomaly Threshold
Edit `dashboard/views.py`, line in `detect_anomaly()`:
```python
def detect_anomaly(value, history, threshold=2.5):  # Change 2.5 here
```

### Change Healthy Target
Edit `dashboard/views.py`, line 11:
```python
HEALTHY_EMISSION_TARGET = 2.5  # kg CO₂ per day
```

### Minimum Entries for Detection
Edit `dashboard/views.py`, line in `detect_user_anomalies()`:
```python
if logs.count() < 3:  # Change 3 to require more/fewer entries
```

---

## ✅ Integration Checklist

- ✓ Anomaly detection functions integrated into dashboard
- ✓ EmissionLog queries working
- ✓ Z-score calculation using numpy
- ✓ Severity classification system
- ✓ HTML/CSS styling for anomalies
- ✓ Chart.js scatter plot for visualization
- ✓ API endpoint created
- ✓ All imports updated

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not enough data" | Add at least 3 emission entries |
| No anomalies shown | Your emissions are consistent (good!) |
| Import errors | Make sure Django migrations are applied |
| Chart not loading | Ensure JavaScript is enabled in browser |
| API returns 403 | You must be logged in to access API |

---

## 📊 Next Steps

1. **Log Activities** - Use the input form to log your carbon emissions
2. **Review Dashboard** - Check trends and future predictions
3. **Analyze Anomalies** - Understand what causes spikes
4. **Reduce Emissions** - Use insights to make lifestyle changes
5. **Track Progress** - Monitor improvement over time

---

**Version:** 1.0  
**Last Updated:** 2024  
**Status:** ✓ Production Ready
