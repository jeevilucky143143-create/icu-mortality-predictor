import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report


def generate_synthetic_data(n=2000):
    np.random.seed(42)
    age          = np.random.randint(18, 90, n)
    heart_rate   = np.random.normal(90, 20, n).clip(40, 180)
    bp_systolic  = np.random.normal(120, 25, n).clip(60, 220)
    bp_diastolic = np.random.normal(75, 15, n).clip(30, 140)
    temperature  = np.random.normal(37.0, 1.0, n).clip(33, 42)
    spo2         = np.random.normal(95, 5, n).clip(60, 100)
    gcs_score    = np.random.randint(3, 16, n)
    creatinine   = np.random.exponential(1.2, n).clip(0.3, 10)
    wbc          = np.random.normal(10, 4, n).clip(1, 30)

    risk = (
        (age > 70)           * 0.30 +
        (heart_rate > 120)   * 0.20 +
        (bp_systolic < 90)   * 0.25 +
        (spo2 < 88)          * 0.30 +
        (gcs_score < 8)      * 0.35 +
        (creatinine > 3)     * 0.20 +
        np.random.normal(0, 0.1, n)
    )
    mortality = (risk > 0.5).astype(int)

    return pd.DataFrame({
        "age": age, "heart_rate": heart_rate,
        "bp_systolic": bp_systolic, "bp_diastolic": bp_diastolic,
        "temperature": temperature, "spo2": spo2,
        "gcs_score": gcs_score, "creatinine": creatinine,
        "wbc": wbc, "hospital_death": mortality
    })


def train_and_save():
    df       = generate_synthetic_data()
    features = ["age","heart_rate","bp_systolic","bp_diastolic",
                "temperature","spo2","gcs_score","creatinine","wbc"]
    X = df[features]
    y = df["hospital_death"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    scaler       = StandardScaler()
    X_train_sc   = scaler.fit_transform(X_train)
    X_test_sc    = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_sc, y_train)

    y_prob = model.predict_proba(X_test_sc)[:, 1]
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))
    print(classification_report(y_test, model.predict(X_test_sc)))

    joblib.dump(model,  "model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("✅ model.pkl and scaler.pkl saved.")


if __name__ == "__main__":
    train_and_save()
