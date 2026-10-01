import joblib
import pandas as pd
import math
import numbers

def validate_input(self, data):

    # 1. Input must be dictionary
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary.")

    # 2. Check missing features
    missing = set(self.features) - set(data.keys())

    if missing:
        raise ValueError(
            f"Missing features: {sorted(missing)}"
        )

    # 3. Check extra features
    extra = set(data.keys()) - set(self.features)

    if extra:
        raise ValueError(
            f"Unexpected features: {sorted(extra)}"
        )

    # 4. Continuous features
    continuous_features = [
        "distance_from_home",
        "distance_from_last_transaction",
        "ratio_to_median_purchase_price"
    ]

    # 5. Binary features
    binary_features = [
        "repeat_retailer",
        "used_chip",
        "used_pin_number",
        "online_order"
    ]

    # 6. Validate all values
    for feature in self.features:

        value = data[feature]

        # Must be numeric
        if not isinstance(value, numbers.Real):
            raise TypeError(
                f"{feature} must be numeric."
            )

        # Reject NaN / infinity
        if not math.isfinite(value):
            raise ValueError(
                f"{feature} must be finite."
            )

    # 7. Continuous domain validation

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

    # 8. Binary validation

    for feature in binary_features:

        if data[feature] not in (0, 1):
            raise ValueError(
                f"{feature} must be 0 or 1."
            )

    return True

class FraudDetector:

    def __init__(self, model, features, threshold=0.79):

        self.model = model
        self.features = features
        self.threshold = threshold


    def validate_input(self, data):

        # Must be dictionary
        if not isinstance(data, dict):
            raise TypeError(
                "Input must be a dictionary."
            )

        # Missing features
        missing = set(self.features) - set(data.keys())

        if missing:
            raise ValueError(
                f"Missing features: {sorted(missing)}"
            )

        # Extra features
        extra = set(data.keys()) - set(self.features)

        if extra:
            raise ValueError(
                f"Unexpected features: {sorted(extra)}"
            )

        # Numeric validation
        for feature in self.features:

            if not isinstance(data[feature], (int, float)):
                raise TypeError(
                    f"{feature} must be numeric."
                )

        # Binary validation
        binary_features = [
            "repeat_retailer",
            "used_chip",
            "used_pin_number",
            "online_order"
        ]

        for feature in binary_features:

            if data[feature] not in [0, 1]:
                raise ValueError(
                    f"{feature} must be either 0 or 1."
                )

        return True


    def predict(self, data):

        # Validate
        self.validate_input(data)

        # Create DataFrame
        input_df = pd.DataFrame(
            [data],
            columns=self.features
        )

        # Fraud probability
        probability = self.model.predict_proba(
            input_df
        )[0, 1]

        # Apply threshold
        prediction = int(
            probability >= self.threshold
        )

        # Label
        label = (
            "FRAUD"
            if prediction == 1
            else "NORMAL"
        )

        return {
            "fraud_probability": float(probability),
            "threshold": self.threshold,
            "prediction": prediction,
            "label": label
        }

# Load the trained fraud detector
detector = joblib.load("fraud_detection/fraud_detection.pkl")

print("Model loaded successfully.")
print("Features:", detector.features)
print("Threshold:", detector.threshold)
print()


# -----------------------------
# TEST 1: Expected FRAUD
# -----------------------------

fraud_transaction = {
    "distance_from_home": 500,
    "distance_from_last_transaction": 100,
    "ratio_to_median_purchase_price": 10,
    "repeat_retailer": 0,
    "used_chip": 0,
    "used_pin_number": 0,
    "online_order": 1
}

fraud_result = detector.predict(fraud_transaction)

print("TEST 1 - Expected FRAUD")
print(fraud_result)
print()


# -----------------------------
# TEST 2: Expected NORMAL
# -----------------------------

normal_transaction = {
    "distance_from_home": 10,
    "distance_from_last_transaction": 2,
    "ratio_to_median_purchase_price": 1,
    "repeat_retailer": 1,
    "used_chip": 1,
    "used_pin_number": 1,
    "online_order": 0
}

normal_result = detector.predict(normal_transaction)

print("TEST 2 - Expected NORMAL")
print(normal_result)
print()


# -----------------------------
# Final check
# -----------------------------

assert fraud_result["label"] == "FRAUD", \
    "FRAUD test failed."

assert normal_result["label"] == "NORMAL", \
    "NORMAL test failed."

print("ALL TESTS PASSED.")