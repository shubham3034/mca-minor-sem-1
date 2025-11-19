import streamlit as st
import plotly.express as px
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Eco Awareness Portal", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🌿 Eco Awareness Portal")
page = st.sidebar.radio("Go to:", ["Home", "Biotic Components", "Abiotic Components", "Interactive Charts", "Awareness Quiz"])

# ------------------ HOME PAGE ------------------
if page == "Home":
    st.title("🌍 Eco Awareness Web Portal")
    st.subheader("Biotic & Abiotic Components of Environment")

    st.write("""
    This interactive portal helps you understand environmental components and their relationship
    through visuals, explanations, and quizzes. Explore the biotic and abiotic factors that shape
    our ecosystem and learn why environmental awareness is important.
    """)

    st.image(
        "https://cdn.pixabay.com/photo/2016/11/29/03/09/earth-1867465_1280.jpg",
        use_container_width=True
    )

# ------------------ BIOTIC PAGE ------------------
elif page == "Biotic Components":
    st.title("🌱 Biotic Components")

    st.write("""
    Biotic components refer to all **living things** in the environment:
    - Plants  
    - Animals  
    - Microorganisms  
    """)

    st.image(
        "https://cdn.pixabay.com/photo/2014/04/03/11/07/forest-309495_1280.png",
        use_container_width=True
    )

    st.write("""
    Biotic components interact with abiotic factors like light, water, and temperature.
    Healthy biotic life indicates a stable ecosystem.
    """)

# ------------------ ABIOTIC PAGE ------------------
elif page == "Abiotic Components":
    st.title("🌊 Abiotic Components")

    st.write("""
    Abiotic components are **non-living physical and chemical** elements:
    - Water  
    - Air  
    - Soil  
    - Temperature  
    - Sunlight  
    """)

    st.image(
        "https://cdn.pixabay.com/photo/2017/03/27/14/58/water-2188121_1280.jpg",
        use_container_width=True
    )

    st.write("""
    Abiotic factors influence the growth, survival, and reproduction of biotic organisms.
    Changes in abiotic components directly affect ecosystems.
    """)

# ------------------ INTERACTIVE CHARTS PAGE ------------------
elif page == "Interactive Charts":
    st.title("📊 Environmental Data Visualization")

    st.write("Below is a **simulated environmental dataset** showing variations in factors affecting ecosystems.")

    # Simulated Data
    data = pd.DataFrame({
        "Temperature (°C)": [18, 20, 22, 25, 30, 32, 35],
        "Humidity (%)": [80, 75, 70, 65, 60, 55, 50],
        "CO2 Level (ppm)": [360, 380, 400, 420, 450, 470, 500]
    })

    st.write("### Temperature Trend")
    fig1 = px.line(data, y="Temperature (°C)", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.write("### Humidity Variation")
    fig2 = px.line(data, y="Humidity (%)", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.write("### CO₂ Level Rise")
    fig3 = px.line(data, y="CO2 Level (ppm)", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

# ------------------ AWARENESS QUIZ ------------------
elif page == "Awareness Quiz":
    st.title("📝 Environmental Awareness Quiz")

    st.write("Answer the following to test your awareness:")

    q1 = st.radio("1. Which of the following is a **biotic** component?",
                  ["Air", "Water", "Plants", "Sunlight"])
    q2 = st.radio("2. Which factor affects biotic life the most?",
                  ["Wind", "Temperature", "Plastic", "Soil nutrients"])
    q3 = st.radio("3. Increasing CO₂ levels mainly affect:",
                  ["Soil Quality", "Oxygen Levels", "Rainfall Patterns", "All of these"])

    if st.button("Submit Quiz"):
        score = 0
        if q1 == "Plants": score += 1
        if q2 == "Temperature": score += 1
        if q3 == "All of these": score += 1

        st.success(f"Your Score: {score} / 3")

        if score == 3:
            st.balloons()
            st.write("Excellent! You understand the environment very well.")
        elif score == 2:
            st.write("Good job! Improve a little more.")
        else:
            st.write("Keep learning! Explore the portal to improve your knowledge.")
