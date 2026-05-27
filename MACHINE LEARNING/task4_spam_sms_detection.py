"""
CODSOFT ML Internship - Task 4: Spam SMS Detection
====================================================
Classifies SMS messages as Spam or Ham (legitimate) using:
- TF-IDF Vectorization
- Naive Bayes
- Logistic Regression
- Support Vector Machine (SVM)

Dataset: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
         (spam.csv)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score)
import re
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load Data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 4 : Spam SMS Detection")
print("=" * 60)

# Replace with your downloaded dataset path
df = pd.read_csv("spam.csv", encoding="latin-1")[["v1", "v2"]]
df.columns = ["label", "message"]

print(f"\nDataset shape  : {df.shape}")
print(f"Spam messages  : {(df['label']=='spam').sum()}")
print(f"Ham  messages  : {(df['label']=='ham').sum()}")
print(f"\nSample messages:")
print(df.sample(4, random_state=1).to_string(index=False))

# ── 2. Pre-processing ─────────────────────────────────────────────────────────
def clean_text(text):
    """Lowercase, remove punctuation and extra spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_msg"] = df["message"].apply(clean_text)

# Encode labels: spam=1, ham=0
df["label_enc"] = (df["label"] == "spam").astype(int)

X = df["clean_msg"]
y = df["label_enc"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ── 3. TF-IDF Vectorization ───────────────────────────────────────────────────
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),   # unigrams + bigrams
    stop_words="english"
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf  = tfidf.transform(X_test)

print(f"\nTF-IDF matrix shape: {X_train_tfidf.shape}")

# ── 4. Train & Evaluate Models ────────────────────────────────────────────────
models = {
    "Naive Bayes"        : MultinomialNB(alpha=0.1),
    "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
    "SVM (LinearSVC)"    : LinearSVC(random_state=42),
}

results = {}

for name, model in models.items():
    print(f"\n{'─'*50}")
    print(f"  Model : {name}")
    print(f"{'─'*50}")

    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)
    acc    = accuracy_score(y_test, y_pred)

    print(f"  Accuracy : {acc*100:.2f}%")
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["Ham", "Spam"]))
    print("  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  [[TN={cm[0,0]}  FP={cm[0,1]}]\n   [FN={cm[1,0]}  TP={cm[1,1]}]]")

    results[name] = {"accuracy": acc, "model": model}

# ── 5. Best Model ─────────────────────────────────────────────────────────────
best = max(results, key=lambda k: results[k]["accuracy"])
print(f"\n{'='*60}")
print(f"  Best Model : {best}")
print(f"  Accuracy   : {results[best]['accuracy']*100:.2f}%")
print(f"{'='*60}")

# ── 6. Top Spam Keywords ──────────────────────────────────────────────────────
if best == "Naive Bayes":
    nb_model = results["Naive Bayes"]["model"]
    feature_names = tfidf.get_feature_names_out()
    spam_idx = 1  # class index for spam
    top_spam_features = np.argsort(nb_model.feature_log_prob_[spam_idx])[-15:][::-1]
    print("\n  Top 15 Spam Keywords (Naive Bayes log-probabilities):")
    for idx in top_spam_features:
        print(f"    {feature_names[idx]}")

# ── 7. Interactive Demo ───────────────────────────────────────────────────────
test_messages = [
    "Congratulations! You've won a FREE iPhone. Click here to claim NOW!",
    "Hey, are we still meeting for lunch at 1pm?",
    "URGENT: Your bank account has been compromised. Call 0800-FREE now!",
    "Can you pick up some milk on your way home please?",
    "Win £1000 cash prize! Text WIN to 87121. Ts&Cs apply.",
]

print("\n[Demo] Classifying sample messages:")
print(f"{'─'*60}")
best_model = results[best]["model"]

for msg in test_messages:
    clean   = clean_text(msg)
    vec     = tfidf.transform([clean])
    pred    = best_model.predict(vec)[0]
    label   = "🚨 SPAM" if pred == 1 else "✅ HAM "
    print(f"  {label} | {msg[:55]}{'...' if len(msg)>55 else ''}")
