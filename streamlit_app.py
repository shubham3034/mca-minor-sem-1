import streamlit as st

# ----------- Nature Theme CSS -----------
nature_css = """
<style>
/* Background Gradient */
body {
    background: linear-gradient(135deg, #dff1d8 0%, #c2e9c4 50%, #b3e6ba 100%);
}

/* Main container */
.main {
    background-color: rgba(255,255,255,0.6) !important;
    border-radius: 12px;
    padding: 20px;
}

/* Title */
h1 {
    color: #1f6f43 !important;
    font-family: 'Trebuchet MS', sans-serif;
    font-weight: 900;
}

/* Subheadings */
h2, h3, h4 {
    color: #245e38 !important;
}

/* Info & warning boxes */
.stAlert {
    border-radius: 12px !important;
}

/* Sliders */
.css-14xtw13 {
    background-color: #7bc47f !important;
}

/* Divider line */
hr {
    border: 1px solid #2d8a47;
}
</style>
"""

st.set_page_config(page_title="Pollution Impact Analyzer", page_icon="🌿")

# Inject CSS
st.markdown(nature_css, unsafe_allow_html=True)

# ----------- App Content -----------
st.title("🌿 Pollution Impact")
st.write("### A nature-inspired tool to understand how pollution affects plants and animals.")

st.write("---")
st.write("## 🌱 Enter Pollution Parameters")

aqi = st.slider("Air Quality Index (AQI)", 0, 500, 100)
noise = st.slider("Noise Level (dB)", 20, 150, 60)
temperature = st.slider("Temperature (°C)", -10, 50, 25)

st.write("---")

# ----------- Rule-based logic -----------
def analyze_plants(aqi, temperature):
    if aqi > 300:
        return "❌ Extremely harmful for plant growth. Leaf damage likely."
    elif aqi > 150:
        return "⚠ Moderate harm. Reduced growth and photosynthesis."
    else:
        return "✅ Safe air quality. Normal plant growth possible."

def analyze_animals(aqi, noise, temperature):
    msg = ""
    if aqi > 300:
        msg += "❌ Very poor air quality — harmful to animal lungs.\n"
    elif aqi > 150:
        msg += "⚠ Some breathing issues for animals.\n"
    else:
        msg += "✅ Air quality suitable for animals.\n"
    
    if noise > 120:
        msg += "❌ Extreme noise — can cause hearing loss in animals.\n"
    elif noise > 80:
        msg += "⚠ Stressful noise levels for wildlife.\n"
    else:
        msg += "✅ Noise level is acceptable for most animals.\n"
    
    return msg

# ----------- Display Results -----------
st.write("## 🌳 Plant Impact")
st.info(analyze_plants(aqi, temperature))

st.write("## 🦌 Animal Impact")
st.warning(analyze_animals(aqi, noise, temperature))

st.write("---")
st.write("### 🌎 Let's protect our environment by understanding how abiotic factors affect all living things.")
