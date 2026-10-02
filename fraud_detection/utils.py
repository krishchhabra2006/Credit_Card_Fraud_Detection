import __main__
import joblib
import pandas as pd
import math
import numbers
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

FEATURES = [
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price",
    "repeat_retailer",
    "used_chip",
    "used_pin_number",
    "online_order"
]

THRESHOLD = 0.79


# ============================================================
# Fraud Detector
# ============================================================

class FraudDetector:

    def __init__(self, model, features, threshold=0.79):

        self.model = model
        self.features = list(features)
        self.threshold = float(threshold)

    def validate_input(self, data):

        # 1. Input must be a dictionary
        if not isinstance(data, dict):
            raise TypeError(
                "Input must be a dictionary."
            )

        # 2. Check missing features
        missing = set(self.features) - set(data.keys())

        if missing:
            raise ValueError(
                f"Missing features: {sorted(missing)}"
            )

        # 3. Check unexpected features
        extra = set(data.keys()) - set(self.features)

        if extra:
            raise ValueError(
                f"Unexpected features: {sorted(extra)}"
            )

        # 4. Binary features
        binary_features = [
            "repeat_retailer",
            "used_chip",
            "used_pin_number",
            "online_order"
        ]

        # 5. Validate numeric values
        for feature in self.features:

            value = data[feature]

            # Reject booleans
            if isinstance(value, bool):
                raise TypeError(
                    f"{feature} must be numeric."
                )

            # Must be a real number
            if not isinstance(value, numbers.Real):
                raise TypeError(
                    f"{feature} must be numeric."
                )

            # Reject NaN and infinity
            if not math.isfinite(float(value)):
                raise ValueError(
                    f"{feature} must be finite."
                )

        # 6. Continuous domain validation

        if data["distance_from_home"] < 0:
            raise ValueError(
                "distance_from_home cannot be negative."
            )

        if data["distance_from_last_transaction"] < 0:
            raise ValueError(
                "distance_from_last_transaction cannot be negative."
            )

        if data["ratio_to_median_purchase_price"] <= 0:
            raise ValueError(
                "ratio_to_median_purchase_price must be greater than 0."
            )

        # 7. Binary validation

        for feature in binary_features:

            if data[feature] not in (0, 1):
                raise ValueError(
                    f"{feature} must be 0 or 1."
                )

    def predict(self, data):

        # Validate input
        self.validate_input(data)

        # Create DataFrame in exact training feature order
        input_df = pd.DataFrame(
            [[data[feature] for feature in self.features]],
            columns=self.features
        )

        # Get fraud probability
        probability = float(
            self.model.predict_proba(input_df)[0, 1]
        )

        # Apply threshold
        prediction = int(
            probability >= self.threshold
        )

        # Convert prediction to label
        label = (
            "FRAUD"
            if prediction == 1
            else "NORMAL"
        )

        return {
            "fraud_probability": probability,
            "threshold": self.threshold,
            "prediction": prediction,
            "label": label
        }


# ============================================================
# Load existing trained detector
# ============================================================

# The existing pickle was created when FraudDetector
# existed in __main__. We make that old reference resolve
# to this class before loading the pickle.

setattr(__main__, "FraudDetector", FraudDetector)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "fraud_detection.pkl"

detector = joblib.load(MODEL_PATH)


# ============================================================
# Public prediction function
# ============================================================

def predict_fraud(data):

    return detector.predict(data)