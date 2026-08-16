# 👟 Shoe Size Prediction

A machine learning web app that predicts a person's **US shoe size** based on their **height**, **weight**, and **gender**, built with `scikit-learn` and deployed as an interactive dashboard using **Streamlit**.

🔗 **Live App:** _add your Streamlit Cloud link here after deployment_
📓 **Kaggle Notebook (model training):** https://www.kaggle.com/code/nayabgulll964/shoe-size-prediction-nayab-gull

---

## 📌 Overview

This project follows a complete ML workflow:
1. Data loading & exploration
2. Model training (Linear Regression)
3. Model evaluation (R², MAE, RMSE)
4. Deployment as an interactive Streamlit dashboard

## 📊 Model Performance

| Metric | Score |
|---|---|
| R² Score | 0.925 |
| MAE | 0.475 |
| RMSE | 0.347 |

## 🖥️ Features

- Interactive sliders for height and weight
- Gender selection
- Real-time shoe size prediction with confidence range
- Gauge chart visualization
- Model performance overview in the sidebar

## 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/shoe-size-prediction.git
cd shoe-size-prediction
pip install -r requirements.txt
streamlit run main.py
```

## 🛠️ Tech Stack

- Python
- scikit-learn (Linear Regression)
- Streamlit (dashboard/UI)
- Plotly (visualizations)
- Pandas / NumPy

## 📁 Project Structure

```
shoe-size-prediction/
├── main.py                 # Streamlit app
├── requirements.txt        # Dependencies
└── models/
    └── shoe_size_model_artifact.pkl   # Trained model
```

## 📄 License

This project is open source and available under t
he [MIT License](LICENSE).