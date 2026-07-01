from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os
from train_model import train_and_save

app = Flask(__name__)
CORS(app)

MODEL_PATH  = "model.pkl"
SCALER_PATH = "scaler.pkl"

if not os.path.exists(MODEL_PATH):
    print("Model not found — training now...")
    train_and_save()

model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


@app.route("/")
def index():
    return jsonify({"status": "ICU Mortality API running"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        features = [
            float(data["age"]),
            float(data["heart_rate"]),
            float(data["bp_systolic"]),
            float(data["bp_diastolic"]),
            float(data["temperature"]),
            float(data["spo2"]),
            float(data["gcs_score"]),
            float(data["creatinine"]),
            float(data["wbc"]),
        ]
        X        = np.array(features).reshape(1, -1)
        X_scaled = scaler.transform(X)
        prob     = model.predict_proba(X_scaled)[0][1]
        risk     = "Low" if prob < 0.35 else "Moderate" if prob < 0.65 else "High"
        return jsonify({
            "mortality_probability": round(float(prob) * 100, 2),
            "prediction":            int(prob >= 0.5),
            "risk_level":            risk
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
