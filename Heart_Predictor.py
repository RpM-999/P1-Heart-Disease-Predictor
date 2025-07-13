import streamlit as st
import pandas as pd                                                                                       #----------> Import Libraries
import numpy as np
import joblib

Hdp_model = joblib.load("Heart_Disease_Predictor_Model.pkl")                                                     #----------> Load the Heart_Desease_Predictor_Model
Sc_model = joblib.load("scaler.pkl")


st.image("logo.png", width=300)
st.title(" 🫀 Heart Disease Prediction App")                                                                  #----------> Name of the App

st.markdown("### 🧪 About This App")
st.write("This app predicts the likelihood of a person having heart disease based on various medical and lifestyle factors.")       #--------->Description


st.sidebar.header("Input Patient Data")



def user_data():
    with st.sidebar.expander("🧑‍⚕️ Personal & Medical Info"):
        age = st.slider("Age", 20, 90, 50)
        gender = st.radio("Gender", ["Male", "Female"])
        family_history = 1 if st.radio("Family History of Heart Disease", ["Yes", "No"]) == "Yes" else 0
        diabetes = 1 if st.radio("Diabetes", ["Yes", "No"]) == "Yes" else 0
        obesity = 1 if st.radio("Obesity", ["Yes", "No"]) == "Yes" else 0
        angina = 1 if st.radio("Exercise Induced Angina", ["Yes", "No"]) == "Yes" else 0

    with st.sidebar.expander("💉 Medical Measurements"):
        cholesterol = st.slider("Cholesterol (mg/dL)", 100, 400, 200)
        bp = st.slider("Blood Pressure (mm Hg)", 80, 200, 120)
        heart_rate = st.slider("Heart Rate (bpm)", 60, 200, 100)
        blood_sugar = st.slider("Blood Sugar (mg/dL)", 70, 300, 120)

    with st.sidebar.expander("🏃 Lifestyle Details"):
        exercise_hours = st.slider("Exercise Hours per Week", 0, 14, 3)
        stress = st.slider("Stress Level (1 = Low, 10 = High)", 1, 10, 5)
        smoking_status = st.radio("Smoking Status", ["Former", "Never", "Current"])
        alcohol_intake = st.radio("Alcohol Intake", ["Moderate", "Unknown", "High"])
        chest_pain_type = st.radio("Chest Pain Type", ["Atypical Angina", "Non-anginal Pain", "Typical Angina", "Asymptomatic"])



    smoking_former = 1 if smoking_status == "Former" else 0
    smoking_never = 1 if smoking_status == "Never" else 0

    alcohol_moderate = 1 if alcohol_intake == "Moderate" else 0
    alcohol_unknown = 1 if alcohol_intake == "Unknown" else 0

    cp_atypical = 1 if chest_pain_type == "Atypical Angina" else 0
    cp_non_anginal = 1 if chest_pain_type == "Non-anginal Pain" else 0
    cp_typical = 1 if chest_pain_type == "Typical Angina" else 0

    gender_numeric = 1 if gender == "Male" else 0


    data = {
        "Age": age,
        "Gender": gender_numeric,
        "Cholesterol": cholesterol,
        "Blood Pressure": bp,
        "Heart Rate": heart_rate,
        "Exercise Hours": exercise_hours,
        "Family History": family_history,
        "Diabetes": diabetes,
        "Obesity": obesity,
        "Stress Level": stress,
        "Blood Sugar": blood_sugar,
        "Exercise Induced Angina": angina,
        "Smoking_Former": smoking_former,
        "Smoking_Never": smoking_never,
        "Alcohol Intake_Moderate": alcohol_moderate,
        "Alcohol Intake_Unknown": alcohol_unknown,
        "Chest Pain Type_Atypical Angina": cp_atypical,
        "Chest Pain Type_Non-anginal Pain": cp_non_anginal,
        "Chest Pain Type_Typical Angina": cp_typical,
    }

    return pd.DataFrame(data, index=[0])


input_df = user_data()

st.subheader("📝 Patient Input Data")                                   #----------> Display User Given Data
st.write(input_df.T)


numeric_col = ['Age', 'Cholesterol', 'Blood Pressure', 'Heart Rate', 'Exercise Hours', 'Stress Level', 'Blood Sugar']

input_df[numeric_col] = Sc_model.transform(input_df[numeric_col])       #----------> Before Prediction Scale the Numeric Inputs 



prediction = Hdp_model.predict(input_df)[0]                             #----------> Try to Predict

proba = Hdp_model.predict_proba(input_df)[0][1] * 100                   #----------> Calculate Probability of Confidence in %





st.subheader("📊 Prediction Result")                                    #----------> Prediction


if proba < 30:
    risk = "Low"
elif proba < 70:
    risk = "Moderate"
else:
    risk = "High"


if prediction == 1:
    st.error(f"⚠️ This person might have a **high chance of heart disease**.\n\n🔴 Risk Level: **{proba:.2f}%**")           # ---------->Display prediction message
else:
    st.success(f"✅ This person is **most likely healthy** and has a **low chance of heart disease**.\n\n🟢 Risk Level: **{proba:.2f}%**")

st.info(f"🧠 Risk Confidence Level: **{risk}**")                                                                               #----------> Display Risk Category Info





st.markdown("---")
st.caption("Developed by Rupam Mondal • Model: 🫀 Heart Desease Predictor • Version 1.0")


