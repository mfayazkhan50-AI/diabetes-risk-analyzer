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

# Header with better styling
st.markdown("---")
st.markdown("### 🧠 Developed by **M Fayaz Khan**")
st.markdown("# 🩺 **Diabetes Risk Analyzer**")
st.markdown("### *Professional Medical Assessment Tool*")

# Input form with improved fields
with st.form("medical_form"):
    st.markdown("### 📋 **Patient Health Profile**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔹 Personal Metrics")
        pregnancies = st.number_input(
            "**Pregnancy Count**", 
            min_value=0, max_value=10, value=0,
            help="Total number of pregnancies"
        )
        
        glucose = st.number_input(
            "**Blood Glucose**", 
            min_value=50, max_value=300, value=100,
            help="Plasma glucose concentration (mg/dL)"
        )
        
        bp = st.number_input(
            "**Blood Pressure**", 
            min_value=40, max_value=120, value=70,
            help="Diastolic blood pressure (mm Hg)"
        )
        
        skin_thickness = st.number_input(
            "**Skin Fold Thickness**", 
            min_value=10, max_value=60, value=25,
            help="Triceps skin fold thickness (mm)"
        )
    
    with col2:
        st.markdown("#### 🔹 Body Composition")
        insulin = st.number_input(
            "**Insulin Level**", 
            min_value=0, max_value=300, value=100,
            help="2-Hour serum insulin (mu U/ml)"
        )
        
        bmi = st.number_input(
            "**Body Mass Index**", 
            min_value=15.0, max_value=50.0, value=25.0, step=0.1,
            help="BMI = weight(kg) / height(m)²"
        )
        
        dpf = st.number_input(
            "**Genetic Score**", 
            min_value=0.0, max_value=2.0, value=0.5, step=0.01,
            help="Diabetes pedigree function (genetic risk)"
        )
        
        age = st.number_input(
            "**Patient Age**", 
            min_value=20, max_value=80, value=30,
            help="Age in years"
        )
    
    # Better submit button
    submitted = st.form_submit_button(
        "🎯 **Calculate Diabetes Risk**", 
        type="primary",
        use_container_width=True
    )

# Results section with better colors
if submitted:
    st.markdown("---")
    st.markdown("## 📊 **Risk Assessment Report**")
    
    features = [pregnancies, glucose, bp, skin_thickness, insulin, bmi, dpf, age]
    prediction = model.predict([features])
    probability = model.predict_proba([features])[0][1]
    
    # Color-coded progress bar
    st.markdown(f"### 🎚️ **Risk Probability: {probability:.1%}**")
    
    if probability > 0.7:
        st.progress(float(probability))
        st.markdown("🔴 **High Risk Zone**")
    elif probability > 0.4:
        st.progress(float(probability)) 
        st.markdown("🟡 **Moderate Risk Zone**")
    else:
        st.progress(float(probability))
        st.markdown("🟢 **Low Risk Zone**")
    
    # Big result card with better colors
    if prediction[0] == 1:
        st.error(f"## ⚠️ **MEDICAL ATTENTION NEEDED**")
        st.warning("### High likelihood of diabetes detected")
        with st.expander("💡 **Immediate Action Plan**", expanded=True):
            st.success("• 🏥 **Consult physician immediately**")
            st.success("• 📊 **Monitor glucose levels daily**")
            st.success("• 🥗 **Follow diabetic diet plan**")
            st.success("• 🏃 **Start regular exercise routine**")
    else:
        st.success(f"## ✅ **HEALTHY STATUS**")
        st.info("### Low risk of diabetes")
        with st.expander("💡 **Preventive Care Plan**", expanded=True):
            st.success("• 👍 **Maintain current lifestyle**")
            st.success("• 🩺 **Annual health checkups**")
            st.success("• ⚖️ **Balanced diet & weight management**")
            st.success("• 🚶 **Regular physical activity**")
    
    # Health dashboard
    st.markdown("---")
    st.markdown("## 🩺 **Health Metrics Dashboard**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if glucose < 100:
            st.success(f"**Glucose**\n\n{glucose} mg/dL\n\n✅ Normal")
        elif glucose < 126:
            st.warning(f"**Glucose**\n\n{glucose} mg/dL\n\n⚠️ Prediabetic")
        else:
            st.error(f"**Glucose**\n\n{glucose} mg/dL\n\n🚨 Diabetic")
    
    with col2:
        if bmi < 25:
            st.success(f"**BMI**\n\n{bmi}\n\n✅ Healthy")
        elif bmi < 30:
            st.warning(f"**BMI**\n\n{bmi}\n\n⚠️ Overweight")
        else:
            st.error(f"**BMI**\n\n{bmi}\n\n🚨 Obese")
    
    with col3:
        if bp < 80:
            st.success(f"**BP**\n\n{bp} mmHg\n\n✅ Normal")
        elif bp < 90:
            st.warning(f"**BP**\n\n{bp} mmHg\n\n⚠️ Elevated")
        else:
            st.error(f"**BP**\n\n{bp} mmHg\n\n🚨 High")
    
    with col4:
        if age < 40:
            st.info(f"**Age**\n\n{age} years\n\n👶 Young")
        elif age < 60:
            st.info(f"**Age**\n\n{age} years\n\n👨 Middle")
        else:
            st.info(f"**Age**\n\n{age} years\n\n👴 Senior")

# Footer
st.markdown("---")
st.markdown("### 📝 **Disclaimer**")
st.caption("This tool provides risk assessment based on machine learning. Always consult healthcare professionals for medical diagnosis and treatment.")

# Instructions
with st.expander("❓ **How to Use This Tool**"):
    st.markdown("""
    ### 📖 User Guide:
    1. **Fill** all health measurements accurately
    2. **Click** 'Calculate Diabetes Risk' button  
    3. **Review** your personalized risk report
    4. **Follow** recommended action plan
    5. **Consult** doctor for professional advice
    """)