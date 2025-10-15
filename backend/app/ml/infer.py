import joblib
from pathlib import Path


MODEL_DIR = Path(__file__).resolve().parent / "models"


def load_model(pos: str, target_col: str):
    path = MODEL_DIR / f"lgb_{pos}_{target_col}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model not found for {pos}/{target_col}. Train models first.")
    return joblib.load(path)