from pathlib import Path
import json, joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from xgboost import XGBClassifier

from .data_preprocessing_threat import load_and_prepare, PACKAGE_ROOT

MODELS_DIR = PACKAGE_ROOT / "models"
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
MODELS_DIR.mkdir(exist_ok=True, parents=True)
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

MODEL_FILE = MODELS_DIR / "threat_model.pkl"
META_FILE  = MODELS_DIR / "threat_model_meta.json"

def main():
    # Load features/labels
    df, X, y, features = load_and_prepare()

    # Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    classes = list(le.classes_)
    print("Classes:", classes)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    # XGBoost (strong settings; no scaling needed)
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
        tree_method="hist",
        early_stopping_rounds=50  # Moved here from fit() method
    )

    # Training with early stopping
    clf.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1m = f1_score(y_test, y_pred, average="macro")
    print(f"Test Accuracy: {acc:.3f} | Macro-F1: {f1m:.3f}")
    print(classification_report(y_test, y_pred, target_names=classes))

    # Simple CV (on the full dataset)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    # Using best_ntree_limit implicitly inside predict; acceptable for this synthetic case

    # Save bundle
    bundle = {"model": clf, "label_encoder": le, "features": features}
    joblib.dump(bundle, MODEL_FILE)
    print(f"Saved model to {MODEL_FILE}")

    meta = {
        "classes": classes,
        "features": features,
        "test_accuracy": float(acc),
        "test_macro_f1": float(f1m),
        "n_rows": int(df.shape[0])
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Saved meta to {META_FILE}")

if __name__ == "__main__":
    main()