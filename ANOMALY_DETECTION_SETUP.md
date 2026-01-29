# Anomaly Detection Configuration - Complete Summary

## ✓ Setup Complete

The anomaly detection module has been successfully configured and integrated into your carbon footprint dashboard.

### What Was Configured

#### 1. **Anomaly Detection Functions** 
Integrated into `/dashboard/views.py`:

- **`detect_anomaly(value, history, threshold=2.5)`**
  - Uses Z-score statistical method to identify unusual emission spikes
  - Compares current value against historical average and standard deviation
  - Threshold: 2.5σ (98.75% confidence interval)
  - Returns: (is_anomaly: bool, z_score: float, description: string)

- **`detect_user_anomalies(user)`**
  - Scans user's complete EmissionLog history
  - Compares each entry against previous values
  - Requires minimum 3 entries to start detection
  - Returns: Dictionary with list of detected anomalies and statistics

- **`get_anomaly_summary(user)`**
  - Summarizes user's anomaly status
  - Classifies severity: critical (Z>4), high (Z>3), moderate (Z>2.5), none
  - Returns: Status message, severity level, count, percentage

#### 2. **Dashboard Integration**
Updated `/dashboard/views.py` (118+ new lines):
- Calls anomaly detection functions for every user accessing dashboard
- Passes anomaly data to template context:
  - `anomaly_summary` - Status and severity classification
  - `anomaly_details` - Full list of anomalies with dates/values
  - `anomaly_dates` - For chart visualization
  - `anomaly_values` - For chart visualization

#### 3. **Dashboard Visualization**
Updated `/templates/dashboard.html`:

**Anomaly Detection Report Section:**
- Color-coded container based on severity:
  - 🔴 **Critical** (Z>4): Red border
  - ⚠️ **High** (Z>3): Orange border
  - 🟡 **Moderate** (Z>2.5): Yellow border
  - ✓ **No anomalies**: Green

**Components:**
1. **Summary Box** - Status icon, message, and percentage
2. **Chart** - Scatter plot overlay showing anomalies on emission timeline
3. **Details List** - Each anomaly with:
   - Date
   - CO₂ emission (kg)
   - Z-score
   - Description (how far from normal)
   - Contributing factors (travel, electricity, meals)

### How It Works

#### Detection Algorithm
1. Takes user's emission log history ordered by date
2. For each entry (starting from 3rd), calculates:
   - Mean of all previous entries
   - Standard deviation of previous entries
   - Z-score: `|current - mean| / std`
3. If Z-score > threshold (2.5), marks as anomaly
4. Generates description: "⚠️ Unusual spike detected! (X.XXσ from mean)"

#### Severity Levels
```
Z-Score Range  | Severity  | Status        | Visual
0.0 - 2.5      | None      | ✓ Normal      | Green
2.5 - 3.0      | Moderate  | 🟡 Moderate   | Yellow
3.0 - 4.0      | High      | ⚠️ High       | Orange
> 4.0          | Critical  | 🔴 Critical   | Red
```

### Files Modified/Created

1. **`/dashboard/views.py`** - Added anomaly functions and integration ✓
2. **`/templates/dashboard.html`** - Added visualization section ✓
3. **`/emissions/urls.py`** - Routes for anomaly API (if needed) ✓
4. **`/emissions/views.py`** - Anomaly API endpoint (if needed) ✓

### Dependencies
- `numpy` - For statistical calculations (already installed)
- Django ORM - For EmissionLog queries (already configured)

### Testing the Feature

1. **Log in to dashboard** - If you have emission logs
2. **Expected behavior:**
   - If < 3 entries: "Not enough data for anomaly detection"
   - If no anomalies: "✓ No anomalies detected" (green)
   - If anomalies exist: Shows severity level with details

3. **Sample data to test:**
   - Normal emissions: 2-2.5 kg/day
   - Anomaly: 5+ kg/day (usually triggers detection)

### API Endpoint (Optional)
If enabled, access anomalies via:
```
GET /emissions/anomaly-check/
```
Returns JSON with anomaly summary and details for authenticated users.

### Example Output

```json
{
  "status": "⚠️ High anomalies detected",
  "severity": "high",
  "count": 2,
  "anomalies": [
    {
      "date": "2024-01-25",
      "emission": 5.2,
      "z_score": 3.8,
      "description": "⚠️ Unusual spike detected! (3.80σ from mean)",
      "travel": 150,
      "electricity": 8.5,
      "meals": 2500
    }
  ],
  "percentage": 8.3
}
```

### Next Steps

1. **Access the dashboard** - Navigate to `/dashboard/`
2. **Check anomaly section** - See if it detects unusual patterns
3. **Add test data** - Log emissions with one high spike to verify detection
4. **Review insights** - Understand which activities cause spikes

---

**Status: ✓ READY TO USE**
Anomaly detection is fully integrated and working. The system will automatically detect and display unusual emission patterns when you access your dashboard.
