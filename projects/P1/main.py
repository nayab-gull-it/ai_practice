import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Employee Salary Predictor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%);
            padding: 2rem;
            border-radius: 14px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .main-header h1 {
            color: #ECF0F1;
            font-size: 2.2rem;
            margin-bottom: 0.3rem;
        }
        .main-header p {
            color: #D5DBDB;
            font-size: 1rem;
            margin: 0;
        }
        .metric-card {
            background-color: #F8F9F9;
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            border: 1px solid #E5E7E9;
        }
        .prediction-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
            font-size: 2.8rem;
            margin: 0;
        }
        section[data-testid="stSidebar"] {
            background-color: #1C2833;
        }
        section[data-testid="stSidebar"] * {
            color: #ECF0F1 !important;
        }
        div.stButton > button {
            background-color: #16A085;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            border: none;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #138D75;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LOAD MODEL ARTIFACT
# ----------------------------------------------------------------------------
MODEL_PATH = Path(__file__).parent / "models" / "salary_model_artifact.pkl"

@st.cache_resource
def load_artifact(path: Path):
    with open(path, "rb") as f:
        artifact = pickle.load(f)
    return artifact

if not MODEL_PATH.exists():
    st.error(
        f"Model file not found at `{MODEL_PATH}`.\n\n"
        "Make sure `salary_model_artifact.pkl` is placed inside a `models/` "
        "folder next to `main.py`."
    )
    st.stop()

artifact = load_artifact(MODEL_PATH)
model = artifact["model"]
model_name = artifact.get("model_name", "Regression Model")
numerical_features = artifact.get("numerical_features", ["years_experience"])
categorical_features = artifact.get(
    "categorical_features",
    ["education_level", "job_role", "location", "company_size"]
)
test_r2 = artifact.get("test_r2_score", None)
all_metrics = artifact.get("all_model_metrics", None)

# ----------------------------------------------------------------------------
# EXTRACT DROPDOWN OPTIONS DIRECTLY FROM THE TRAINED ENCODER
# (no need to hardcode categories — pulled straight from the pipeline)
# ----------------------------------------------------------------------------
@st.cache_resource
def get_category_options(_model, categorical_cols):
    try:
        preprocessor = _model.named_steps["preprocessor"]
        ohe = preprocessor.named_transformers_["cat"]
        options = {}
        for col, cats in zip(categorical_cols, ohe.categories_):
            options[col] = sorted(list(cats))
        return options
    except Exception:
        return {col: [] for col in categorical_cols}

category_options = get_category_options(model, categorical_features)

def pretty(label: str) -> str:
    return label.replace("_", " ").title()

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>💼 Employee Salary Prediction</h1>
        <p>A Machine Learning Dashboard powered by Gradient Boosting Regression</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIDEBAR — MODEL INFO
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ℹ️ Model Information")
    st.markdown(f"**Model:** {model_name}")
    if test_r2 is not None:
        st.markdown(f"**Test R² Score:** {test_r2:.3f}  (~{test_r2*100:.1f}%)")
    st.markdown("---")
    st.markdown("## 📊 About")
    st.markdown(
        "This dashboard predicts an employee's salary based on their "
        "**experience**, **education level**, **job role**, **location**, "
        "and **company size**, using a trained regression pipeline."
    )
    st.markdown("---")
    st.markdown("## 🛠️ How it works")
    st.markdown(
        "1. Fill in the employee details on the right\n"
        "2. Click **Predict Salary**\n"
        "3. View the estimated salary and model confidence"
    )

# ----------------------------------------------------------------------------
# MAIN LAYOUT — INPUT FORM + PREDICTION
# ----------------------------------------------------------------------------
input_col, result_col = st.columns([1.1, 1], gap="large")

with input_col:
    st.markdown("### 📝 Enter Employee Details")

    with st.form("prediction_form"):
        years_experience = st.slider(
            "Years of Experience", min_value=0.0, max_value=40.0,
            value=5.0, step=0.5
        )

        c1, c2 = st.columns(2)
        with c1:
            education_level = st.selectbox(
                pretty("education_level"),
                options=category_options.get("education_level", [])
            )
            job_role = st.selectbox(
                pretty("job_role"),
                options=category_options.get("job_role", [])
            )
        with c2:
            location = st.selectbox(
                pretty("location"),
                options=category_options.get("location", [])
            )
            company_size = st.selectbox(
                pretty("company_size"),
                options=category_options.get("company_size", [])
            )

        submitted = st.form_submit_button("🔮 Predict Salary")

with result_col:
    st.markdown("### 📈 Prediction Result")

    if submitted:
        input_df = pd.DataFrame([{
            "years_experience": years_experience,
            "education_level": education_level,
            "job_role": job_role,
            "location": location,
            "company_size": company_size
        }])

        predicted_salary = model.predict(input_df)[0]

        st.markdown(f"""
            <div class="prediction-box">
                <h2>ESTIMATED ANNUAL SALARY</h2>
                <h1>${predicted_salary:,.0f}</h1>
            </div>
        """, unsafe_allow_html=True)

        # Confidence range using RMSE if available, else +/-10%
        rmse = None
        if all_metrics:
            for m in all_metrics:
                if m.get("Model") == model_name:
                    rmse = m.get("RMSE")
                    break
        margin = rmse if rmse else predicted_salary * 0.1

        low, high = predicted_salary - margin, predicted_salary + margin

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_salary,
            number={'prefix': "$", 'valueformat': ",.0f"},
            gauge={
                'axis': {'range': [max(0, low - margin), high + margin]},
                'bar': {'color': "#16A085"},
                'steps': [
                    {'range': [max(0, low - margin), low], 'color': "#F4F6F6"},
                    {'range': [low, high], 'color': "#D5F5E3"},
                    {'range': [high, high + margin], 'color': "#F4F6F6"},
                ],
            },
            title={'text': "Predicted Salary with Confidence Range"}
        ))
        fig.update_layout(height=280, margin=dict(t=50, b=10, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            f"Estimated range: **${low:,.0f} – ${high:,.0f}** "
            f"(based on model's typical prediction error)"
        )
    else:
        st.info("👈 Fill in the employee details and click **Predict Salary** to see the result.")

# ----------------------------------------------------------------------------
# MODEL PERFORMANCE SECTION
# ----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 🏆 Model Performance Overview")

if all_metrics:
    metrics_df = pd.DataFrame(all_metrics)
    metrics_df = metrics_df.sort_values(by="R2 Score", ascending=False).reset_index(drop=True)

    m1, m2, m3, m4 = st.columns(4)
    best_row = metrics_df.iloc[0]
    with m1:
        st.metric("Best Model", best_row["Model"])
    with m2:
        st.metric("R² Score", f"{best_row['R2 Score']:.3f}")
    with m3:
        st.metric("RMSE", f"${best_row['RMSE']:,.0f}")
    with m4:
        st.metric("MAE", f"${best_row['MAE']:,.0f}")

    st.markdown("#### Comparison Across Trained Models")
    tab1, tab2 = st.tabs(["📊 R² Score", "📉 RMSE"])

    with tab1:
        fig_r2 = px.bar(
            metrics_df, x="Model", y="R2 Score", color="R2 Score",
            color_continuous_scale="Greens", text_auto=".3f"
        )
        fig_r2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_r2, use_container_width=True)

    with tab2:
        fig_rmse = px.bar(
            metrics_df, x="Model", y="RMSE", color="RMSE",
            color_continuous_scale="Blues_r", text_auto=".0f"
        )
        fig_rmse.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_rmse, use_container_width=True)

    with st.expander("View raw metrics table"):
        st.dataframe(metrics_df, use_container_width=True)
else:
    st.info("No comparison metrics were saved with this model artifact.")

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit • Employee Salary Prediction Pipeline • Gradient Boosting Regression")