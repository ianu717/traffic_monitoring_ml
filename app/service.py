import pandas as pd

from pathlib import Path
from catboost import CatBoostClassifier

from traffic_monitoring_ml.config import SELECTED_FEATURES_PATH, CATBOOST_MODEL_PATH
from traffic_monitoring_ml.utils import load_json

from preprocessing import preprocess

class SeverityInferenceService:

    def __init__(self, model_path: str = CATBOOST_MODEL_PATH, threshold: float = 0.5):
        self.threshold = threshold
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.model_features = load_json(Path(SELECTED_FEATURES_PATH))

    def predict_from_context(self, casualty_df: pd.DataFrame, vehicle_df: pd.DataFrame,collision_df: pd.DataFrame) -> dict:
        processed_df = preprocess(casualty=casualty_df, vehicle=vehicle_df, collision=collision_df)
        return self.predict(processed_df)

    def predict(self,model_input: pd.DataFrame) -> dict:
        model_input = model_input[
            self.model_features
        ]
        probabilities = self.model.predict_proba(model_input)[:, 1]
        predictions = (probabilities >= self.threshold).astype(int)
        return {
            'severity_probability': float(probabilities[0]),
            'prediction': int(predictions[0]),
            'threshold': self.threshold
        }

    def set_threshold(self,threshold: float):
        self.threshold = threshold