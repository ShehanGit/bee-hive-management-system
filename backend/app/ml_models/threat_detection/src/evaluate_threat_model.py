import joblib, json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

from .data_preprocessing_threat import load_and_prepare, PACKAGE_ROOT

MODELS_DIR = PACKAGE_ROOT / "models"
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

MODEL_FILE = MODELS_DIR / "threat_model.pkl"

def main():
    bundle = joblib.load(MODEL_FILE)
    model = bundle["model"]
    le = bundle["label_encoder"]
    features = bundle["features"]

    df, X, y, _ = load_and_prepare()
    y_true = le.transform(y)
    y_pred = model.predict(X)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    fig, ax = plt.subplots(figsize=(6,5))
    disp.plot(ax=ax, cmap="Blues", values_format="d")
    plt.title("Confusion Matrix — Threat Detection")
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / "confusion_matrix.png")
    plt.close(fig)

    report = classification_report(y_true, y_pred, target_names=le.classes_, output_dict=True)
    with open(OUTPUTS_DIR / "classification_report.json", "w") as f:
        json.dump(report, f, indent=2)

    if hasattr(model, "feature_importances_"):
        importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=True)
        ax = importances.plot(kind="barh", figsize=(7,4), title="Feature Importances")
        ax.figure.tight_layout()
        ax.figure.savefig(OUTPUTS_DIR / "feature_importances.png")
        plt.close(ax.figure)

    print("Saved evaluation outputs to", OUTPUTS_DIR)

if __name__ == "__main__":
    main()
