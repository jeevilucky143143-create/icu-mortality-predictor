# ICU Mortality Predictor — Render Deployment

```
icu_render/
├── backend/
│   ├── app.py
│   ├── train_model.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── render.yaml
└── README.md
```

---

## Local Run

```bash
cd backend
pip install -r requirements.txt
python app.py          # trains model then starts on :5000
```
Open `frontend/index.html` in browser, paste `http://localhost:5000` as the backend URL.

---

## Deploy to Render — Step by Step

### STEP 1 — Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
# create a repo on github.com then:
git remote add origin https://github.com/YOUR_USERNAME/icu-mortality.git
git push -u origin main
```

### STEP 2 — Deploy Backend on Render
1. Go to https://render.com → Sign up / Log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account → select your repo
4. Fill in:
   - **Name**: `icu-mortality-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python train_model.py`
   - **Start Command**: `gunicorn app:app`
5. Click **"Create Web Service"**
6. Wait ~3 min for build. Copy the URL shown (e.g. `https://icu-mortality-api.onrender.com`)

### STEP 3 — Deploy Frontend on Render
1. Click **"New +"** → **"Static Site"**
2. Select the same GitHub repo
3. Fill in:
   - **Name**: `icu-mortality-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: *(leave empty)*
   - **Publish Directory**: `.`
4. Click **"Create Static Site"**
5. Wait ~1 min. You'll get a URL like `https://icu-mortality-frontend.onrender.com`

### STEP 4 — Connect Frontend to Backend
1. Open your frontend URL in browser
2. Paste your **backend URL** in the `BACKEND URL` field at the top
3. The status dot turns 🟢 green when connected
4. Enter patient vitals → click **Run Prediction**

---

## API Reference

**POST** `/predict`
```json
{
  "age": 70, "heart_rate": 115, "bp_systolic": 88,
  "bp_diastolic": 55, "temperature": 38.5,
  "spo2": 87, "gcs_score": 7, "creatinine": 3.5, "wbc": 16.2
}
```
Response:
```json
{ "mortality_probability": 82.4, "prediction": 1, "risk_level": "High" }
```

**GET** `/health` → `{ "status": "ok" }`

---

> ⚠ Educational project only. Not for clinical use.
