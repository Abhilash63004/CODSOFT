# ============================================================
# TASK 4: SALES PREDICTION USING PYTHON
# CodSoft Data Science Internship
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# ── 1. Load / Create Data ─────────────────────────────────────
# Dataset: Advertising (TV, Radio, Newspaper → Sales)
# Download from: https://www.kaggle.com/datasets/bumba5341/advertisingcsv
# OR use the sample below (representative of the real dataset)

url = "https://raw.githubusercontent.com/selva86/datasets/master/Advertising.csv"
try:
    df = pd.read_csv(url, index_col=0)
    print("Dataset loaded from URL.")
except Exception:
    # Reproducible sample if offline
    np.random.seed(42)
    n = 200
    TV      = np.random.uniform(0.7, 296, n)
    Radio   = np.random.uniform(0, 49.6, n)
    News    = np.random.uniform(0.3, 114, n)
    Sales   = 2.9 + 0.046*TV + 0.188*Radio - 0.001*News + np.random.normal(0, 1.5, n)
    df = pd.DataFrame({'TV': TV, 'Radio': Radio, 'Newspaper': News, 'Sales': Sales})
    print("Using generated sample data.")

print(f"\nDataset shape: {df.shape}")
print(df.head())

# ── 2. EDA ───────────────────────────────────────────────────
print("\n── Statistical Summary ──")
print(df.describe().round(2))

print("\n── Correlation with Sales ──")
print(df.corr()['Sales'].sort_values(ascending=False))

# ── 3. Preprocessing ─────────────────────────────────────────
X = df.drop('Sales', axis=1)
y = df['Sales']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 4. Train Models ───────────────────────────────────────────
# Linear Regression
lr = LinearRegression()
lr.fit(X_train_s, y_train)
lr_preds = lr.predict(X_test_s)

# Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# ── 5. Evaluation ─────────────────────────────────────────────
def evaluate(name, y_true, y_pred):
    print(f"\n── {name} ──")
    print(f"  MAE  : {mean_absolute_error(y_true, y_pred):.4f}")
    print(f"  RMSE : {np.sqrt(mean_squared_error(y_true, y_pred)):.4f}")
    print(f"  R²   : {r2_score(y_true, y_pred):.4f}")

print("\n══ RESULTS ══")
evaluate("Linear Regression", y_test, lr_preds)
evaluate("Random Forest Regressor", y_test, rf_preds)

print("\n── Linear Regression Coefficients ──")
coef_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': lr.coef_})
print(coef_df.to_string(index=False))

# ── 6. Visualizations ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('Sales Prediction using Python', fontsize=15, fontweight='bold')

# Actual vs Predicted - Linear Regression
axes[0, 0].scatter(y_test, lr_preds, alpha=0.6, color='#3498db')
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', lw=2, label='Perfect prediction')
axes[0, 0].set_title('Linear Regression: Actual vs Predicted')
axes[0, 0].set_xlabel('Actual Sales')
axes[0, 0].set_ylabel('Predicted Sales')
axes[0, 0].legend()

# Actual vs Predicted - Random Forest
axes[0, 1].scatter(y_test, rf_preds, alpha=0.6, color='#2ecc71')
axes[0, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', lw=2, label='Perfect prediction')
axes[0, 1].set_title('Random Forest: Actual vs Predicted')
axes[0, 1].set_xlabel('Actual Sales')
axes[0, 1].set_ylabel('Predicted Sales')
axes[0, 1].legend()

# Correlation Heatmap
corr = df.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1, 0], square=True)
axes[1, 0].set_title('Feature Correlation Heatmap')

# R² Score Comparison
models = ['Linear\nRegression', 'Random\nForest']
r2s = [r2_score(y_test, lr_preds), r2_score(y_test, rf_preds)]
bars = axes[1, 1].bar(models, r2s, color=['#3498db', '#2ecc71'], width=0.4)
axes[1, 1].set_ylim(0, 1.15)
axes[1, 1].set_title('R² Score Comparison')
axes[1, 1].set_ylabel('R² Score')
for bar, r2 in zip(bars, r2s):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{r2:.4f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/task4_sales_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nPlot saved: task4_sales_results.png")

# ── 7. Predict new advertising spend ─────────────────────────
new_data = pd.DataFrame({'TV': [200], 'Radio': [30], 'Newspaper': [10]})
new_scaled = scaler.transform(new_data)
pred = lr.predict(new_scaled)[0]
print(f"\nSample prediction → TV=$200k, Radio=$30k, Newspaper=$10k : Sales ≈ ${pred:.2f}k")
