"""
CODSOFT ML Internship - Task 2: Credit Card Fraud Detection
============================================================
Detects fraudulent credit card transactions using:
- Logistic Regression
- Decision Tree
- Random Forest

Dataset: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, accuracy_score)
from sklearn.utils import resample
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load Data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 2 : Credit Card Fraud Detection")
print("=" * 60)

# Replace 'creditcard.csv' with your downloaded dataset path
df = pd.read_csv("creditcard.csv")

print(f"\nDataset shape : {df.shape}")
print(f"Fraud cases   : {df['Class'].sum()} ({df['Class'].mean()*100:.2f}%)")
print(f"Legit cases   : {(df['Class'] == 0).sum()}")

# ── 2. Pre-processing ─────────────────────────────────────────────────────────
# Scale 'Amount' and 'Time' (PCA features V1-V28 are already scaled)
scaler = StandardScaler()
df["scaled_amount"] = scaler.fit_transform(df[["Amount"]])
df["scaled_time"]   = scaler.fit_transform(df[["Time"]])
df.drop(["Amount", "Time"], axis=1, inplace=True)

X = df.drop("Class", axis=1)
y = df["Class"]

# ── 3. Handle Class Imbalance via Under-sampling ──────────────────────────────
df_majority = df[df.Class == 0]
df_minority = df[df.Class == 1]

df_majority_down = resample(df_majority,
                            replace=False,
                            n_samples=len(df_minority) * 10,  # 10:1 ratio
                            random_state=42)

df_balanced = pd.concat([df_majority_down, df_minority])
print(f"\nBalanced dataset: {df_balanced.shape}  |  Fraud: {df_balanced['Class'].mean()*100:.1f}%")

X_bal = df_balanced.drop("Class", axis=1)
y_bal = df_balanced["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X_bal, y_bal, test_size=0.2, random_state=42, stratify=y_bal)

# ── 4. Train & Evaluate Models ────────────────────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree"      : DecisionTreeClassifier(max_depth=6, random_state=42),
    "Random Forest"      : RandomForestClassifier(n_estimators=100, n_jobs=-1,
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
                                target_names=["Legitimate", "Fraud"]))
    print("  Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    results[name] = {"accuracy": acc, "roc_auc": roc_auc, "model": model}

# ── 5. Best Model Summary ─────────────────────────────────────────────────────
best = max(results, key=lambda k: results[k]["roc_auc"])
print(f"\n{'='*60}")
print(f"  Best Model : {best}")
print(f"  ROC-AUC    : {results[best]['roc_auc']:.4f}")
print(f"{'='*60}")

# ── 6. Predict on a Single Sample ────────────────────────────────────────────
print("\n[Demo] Predicting on first 5 test samples:")
sample = X_test.head(5)
preds  = results[best]["model"].predict(sample)
labels = ["Legitimate" if p == 0 else "FRAUD ⚠️" for p in preds]
for i, label in enumerate(labels):
    print(f"  Sample {i+1}: {label}")
