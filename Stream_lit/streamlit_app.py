import json
import streamlit as st
import requests

# Title of the app
st.title("Mobile Price Range Prediction")

# Dictionary to store user inputs
user_options = {}

# Define feature options and ranges
feature_options = {
    "slider_fields": {
        "BatteryPower": [500, 5000],
        "MobileWeight": [50, 300],
        "ClockSpeed": [0.5, 3.0],
        "IntMemory": [4, 256],
        "NCores": [1, 12],
        "PxHeight": [100, 4000],
        "PxWidth": [100, 4000],
        "RAM": [512, 12000],
    },
    "single_select_fields": {
        "DualSim": [0, 1],
        "FourG": [0, 1],
        "ThreeG": [0, 1],
        "TouchScreen": [0, 1],
        "Wifi": [0, 1],
        "Bluetooth": [0, 1],
    },
}

# Add sliders for numerical fields
for field_name, range_vals in feature_options["slider_fields"].items():
    min_val, max_val = range_vals
    current_value = (min_val + max_val) // 2
    user_options[field_name] = st.sidebar.slider(
        field_name, min_val, max_val, value=current_value
    )

# Add select boxes for categorical fields
for field_name, values in feature_options["single_select_fields"].items():
    user_options[field_name] = st.sidebar.selectbox(field_name, values)

# Display user input
st.write("User Input:", user_options)

# Predict button
if st.button("Predict"):
    # Convert input to JSON format
    data = json.dumps({"features": user_options}, indent=2)

    # API endpoint URL
    api_url = "http://localhost:8000/predict"  # Change this to your deployed API URL if necessary

    # Send request to the FastAPI model
    try:
        response = requests.post(
            api_url, data=data, headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Price Range: {result['prediction']}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
