import streamlit as st
import pandas as pd
import base64

# Function to encode local image to Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Provide correct local path of the image
image_path = "image.webp"  # Ensure this file is in the same directory
try:
    base64_image = get_base64_of_image(image_path)
except FileNotFoundError:
    base64_image = None

# Custom CSS for Background Image & Styling
if base64_image:
    page_bg_img = f'''
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                    url("data:image/png;base64,{base64_image}") no-repeat center center fixed;
        background-size: cover;
        color: white;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Title & Introduction
st.title("🏋 Personal Fitness & Diet Tracker")
st.write("### Track your health, stay fit, and get personalized diet recommendations!")

# Load diet dataset
try:
    diet_df = pd.read_csv("dietchartdataset.csv")  # Ensure this file is uploaded
except FileNotFoundError:
    diet_df = None
    st.error("⚠ Diet dataset not found! Please add 'dietchartdataset.csv' to your app directory.")

# Sidebar for User Input
st.sidebar.header("🔹 Enter Your Details")
age = st.sidebar.number_input("Age:", min_value=5, max_value=100, step=1)
height = st.sidebar.number_input("Height (cm):", min_value=50, max_value=250, step=1)
weight = st.sidebar.number_input("Weight (kg):", min_value=10, max_value=300, step=1)
steps = st.sidebar.number_input("Daily Steps:", min_value=0, step=100)
workout = st.sidebar.number_input("Workout Minutes:", min_value=0, step=5)
sleep = st.sidebar.number_input("Sleep Hours:", min_value=0.0, step=0.5)

# BMI Calculator
def calculate_bmi(weight, height):
    if height > 0:
        return round(weight / ((height / 100) ** 2), 2)
    return None

# Calories Burned Calculator
def calculate_calories_burned(steps, workout, weight):
    return round((steps * 0.04) + (workout * 7), 2)

# Fitness Recommendation
def recommend_workout(steps, workout, sleep, bmi):
    step_advice = "<span style='color:red'>Great job! Maintain your activity level.</span>" if steps >= 10000 else "<span style='color:red'>Try to hit 10,000 steps daily.</span>"
    workout_advice = "<span style='color:red'>You're working out enough!</span>" if workout >= 30 else "<span style='color:red'>Increase your workout time to at least 30 minutes.</span>"
    sleep_advice = "<span style='color:red'>Your sleep is good!</span>" if sleep >= 6 else "<span style='color:red'>Try to get 7-8 hours of sleep.</span>"
    bmi_advice = f"<span style='color:red'>Your BMI is {bmi}, which is in the "

    if bmi < 18.5:
        bmi_advice += "**Underweight** category. Consider gaining some weight.</span>"
    elif 18.5 <= bmi < 25:
        bmi_advice += "**Healthy Weight** range. Keep up the good work!</span>"
    elif 25 <= bmi < 30:
        bmi_advice += "**Overweight** category. Consider adjusting your diet & exercise.</span>"
    else:
        bmi_advice += "**Obese** category. Focus on fitness & a balanced diet.</span>"

    return f"{step_advice} {workout_advice} {sleep_advice} {bmi_advice}"

# Generate Diet Chart based on BMI
def generate_diet_chart(bmi):
    if diet_df is not None and 'BMI_Category' in diet_df.columns and 'Meal_Example' in diet_df.columns:
        if bmi < 18.5:
            return diet_df[diet_df['BMI_Category'] == 'Underweight']['Meal_Example'].values[0]
        elif 18.5 <= bmi < 25:
            return diet_df[diet_df['BMI_Category'] == 'Healthy Weight']['Meal_Example'].values[0]
        elif 25 <= bmi < 30:
            return diet_df[diet_df['BMI_Category'] == 'Overweight']['Meal_Example'].values[0]
        else:
            return diet_df[diet_df['BMI_Category'] == 'Obese']['Meal_Example'].values[0]
    return "No diet data available."

# Process User Data
bmi = calculate_bmi(weight, height)
calories_burned = calculate_calories_burned(steps, workout, weight)
diet_chart = generate_diet_chart(bmi)

if st.sidebar.button("<span style='color:red'>Get Recommendation</span>", unsafe_allow_html=True):
    st.subheader("📊 Your Fitness Summary")
    st.write(f"🔥 **Calories Burned Today:** {calories_burned} kcal")
    st.write(f"⚖ **Your BMI:** {bmi}")

    result = recommend_workout(steps, workout, sleep, bmi)
    st.markdown(result, unsafe_allow_html=True)

    st.markdown("### <span style='color:white'>🥗 Recommended Diet Plan</span>", unsafe_allow_html=True)
    if diet_chart != "No diet data available.":
        st.markdown(f"<span style='color:red'>🍽 **Recommended Meal:** {diet_chart}</span>", unsafe_allow_html=True)
    else:
        st.warning("No diet recommendations available. Please check 'dietchartdataset.csv'.")
