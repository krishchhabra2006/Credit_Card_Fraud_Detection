import streamlit as st
from utils import predict_fraud


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="centered"
)


# ============================================================
# Title
# ============================================================

st.title("Credit Card Fraud Detection")

st.write(
    "Enter the transaction details below to check whether "
    "the transaction is likely to be fraudulent."
)


# ============================================================
# Input fields
# ============================================================

st.subheader("Transaction Details")

distance_from_home = st.number_input(
    "Distance from home",
    min_value=0.0,
    value=10.0,
    step=0.1
)

distance_from_last_transaction = st.number_input(
    "Distance from last transaction",
    min_value=0.0,
    value=2.0,
    step=0.1
)

ratio_to_median_purchase_price = st.number_input(
    "Ratio to median purchase price",
    min_value=0.000001,
    value=1.0,
    step=0.1
)

repeat_retailer = st.selectbox(
    "Repeat retailer",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

used_chip = st.selectbox(
    "Used chip",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

used_pin_number = st.selectbox(
    "Used PIN number",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

online_order = st.selectbox(
    "Online order",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)


# ============================================================
# Prediction
# ============================================================

if st.button("Check Transaction", type="primary"):

    transaction = {
        "distance_from_home": distance_from_home,
        "distance_from_last_transaction": distance_from_last_transaction,
        "ratio_to_median_purchase_price": ratio_to_median_purchase_price,
        "repeat_retailer": repeat_retailer,
        "used_chip": used_chip,
        "used_pin_number": used_pin_number,
        "online_order": online_order
    }

    try:

        result = predict_fraud(transaction)

        st.subheader("Prediction")

        if result["label"] == "FRAUD":
            st.error("FRAUDULENT TRANSACTION")
        else:
            st.success("NORMAL TRANSACTION")

        st.write(
            f"Fraud Probability: "
            f"{result['fraud_probability']:.2%}"
        )

    except (TypeError, ValueError) as e:

        st.error(str(e))