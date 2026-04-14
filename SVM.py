import pandas as pd

# Load datasets
cleaned = pd.read_json("cleaned.json")
medical = pd.read_csv("saca_dataset.csv")

# Inspect columns
print("CLEANED COLUMNS:", cleaned.columns)
print("MEDICAL COLUMNS:", medical.columns)

# ✅ Merge safely (auto fallback)
common_cols = list(set(cleaned.columns).intersection(set(medical.columns)))

if len(common_cols) > 0:
    print("Merging on:", common_cols[0])
    df = pd.merge(cleaned, medical, on=common_cols[0])
else:
    print("No common column found — using concat")
    df = pd.concat([cleaned, medical], axis=1)

# 🔍 Check result
print(df.head())
print("FINAL COLUMNS:", df.columns)

# ✅ Automatically pick a target column (safer)
possible_targets = ["target", "label", "diagnosis", "outcome", "disease"]

target_column = None
for col in possible_targets:
    if col in df.columns:
        target_column = col
        break

if target_column is None:
    raise Exception("❌ No valid target column found. Check your dataset.")

print("Using target column:", target_column)

# Features + labels
X = df.drop(target_column, axis=1)
y = df[target_column]

# Convert categorical → numeric
X = pd.get_dummies(X)

# Fill missing values
X = X.fillna(0)

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train SVM
from sklearn.svm import SVC
model = SVC(kernel='rbf', C=1, gamma='scale')

model.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))