"""
CODSOFT ML Internship - Task 3: Customer Churn Prediction
==========================================================
Predicts whether a customer will churn using:
- Logistic Regression
- Random Forest
- Gradient Boosting

Dataset: https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction
         (Churn_Modelling.csv)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, roc_auc_score)
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load Data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 3 : Customer Churn Prediction")
print("=" * 60)

# Replace with your downloaded dataset path
df = pd.read_csv("Churn_Modelling.csv")

print(f"\nDataset shape : {df.shape}")
print(f"Churn rate    : {df['Exited'].mean()*100:.1f}%")
print(f"\nFirst 3 rows:\n{df.head(3)}")

# ── 2. Pre-processing ─────────────────────────────────────────────────────────
# Drop irrelevant columns
df.drop(["RowNumber", "CustomerId", "Surname"], axis=1, inplace=True)

# Encode categorical columns
le = LabelEncoder()
df["Geography"] = le.fit_transform(df["Geography"])   # France/Spain/Germany → 0/1/2
df["Gender"]    = le.fit_transform(df["Gender"])      # Male/Female → 0/1

print(f"\nFeatures after encoding:\n{df.dtypes}")

X = df.drop("Exited", axis=1)
y = df["Exited"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# ── 3. Train & Evaluate Models ────────────────────────────────────────────────
models = {
    "Logistic Regression" : LogisticRegression(max_iter=500, random_state=42),
    "Random Forest"       : RandomForestClassifier(n_estimators=100,
                                                   random_state=42, n_jobs=-1),
    "Gradient Boosting"   : GradientBoostingClassifier(n_estimators=100,
                                                       learning_rate=0.1,
                                                       random_state=42),
}

results = {}

for name, model in models.items():
    print(f"\n{'─'*50}")
    print(f"  Model : {name}")
    print(f"{'─'*50}")

    model.fit(X_train, y_train)
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc     = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    print(f"  Accuracy : {acc*100:.2f}%")
    print(f"  ROC-AUC  : {roc_auc:.4f}")
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["Retained", "Churned"]))
    print("  Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    results[name] = {"accuracy": acc, "roc_auc": roc_auc, "model": model}

# ── 4. Feature Importance (Random Forest) ────────────────────────────────────
rf_model   = results["Random Forest"]["model"]
feat_names = df.drop("Exited", axis=1).columns
importances = pd.Series(rf_model.feature_importances_, index=feat_names)
importances = importances.sort_values(ascending=False)

print(f"\n{'='*60}")
print("  Top Feature Importances (Random Forest):")
print(f"{'='*60}")
for feat, imp in importances.items():
    bar = "█" * int(imp * 50)
    print(f"  {feat:<20} {bar} {imp:.4f}")

# ── 5. Best Model Summary ─────────────────────────────────────────────────────
best = max(results, key=lambda k: results[k]["roc_auc"])
print(f"\n{'='*60}")
print(f"  Best Model : {best}")
print(f"  ROC-AUC    : {results[best]['roc_auc']:.4f}")
print(f"  Accuracy   : {results[best]['accuracy']*100:.2f}%")
print(f"{'='*60}")

# ── 6. Demo Prediction ────────────────────────────────────────────────────────
print("\n[Demo] Predict churn for a sample customer:")
sample_customer = pd.DataFrame([{
    "CreditScore": 650, "Geography": 0, "Gender": 1, "Age": 35,
    "Tenure": 5, "Balance": 50000.0, "NumOfProducts": 2,
    "HasCrCard": 1, "IsActiveMember": 1, "EstimatedSalary": 60000.0
}])

sample_scaled = scaler.transform(sample_customer)
pred    = results[best]["model"].predict(sample_scaled)[0]
prob    = results[best]["model"].predict_proba(sample_scaled)[0][1]
outcome = "Will Churn ⚠️" if pred == 1 else "Will Stay ✅"
print(f"  Prediction : {outcome}  (churn probability: {prob:.2%})")
