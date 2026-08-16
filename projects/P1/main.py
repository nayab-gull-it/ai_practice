import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from pathlib import Path

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Shoe Size Predictor",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #6A11CB 0%, #2575FC 100%);
            padding: 2rem;
            border-radius: 14px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .main-header h1 {
            color: #FFFFFF;
            font-size: 2.2rem;
            margin-bottom: 0.3rem;
        }
        .main-header p {
            color: #E8EAF6;
            font-size: 1rem;
            margin: 0;
        }
        .prediction-box {
            background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin: 1.5rem 0;
        }
        .prediction-box h2 {
            color: white;
            font-size: 0.95rem;
            font-weight: 400;
            margin-bottom: 0.4rem;
            opacity: 0.9;
        }
        .prediction-box h1 {
            color: white;
            font-size: 3rem;
            margin: 0;
        }
        section[data-testid="stSidebar"] {
            background-color: #1C2833;
        }
        section[data-testid="stSidebar"] * {
            color: #ECF0F1 !important;
        }
        div.stButton > button {
            background-color: #2575FC;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            border: none;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #1a5fd0;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LOAD MODEL ARTIFACT
# ----------------------------------------------------------------------------
MODEL_PATH = Path(__file__).parent / "models" / "shoe_size_model_artifact.pkl"

@st.cache_resource
def load_artifact(path: Path):
    with open(path, "rb") as f:
        artifact = pickle.load(f)
    return artifact

if not MODEL_PATH.exists():
    st.error(
        f"Model file not found at `{MODEL_PATH}`.\n\n"
        "Make sure `shoe_size_model_artifact.pkl` is placed inside a `models/` "
        "folder next to `main.py`."
    )
    st.stop()

artifact = load_artifact(MODEL_PATH)
model = artifact["model"]
model_name = artifact.get("model_name", "Regression Model")
feature_names = artifact.get("feature_names", ["height_cm", "weight_kg", "gender"])
gender_mapping = artifact.get("gender_mapping", {0: "Female", 1: "Male"})
test_r2 = artifact.get("test_r2_score", None)
test_mae = artifact.get("test_mae", None)
test_rmse = artifact.get("test_rmse", None)

# Reverse mapping: label -> code, for the dropdown
label_to_code = {v: k for k, v in gender_mapping.items()}

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>👟 Shoe Size Prediction</h1>
        <p>Predict US shoe size from height, weight, and gender using Linear Regression</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIDEBAR — MODEL INFO
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ℹ️ Model Information")
    st.markdown(f"**Model:** {model_name}")
    if test_r2 is not None:
        st.markdown(f"**R² Score:** {test_r2:.3f}  (~{test_r2*100:.1f}%)")
    if test_mae is not None:
        st.markdown(f"**MAE:** {test_mae:.2f} sizes")
    if test_rmse is not None:
        st.markdown(f"**RMSE:** {test_rmse:.2f} sizes")
    st.markdown("---")
    st.markdown("## 📊 About")
    st.markdown(
        "This dashboard predicts a person's **US shoe size** based on their "
        "**height**, **weight**, and **gender**, using a trained Linear "
        "Regression model."
    )
    st.markdown("---")
    st.markdown("## 🛠️ How it works")
    st.markdown(
        "1. Enter height, weight, and select gender\n"
        "2. Click **Predict Shoe Size**\n"
        "3. View the estimated US shoe size"
    )

# ----------------------------------------------------------------------------
# MAIN LAYOUT — INPUT FORM + PREDICTION
# ----------------------------------------------------------------------------
input_col, result_col = st.columns([1.1, 1], gap="large")

with input_col:
    st.markdown("### 📝 Enter Your Details")

    with st.form("prediction_form"):
        height_cm = st.slider(
            "Height (cm)", min_value=120.0, max_value=210.0,
            value=170.0, step=0.5
        )
        weight_kg = st.slider(
            "Weight (kg)", min_value=30.0, max_value=140.0,
            value=65.0, step=0.5
        )
        gender_label = st.selectbox(
            "Gender", options=list(label_to_code.keys())
        )

        submitted = st.form_submit_button("👟 Predict Shoe Size")

with result_col:
    st.markdown("### 📈 Prediction Result")

    if submitted:
        gender_code = label_to_code[gender_label]

        input_df = pd.DataFrame([{
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "gender": gender_code
        }])[feature_names]

        predicted_size = model.predict(input_df)[0]

        st.markdown(f"""
            <div class="prediction-box">
                <h2>ESTIMATED US SHOE SIZE</h2>
                <h1>{predicted_size:.1f}</h1>
            </div>
        """, unsafe_allow_html=True)

        margin = test_rmse if test_rmse else 0.5
        low, high = predicted_size - margin, predicted_size + margin

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_size,
            number={'valueformat': ".1f"},
            gauge={
                'axis': {'range': [max(0, low - 2), high + 2]},
                'bar': {'color': "#2575FC"},
                'steps': [
                    {'range': [max(0, low - 2), low], 'color': "#F4F6F6"},
                    {'range': [low, high], 'color': "#D6EAF8"},
                    {'range': [high, high + 2], 'color': "#F4F6F6"},
                ],
            },
            title={'text': "Predicted Shoe Size with Confidence Range"}
        ))
        fig.update_layout(height=280, margin=dict(t=50, b=10, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            f"Estimated range: **{low:.1f} – {high:.1f} (US size)** "
            f"based on the model's typical prediction error."
        )
    else:
        st.info("👈 Enter your details and click **Predict Shoe Size** to see the result.")

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit • Shoe Size Prediction Pipeline • Linear Regression")