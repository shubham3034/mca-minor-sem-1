import streamlit as st
import random
import pandas as pd
import plotly.express as px

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Eco Awareness Portal",
                   layout="wide",
                   page_icon="🌿")

# ------------------------------
# SIDEBAR NAVIGATION
# ------------------------------
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Biotic Components", "Abiotic Components",
                                  "Environmental Charts", "Quiz"])

# =====================================================================
# HOME PAGE
# =====================================================================

if page == "Home":
    st.title("🌿 Eco Awareness Portal")
    st.subheader("Biotic & Abiotic Components of Environment")
    st.write("""
    This portal helps users understand how living (biotic) and non-living (abiotic)
    components interact to shape the environment.  
    Explore the modules to learn, visualize, and test your awareness!
    """)

    st.image("https://cdn.pixabay.com/photo/2020/05/28/16/29/environment-5231737_1280.jpg")

    st.info("Use the left navigation panel to explore the content.")

# =====================================================================
# BIOTIC COMPONENTS
# =====================================================================

elif page == "Biotic Components":
    st.title("🌱 Biotic Components")
    st.write("""
    Biotic components are **living organisms** in the environment, such as:
    - Plants  
    - Animals  
    - Microorganisms  
    """)

    st.subheader("Examples")
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cdn.pixabay.com/photo/2016/10/18/21/21/forest-1758766_1280.jpg")
        st.caption("Plants – Primary producers")

    with col2:
        st.image("https://cdn.pixabay.com/photo/2018/03/28/17/24/tiger-3278854_1280.jpg")
        st.caption("Animals – Consumers")

    st.write("""
    Biotic components depend on abiotic factors such as sunlight, water, temperature, and soil nutrients.
    """)

# =====================================================================
# ABIOTIC COMPONENTS
# =====================================================================

elif page == "Abiotic Components":
    st.title("🌞 Abiotic Components")
    st.write("""
    Abiotic components include **non-living physical and chemical parts** of the environment:
    - Water  
    - Air  
    - Soil  
    - Temperature  
    - Light  
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cdn.pixabay.com/photo/2016/11/29/03/28/water-1867697_1280.jpg")
        st.caption("Water – Essential for all life")

    with col2:
        st.image("https://cdn.pixabay.com/photo/2016/11/18/16/52/nature-1834663_1280.jpg")
        st.caption("Soil – Habitat & nutrients for plants")

    st.success("Abiotic factors directly influence the survival of biotic organisms.")

# =====================================================================
# ENVIRONMENTAL CHARTS
# =====================================================================

elif page == "Environmental Charts":
    st.title("📊 Environmental Interaction Charts")

    st.write("Here is a simulated interaction chart showing how abiotic changes affect plant growth.")

    data = {
        "Temperature": ["Low", "Moderate", "High"],
        "Growth Rate": [20, 80, 40]
    }

    df = pd.DataFrame(data)
    fig = px.bar(df, x="Temperature", y="Growth Rate",
                 title="Effect of Temperature on Plant Growth")

    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    **Observation:**  
    - Moderate temperature results in maximum growth.  
    - Extreme conditions reduce plant productivity.  
    """)

# =====================================================================
# QUIZ PAGE
# =====================================================================

elif page == "Quiz":
    st.title("📝 Environmental Awareness Quiz")

    questions = {
        "Which of these is a biotic component?": ["Soil", "Plant", "Water", "Light"],
        "Which factor affects abiotic components?": ["Temperature", "Animals", "Plants", "Microbes"],
        "Oxygen is produced mainly by?": ["Animals", "Machines", "Plants", "Vehicles"],
        "Which is not an abiotic factor?": ["Air", "Sunlight", "Bacteria", "Water"]
    }

    answers = {
        "Which of these is a biotic component?": "Plant",
        "Which factor affects abiotic components?": "Temperature",
        "Oxygen is produced mainly by?": "Plants",
        "Which is not an abiotic factor?": "Bacteria"
    }

    score = 0
    user_answers = {}

    for q, options in questions.items():
        user_choice = st.radio(q, options)
        user_answers[q] = user_choice

    if st.button("Submit Quiz"):
        for q in questions:
            if user_answers[q] == answers[q]:
                score += 1

        st.success(f"Your Score: {score} / {len(questions)}")

        if score == 4:
            st.balloons()

        st.subheader("Correct Answers:")
        for q in answers:
            st.write(f"**{q}** → {answers[q]}")

