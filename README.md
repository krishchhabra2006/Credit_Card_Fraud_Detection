# Credit Card Fraud Detection

A machine learning project for detecting potentially fraudulent credit card transactions using LightGBM.

## Project Overview

This project uses a supervised machine learning approach to classify credit card transactions as either:

- NORMAL
- FRAUD

The model was trained on a transaction dataset containing behavioral and transaction-related features.

The final model is wrapped inside a `FraudDetector` class that handles:

- Input validation
- Feature ordering
- Fraud probability prediction
- Classification using a probability threshold

The trained detector is serialized using Joblib and used by a Streamlit web application.

## Features

The model uses the following seven input features:

1. `distance_from_home`
2. `distance_from_last_transaction`
3. `ratio_to_median_purchase_price`
4. `repeat_retailer`
5. `used_chip`
6. `used_pin_number`
7. `online_order`

The target variable used during training was:

- `fraud`

The target is not required during prediction.

## Model

The final machine learning model is a LightGBM binary classifier.

The prediction threshold used by the application is:

```text
0.79