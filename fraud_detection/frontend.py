import streamlit as st
from utils import predict_fraud


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# Styling (UI only)
# ============================================================

st.markdown(
    """
<style>
/* ---------- Layout ---------- */
.block-container {
    max-width: 1050px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* ---------- Top bar ---------- */
.topbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 4px 14px 4px;
    border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    margin-bottom: 22px;
}
.topbar .logo {
    font-size: 1.6rem;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    padding: 4px 9px;
    line-height: 1.4;
}
.topbar .name {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.2px;
}
.topbar .tag {
    margin-left: auto;
    font-size: 0.78rem;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid rgba(99, 102, 241, 0.45);
    background: rgba(99, 102, 241, 0.12);
    color: #818cf8;
    font-weight: 600;
}

/* ---------- Hero ---------- */
.hero {
    border-radius: 18px;
    padding: 34px 32px;
    margin-bottom: 26px;
    color: #ffffff;
    background:
        radial-gradient(circle at 85% 20%, rgba(255,255,255,0.18), transparent 45%),
        linear-gradient(135deg, #4338ca 0%, #6d28d9 55%, #7c3aed 100%);
    box-shadow: 0 10px 30px rgba(79, 70, 229, 0.30);
}
.hero h1 {
    margin: 0 0 8px 0;
    padding: 0;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
}
.hero p {
    margin: 0 0 20px 0;
    font-size: 1.02rem;
    opacity: 0.92;
    max-width: 620px;
}
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip {
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.28);
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 0.86rem;
    font-weight: 600;
    backdrop-filter: blur(4px);
}

/* ---------- Section headings ---------- */
.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin: 4px 0 2px 0;
}
.section-sub {
    font-size: 0.82rem;
    opacity: 0.65;
    margin-bottom: 10px;
}

/* ---------- Bordered containers ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px;
}

/* ---------- Button (replaces the red "warning" look) ---------- */
div.stButton > button,
div.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
div.stButton > button:hover,
button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
    box-shadow: 0 10px 24px rgba(99, 102, 241, 0.45);
    color: #ffffff;
    border: none;
}
div.stButton > button:active,
button[data-testid="stBaseButton-primary"]:active {
    transform: translateY(0);
    color: #ffffff;
}
div.stButton > button:focus:not(:active),
button[data-testid="stBaseButton-primary"]:focus:not(:active) {
    color: #ffffff;
    border: none;
}

/* ---------- Result card ---------- */
.result {
    border-radius: 18px;
    padding: 26px 28px;
    margin-top: 10px;
    border: 1px solid;
    animation: pop 0.35s ease;
}
@keyframes pop {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result.fraud {
    background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(239,68,68,0.05));
    border-color: rgba(239, 68, 68, 0.55);
}
.result.safe {
    background: linear-gradient(135deg, rgba(34,197,94,0.16), rgba(34,197,94,0.05));
    border-color: rgba(34, 197, 94, 0.55);
}
.result-head { display: flex; align-items: center; gap: 16px; }
.result-icon { font-size: 2.6rem; line-height: 1; }
.result-label {
    font-size: 1.6rem;
    font-weight: 800;
    line-height: 1.15;
}
.fraud .result-label { color: #ef4444; }
.safe .result-label  { color: #22c55e; }
.result-sub { font-size: 0.9rem; opacity: 0.75; margin-top: 2px; }

.meter-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 22px 0 8px 0;
    font-size: 0.9rem;
    font-weight: 600;
}
.meter-row .pct { font-size: 1.7rem; font-weight: 800; }
.meter {
    position: relative;
    height: 14px;
    border-radius: 999px;
    background: rgba(128, 128, 128, 0.25);
    overflow: visible;
}
.meter-fill {
    height: 100%;
    border-radius: 999px;
}
.fraud .meter-fill { background: linear-gradient(90deg, #f97316, #ef4444); }
.safe .meter-fill  { background: linear-gradient(90deg, #22c55e, #4ade80); }
.meter-mark {
    position: absolute;
    top: -5px;
    width: 2px;
    height: 24px;
    background: currentColor;
    opacity: 0.7;
}
.meter-legend {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    opacity: 0.6;
    margin-top: 8px;
}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# Top bar
# ============================================================

st.markdown(
    """
<div class="topbar">
    <div class="logo">💳</div>
    <div class="name">FraudGuard</div>
    <div class="tag">🛡️ Fraud Detection</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# Hero section
# ============================================================

st.markdown(
    """
<div class="hero">
    <h1>💳 Credit Card Fraud Detection</h1>
    <p>Enter the transaction details below to check whether
    the transaction is likely to be fraudulent.</p>
    <div class="chips">
        <span class="chip">⚡ Instant result</span>
        <span class="chip">🧠 Model-based scoring</span>
        <span class="chip">📊 Probability breakdown</span>
        <span class="chip">🔒 7 transaction signals</span>
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# Input fields
# ============================================================

st.markdown(
    '<div class="section-title">📝 Transaction Details</div>'
    '<div class="section-sub">Fill in the values for the transaction you want to check.</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.markdown("**📏 Distance & Price Metrics**")

        distance_from_home = st.number_input(
            "🏠 Distance from home",
            min_value=0.0,
            value=10.0,
            step=0.1
        )

        distance_from_last_transaction = st.number_input(
            "📍 Distance from last transaction",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

        ratio_to_median_purchase_price = st.number_input(
            "💰 Ratio to median purchase price",
            min_value=0.000001,
            value=1.0,
            step=0.1
        )

with right:
    with st.container(border=True):
        st.markdown("**🔐 Transaction Behaviour**")

        yes_no = lambda x: "Yes" if x == 1 else "No"

        c1, c2 = st.columns(2)

        with c1:
            repeat_retailer = st.radio(
                "🏪 Repeat retailer",
                options=[0, 1],
                format_func=yes_no,
                horizontal=True
            )

            used_pin_number = st.radio(
                "🔢 Used PIN number",
                options=[0, 1],
                format_func=yes_no,
                horizontal=True
            )

        with c2:
            used_chip = st.radio(
                "💠 Used chip",
                options=[0, 1],
                format_func=yes_no,
                horizontal=True
            )

            online_order = st.radio(
                "🌐 Online order",
                options=[0, 1],
                format_func=yes_no,
                horizontal=True
            )

        st.caption("Select Yes / No for each transaction attribute.")


# ============================================================
# Prediction
# ============================================================

st.write("")

_, mid, _ = st.columns([1, 1.4, 1])

with mid:
    check = st.button("🔍  Check Transaction", type="primary")

if check:

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

        st.write("")
        st.markdown(
            '<div class="section-title">🎯 Prediction</div>',
            unsafe_allow_html=True
        )

        is_fraud = result["label"] == "FRAUD"
        prob = float(result["fraud_probability"])
        pct_width = max(0.0, min(prob * 100, 100.0))
        threshold = result.get("threshold")

        css_class = "fraud" if is_fraud else "safe"
        icon = "🚨" if is_fraud else "✅"
        title = "FRAUDULENT TRANSACTION" if is_fraud else "NORMAL TRANSACTION"
        sub = (
            "This transaction looks suspicious. Review it before approving."
            if is_fraud
            else "No signs of fraud detected for this transaction."
        )

        marker_html = ""
        legend_html = "<span>0%</span><span>100%</span>"
        if threshold is not None:
            t_pct = max(0.0, min(float(threshold) * 100, 100.0))
            marker_html = f'<div class="meter-mark" style="left:{t_pct}%"></div>'
            legend_html = (
                f"<span>0%</span>"
                f"<span>Decision threshold: {float(threshold):.0%}</span>"
                f"<span>100%</span>"
            )

        st.markdown(
            f"""
<div class="result {css_class}">
<div class="result-head">
<div class="result-icon">{icon}</div>
<div>
<div class="result-label">{title}</div>
<div class="result-sub">{sub}</div>
</div>
</div>
<div class="meter-row">
<span>Fraud Probability</span>
<span class="pct">{prob:.2%}</span>
</div>
<div class="meter">
<div class="meter-fill" style="width:{pct_width}%"></div>
{marker_html}
</div>
<div class="meter-legend">{legend_html}</div>
</div>
""",
            unsafe_allow_html=True
        )

    except (TypeError, ValueError) as e:

        st.error(str(e))
