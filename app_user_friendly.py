import streamlit as st
import joblib
import numpy as np

# Page setup
st.set_page_config(page_title="Diabetes Pro", page_icon="🩺", layout="centered")

# Load model
@st.cache_resource
def load_model():
    return joblib.load('diabetes_model.joblib')

model = load_model()

# Header
st.markdown("---")
st.markdown("### 🧠 Developed by **M Fayaz Khan**")
st.markdown("# 🩺 **Diabetes Risk Checker**")
st.markdown("### *Quick Health Assessment*")

# SIMPLE INPUTS - No medical tests required
with st.form("simple_form"):
    st.markdown("### 📝 **Your Health Profile**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("**Your Age**", 20, 80, 30)
        weight = st.number_input("**Weight (kg)**", 30, 150, 70)
        height = st.number_input("**Height (cm)**", 120, 220, 170)
        
        # Calculate BMI automatically
        if height > 0:
            bmi = weight / ((height/100) ** 2)
            st.metric("**Your BMI**", f"{bmi:.1f}")
    
    with col2:
        family_diabetes = st.selectbox(
            "**Family Diabetes History**",
            ["None", "Parents", "Siblings", "Both"]
        )
        
        physical_activity = st.selectbox(
            "**Physical Activity**", 
            ["Daily", "3-4 times/week", "Once a week", "Rarely"]
        )
        
        diet = st.selectbox(
            "**Diet Type**",
            ["Healthy/Balanced", "Mixed", "High Sugar/Fat", "Junk Food"]
        )
    
    # Map simple inputs to medical features
    submitted = st.form_submit_button("🎯 **Check My Risk**", use_container_width=True)

if submitted:
    # Convert simple inputs to medical features (approximate)
    pregnancies = 0  # Assuming not pregnant for general use
    
    # Estimate glucose based on lifestyle
    if diet == "High Sugar/Fat" or physical_activity == "Rarely":
        glucose = 160  # High estimate
    else:
        glucose = 110  # Normal estimate
    
    # Estimate BP based on age and activity
    bp = 75 if age < 40 else 85
    
    # Estimate other parameters
    skin_thickness = 25 if bmi < 25 else 35
    insulin = 120 if glucose > 140 else 80
    
    # Estimate diabetes pedigree from family history
    dpf_map = {"None": 0.3, "Parents": 0.6, "Siblings": 0.7, "Both": 0.9}
    dpf = dpf_map[family_diabetes]
    
    features = [pregnancies, glucose, bp, skin_thickness, insulin, bmi, dpf, age]
    
    # Prediction
    prediction = model.predict([features])
    probability = model.predict_proba([features])[0][1]
    
    # Display results
    st.markdown("---")
    st.markdown("## 📊 **Your Health Report**")
    
    st.progress(float(probability))
    st.write(f"**Diabetes Risk: {probability:.1%}**")
    
    if prediction[0] == 1:
        st.error("## ⚠️ **Higher Risk Detected**")
        st.warning("Consider consulting a doctor for proper tests")
    else:
        st.success("## ✅ **Lower Risk Profile**")
        st.info("Maintain your healthy lifestyle!")
    
    # Lifestyle recommendations
    st.markdown("### 💡 **Health Tips**")
    if physical_activity == "Rarely":
        st.write("• 🏃 **Start exercising regularly**")
    if diet in ["High Sugar/Fat", "Junk Food"]:
        st.write("• 🥗 **Improve your diet**")
    if bmi > 25:
        st.write("• ⚖️ **Manage your weight**")

# Footer
st.markdown("---")
st.markdown("### 📝 **Note**")
st.caption("This is a screening tool based on lifestyle factors. For accurate diagnosis, consult a doctor and get proper medical tests.")