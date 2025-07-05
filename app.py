import streamlit as st
import numpy as np
import pandas as pd
import joblib
import math
import plotly.graph_objects as go

# --- Load Model ---
model = joblib.load("C:\\Users\\Dell\\OneDrive - City Community Education Consultancy Pvt. Ltd\\Desktop\\Music_analysis\\yt_analyzer.pkl")

# --- Feature list (Must match what model was trained on) ---
# Example: 'Transformed_target_7' was removed
selected_features = [
    'thumbnail_brightness',
    'subscriber_count',
    'upload_hour',
    'title_length',
    'discription_length_transformed',
    'transformed_tags_count',
    'Transformed_duration_sec',
    'uploade_day_sin',
    'uploade_day_cos'
]

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Analyzer", layout="centered")
st.title("📊 YouTube Video Performance Analyzer")
st.markdown("Enter your video details to predict expected performance score.")

# --- Input Fields ---
thumbnail_brightness = st.slider("Thumbnail Brightness (0 to 1)", 0.0, 1.0, 0.5)
subscriber_count = st.number_input("Subscriber Count", min_value=0, value=1000)
upload_hour = st.selectbox("Upload Hour (24-hr)", list(range(0, 24)))
title_length = st.number_input("Title Length (characters)", min_value=1, value=50)
description_length = st.number_input("Description Length (words)", min_value=1, value=300)
tags_count = st.number_input("Number of Tags", min_value=0, value=5)
duration_sec = st.number_input("Video Duration (seconds)", min_value=1, value=300)

# --- Upload Day sin/cos encoding ---
upload_day = st.selectbox("Upload Day", ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
day_to_num = {
    'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
    'Thursday': 4, 'Friday': 5, 'Saturday': 6
}
day_num = day_to_num[upload_day]
upload_day_sin = math.sin(2 * math.pi * day_num / 7)
upload_day_cos = math.cos(2 * math.pi * day_num / 7)

# --- Prepare input dictionary ---
input_dict = {
    'thumbnail_brightness': thumbnail_brightness,
    'subscriber_count': subscriber_count,
    'upload_hour': upload_hour,
    'title_length': title_length,
    'discription_length_transformed': description_length,
    'transformed_tags_count': tags_count,
    'Transformed_duration_sec': duration_sec,
    'uploade_day_sin': upload_day_sin,
    'uploade_day_cos': upload_day_cos
}

# --- Create input DataFrame ---
input_df = pd.DataFrame([input_dict])[selected_features]

# --- Predict and display results ---
if st.button("🔍 Analyze Now"):
    try:
        prediction = model.predict(input_df).item()  # ✅ FIXED: extract float from array

        st.subheader("🎯 Predicted Performance Score")
        st.metric(label="Estimated Score", value=f"{prediction:.2f}")

        # --- Gauge Chart ---
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={'text': "Performance Score"},
            gauge={'axis': {'range': [0, 1]}, 'bar': {'color': "red"}}
        ))
        st.plotly_chart(fig)

        # --- Optional Tip ---
        st.markdown("💡 **Tip:** Upload between 5–8 PM, use catchy titles, bright thumbnails, and 5–10 tags for best results.")

    except Exception as e:
        st.error(f"Prediction failed: {e}")
