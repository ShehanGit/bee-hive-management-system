from pathlib import Path
import json, joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from xgboost import XGBClassifier

from .data_preprocessing_threat import load_and_prepare, PACKAGE_ROOT

# Paths
MODELS_DIR = PACKAGE_ROOT / "models"
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
MODELS_DIR.mkdir(exist_ok=True, parents=True)
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

MODEL_FILE = MODELS_DIR / "threat_model.pkl"
META_FILE  = MODELS_DIR / "threat_model_meta.json"

def main():
    # 1. Load features/labels
    df, X, y, features = load_and_prepare()

    # 2. Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    classes = list(le.classes_)
    print("Classes:", classes)

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    # 4. XGBoost model
    clf = XGBClassifier(
        n_estimators=600,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        eval_metric="mlogloss",
        tree_method="hist"
    )

    # 5. Training
    clf.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    # 6. Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1m = f1_score(y_test, y_pred, average="macro")
    print(f"Test Accuracy: {acc:.3f} | Macro-F1: {f1m:.3f}")
    print(classification_report(y_test, y_pred, target_names=classes))

    # 7. Save model + meta
    bundle = {"model": clf, "label_encoder": le, "features": features}
    joblib.dump(bundle, MODEL_FILE)
    print(f"✅ Saved model to {MODEL_FILE}")

    meta = {
        "classes": classes,
        "features": features,
        "test_accuracy": float(acc),
        "test_macro_f1": float(f1m),
        "n_rows": int(df.shape[0])
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"✅ Saved meta to {META_FILE}")

    # 8. Correlation Heatmap
    corr = df[features].corr(numeric_only=True)
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    corr_file = OUTPUTS_DIR / "correlation_heatmap.png"
    plt.savefig(corr_file)
    print(f"📊 Saved correlation heatmap to {corr_file}")

    # 9. Feature Importances
    importances = clf.feature_importances_
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances, y=features, palette="viridis")
    plt.title("Feature Importances (XGBoost)")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    fi_file = OUTPUTS_DIR / "feature_importances.png"
    plt.savefig(fi_file)
    print(f"📊 Saved feature importance chart to {fi_file}")

if __name__ == "__main__":
    main()
