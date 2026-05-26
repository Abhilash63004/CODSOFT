# ============================================================
# TASK 3: IRIS FLOWER CLASSIFICATION
# CodSoft Data Science Internship
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# ── 1. Load Data ─────────────────────────────────────────────
# Option A: Load from sklearn (built-in, always available)
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

# Option B (commented): Load from CSV if you downloaded from Kaggle
# df = pd.read_csv('iris.csv')

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print(df.head())

# ── 2. EDA ───────────────────────────────────────────────────
print("\n── Species Distribution ──")
print(df['species'].value_counts())

print("\n── Statistical Summary ──")
print(df.describe().round(2))

# ── 3. Preprocessing ─────────────────────────────────────────
X = df.drop('species', axis=1)
y = df['species']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ── 4. Train Models ───────────────────────────────────────────
# K-Nearest Neighbors
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn_preds = knn.predict(X_test)

# Decision Tree
dt = DecisionTreeClassifier(max_depth=4, random_state=42)
dt.fit(X_train, y_train)
dt_preds = dt.predict(X_test)

# ── 5. Evaluation ─────────────────────────────────────────────
print("\n══ RESULTS ══")
print(f"KNN Accuracy          : {accuracy_score(y_test, knn_preds):.4f}")
print(f"Decision Tree Accuracy: {accuracy_score(y_test, dt_preds):.4f}")

print("\n── KNN Classification Report ──")
print(classification_report(y_test, knn_preds))

# ── 6. Visualizations ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('Iris Flower Classification', fontsize=15, fontweight='bold')

# Pairplot-style: Sepal Length vs Width
colors = {'setosa': '#e74c3c', 'versicolor': '#3498db', 'virginica': '#2ecc71'}
for species, color in colors.items():
    subset = df[df['species'] == species]
    axes[0, 0].scatter(subset['sepal length (cm)'], subset['sepal width (cm)'],
                       label=species, color=color, alpha=0.7)
axes[0, 0].set_xlabel('Sepal Length (cm)')
axes[0, 0].set_ylabel('Sepal Width (cm)')
axes[0, 0].set_title('Sepal: Length vs Width')
axes[0, 0].legend()

# Petal Length vs Width
for species, color in colors.items():
    subset = df[df['species'] == species]
    axes[0, 1].scatter(subset['petal length (cm)'], subset['petal width (cm)'],
                       label=species, color=color, alpha=0.7)
axes[0, 1].set_xlabel('Petal Length (cm)')
axes[0, 1].set_ylabel('Petal Width (cm)')
axes[0, 1].set_title('Petal: Length vs Width')
axes[0, 1].legend()

# Confusion Matrix - KNN
cm = confusion_matrix(y_test, knn_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0],
            xticklabels=iris.target_names, yticklabels=iris.target_names)
axes[1, 0].set_title('Confusion Matrix (KNN)')
axes[1, 0].set_ylabel('Actual')
axes[1, 0].set_xlabel('Predicted')

# Accuracy Comparison
models = ['KNN\n(k=5)', 'Decision\nTree']
accs = [accuracy_score(y_test, knn_preds), accuracy_score(y_test, dt_preds)]
bars = axes[1, 1].bar(models, accs, color=['#3498db', '#2ecc71'], width=0.4)
axes[1, 1].set_ylim(0, 1.15)
axes[1, 1].set_title('Model Accuracy Comparison')
axes[1, 1].set_ylabel('Accuracy')
for bar, acc in zip(bars, accs):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{acc:.2%}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/task3_iris_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nPlot saved: task3_iris_results.png")

# ── 7. Predict a new flower ───────────────────────────────────
sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # likely setosa
sample_scaled = scaler.transform(sample)
prediction = knn.predict(sample_scaled)
print(f"\nSample prediction → sepal(5.1, 3.5) petal(1.4, 0.2) : {prediction[0]}")
