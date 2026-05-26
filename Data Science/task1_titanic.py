# ============================================================
# TASK 1: TITANIC SURVIVAL PREDICTION
# CodSoft Data Science Internship
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# ── 1. Load Data ─────────────────────────────────────────────
# Download from: https://www.kaggle.com/datasets/brendan45774/test-file
# Or use the built-in sample below for demonstration

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
try:
    df = pd.read_csv(url)
    print("Dataset loaded from URL.")
except Exception:
    # Minimal sample data for offline use
    data = {
        'Survived': [0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,1,0,1],
        'Pclass':   [3,1,3,1,3,3,1,3,3,2,3,1,3,3,3,2,3,2,3,3],
        'Sex':      ['male','female','female','female','male','male','male','male','female','female','female','female','male','male','male','female','male','male','female','female'],
        'Age':      [22,38,26,35,35,np.nan,54,2,27,14,4,58,20,39,14,55,2,np.nan,31,np.nan],
        'SibSp':    [1,1,0,1,0,0,0,3,0,1,1,0,0,1,0,0,4,0,1,0],
        'Parch':    [0,0,0,0,0,0,0,1,2,0,1,0,0,5,0,0,1,0,0,0],
        'Fare':     [7.25,71.28,7.92,53.1,8.05,8.46,51.86,21.08,11.13,30.07,16.7,26.55,8.05,31.27,7.85,16,29.12,13,18,7.22],
    }
    df = pd.DataFrame(data)
    print("Using sample data.")

print(f"\nDataset shape: {df.shape}")
print(df.head())

# ── 2. Exploratory Data Analysis ─────────────────────────────
print("\n── Missing Values ──")
print(df.isnull().sum())

print("\n── Survival Rate ──")
print(df['Survived'].value_counts())

# ── 3. Feature Engineering & Preprocessing ───────────────────
df_model = df.copy()

# Fill missing Age with median
df_model['Age'].fillna(df_model['Age'].median(), inplace=True)

# Fill missing Embarked with mode (if column exists)
if 'Embarked' in df_model.columns:
    df_model['Embarked'].fillna(df_model['Embarked'].mode()[0], inplace=True)

# Drop high-cardinality / less useful columns if present
drop_cols = ['Name', 'Ticket', 'Cabin', 'PassengerId']
df_model.drop(columns=[c for c in drop_cols if c in df_model.columns], inplace=True)

# Encode categorical columns
le = LabelEncoder()
for col in ['Sex', 'Embarked']:
    if col in df_model.columns:
        df_model[col] = le.fit_transform(df_model[col].astype(str))

# Fill any remaining NaNs with column median
df_model.fillna(df_model.median(numeric_only=True), inplace=True)

print("\n── Processed Features ──")
print(df_model.head())

# ── 4. Train / Test Split ─────────────────────────────────────
X = df_model.drop('Survived', axis=1)
y = df_model['Survived']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── 5. Model Training ─────────────────────────────────────────
# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# ── 6. Evaluation ─────────────────────────────────────────────
print("\n══ RESULTS ══")
print(f"Logistic Regression Accuracy : {accuracy_score(y_test, lr_preds):.4f}")
print(f"Random Forest Accuracy       : {accuracy_score(y_test, rf_preds):.4f}")

print("\n── Random Forest Classification Report ──")
print(classification_report(y_test, rf_preds, target_names=['Did Not Survive', 'Survived']))

# ── 7. Visualizations ─────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Titanic Survival Prediction', fontsize=15, fontweight='bold')

# Confusion Matrix
cm = confusion_matrix(y_test, rf_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', ax=axes[0],
            xticklabels=['Did Not Survive', 'Survived'],
            yticklabels=['Did Not Survive', 'Survived'])
axes[0].set_title('Confusion Matrix (Random Forest)')
axes[0].set_ylabel('Actual')
axes[0].set_xlabel('Predicted')

# Feature Importance
feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=True)
feat_imp.plot(kind='barh', ax=axes[1], color='#5c2d91')
axes[1].set_title('Feature Importance')
axes[1].set_xlabel('Importance Score')

# Model Accuracy Comparison
models = ['Logistic\nRegression', 'Random\nForest']
accs = [accuracy_score(y_test, lr_preds), accuracy_score(y_test, rf_preds)]
bars = axes[2].bar(models, accs, color=['#7b52ab', '#5c2d91'], width=0.4)
axes[2].set_ylim(0, 1.1)
axes[2].set_title('Model Accuracy Comparison')
axes[2].set_ylabel('Accuracy')
for bar, acc in zip(bars, accs):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'{acc:.2%}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/task1_titanic_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nPlot saved: task1_titanic_results.png")
