# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import datetime
import os

st.set_page_config(page_title="Biotic & Abiotic Components — Awareness App", layout="centered")

# ---- Helper functions ----
@st.cache_data
def sample_dataset():
    # A small sample dataset describing observation sites with biotic and abiotic features
    data = {
        "Site": ["Park A", "River Bend", "Forest Edge", "Agricultural Field", "Urban Garden"],
        "Location_Type": ["Urban", "Riverside", "Forest", "Rural", "Urban"],
        "Soil_pH": [6.5, 7.1, 5.8, 6.9, 6.3],
        "Temperature_C": [29.1, 26.8, 24.3, 31.0, 28.0],
        "Moisture_%": [30, 45, 60, 25, 35],
        "Dominant_Biota": ["Grass, Trees", "Algae, Fish", "Trees, Shrubs", "Crops", "Flowering Plants"],
        "Human_Impact": ["Moderate", "Low", "Low", "High", "High"]
    }
    return pd.DataFrame(data)

def load_uploaded_csv(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error("Error reading CSV. Make sure it is a valid CSV file. Error: " + str(e))
        return None

def numeric_columns(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

def save_pledge(name, email, pledge_text):
    # Append to a CSV in the working directory (Streamlit Cloud persists between runs per app)
    filename = "pledges.csv"
    row = {"timestamp": datetime.datetime.now().isoformat(), "name": name, "email": email, "pledge": pledge_text}
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(filename, index=False)
    return True

# ---- Layout ----
st.title("Biotic & Abiotic Components — Environmental Awareness (MCA Project)")
st.markdown("""
This interactive app demonstrates the relationships between **biotic** (living) and **abiotic** (non-living) components of the environment,
provides simple visualization, and includes an awareness quiz and pledge capture for user engagement.
""")

st.sidebar.header("Controls")
mode = st.sidebar.radio("App mode", ["Overview", "Explore Dataset", "Visualize", "Quiz & Pledge", "Upload Data / Admin"])

# ---- Overview ----
if mode == "Overview":
    st.header("Overview")
    st.markdown("""
    **Biotic components**: living organisms such as plants, animals, fungi, bacteria — they interact and form ecosystems.

    **Abiotic components**: non-living physical and chemical factors such as sunlight, temperature, water, soil pH, nutrients, moisture.

    Understanding the interplay is crucial for environmental awareness and conservation.
    """)
    st.subheader("How to use this app")
    st.markdown("""
    1. Explore the sample dataset under *Explore Dataset* or upload your own CSV under *Upload Data*.  
    2. Visualize numeric abiotic factors and compare sites.  
    3. Take the quick quiz to test understanding and submit a pledge to encourage awareness.
    """)
    st.subheader("Sample dataset preview")
    st.dataframe(sample_dataset())

# ---- Explore Dataset ----
elif mode == "Explore Dataset":
    st.header("Explore Dataset")
    st.markdown("You can use the provided sample dataset or upload your own CSV (columns with numeric abiotic values are auto-detected).")

    use_sample = st.checkbox("Use sample dataset", value=True)
    if use_sample:
        df = sample_dataset()
    else:
        uploaded = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded is not None:
            df = load_uploaded_csv(uploaded)
        else:
            st.info("No file uploaded. Showing sample dataset.")
            df = sample_dataset()

    if df is not None:
        st.subheader("Dataset (first 50 rows)")
        st.dataframe(df.head(50))

        st.subheader("Column descriptions")
        for c in df.columns:
            typ = df[c].dtype
            st.write(f"- **{c}** — type: {typ}")

        st.subheader("Filter by site or location type")
        if "Site" in df.columns:
            site = st.selectbox("Select Site (optional)", options=["(all)"] + list(df["Site"].unique()))
            if site != "(all)":
                df = df[df["Site"] == site]
        if "Location_Type" in df.columns:
            ltype = st.selectbox("Select Location Type (optional)", options=["(all)"] + list(df["Location_Type"].unique()))
            if ltype != "(all)":
                df = df[df["Location_Type"] == ltype]

        st.write("Filtered data:")
        st.dataframe(df)

# ---- Visualize ----
elif mode == "Visualize":
    st.header("Visualize Abiotic Factors")
    st.markdown("Select numeric columns (abiotic factors) to visualize and compare across sites.")
    # load dataset (prefer previously uploaded or sample)
    uploaded = st.file_uploader("Upload CSV for visualization (optional)", type=["csv"], key="viz_upload")
    if uploaded is not None:
        df = load_uploaded_csv(uploaded)
        if df is None:
            st.stop()
    else:
        df = sample_dataset()

    num_cols = numeric_columns(df)
    if not num_cols:
        st.warning("No numeric columns detected in dataset.")
    else:
        st.subheader("Select numeric column to plot")
        column = st.selectbox("Numeric column", num_cols)
        group_by = None
        if "Site" in df.columns:
            group_by = st.selectbox("Group by (optional)", options=["None", "Site", "Location_Type"])
            if group_by == "None":
                group_by = None

        # Plotting
        st.write(f"Plotting `{column}` across rows")
        fig, ax = plt.subplots(figsize=(8, 4))
        if group_by and group_by in df.columns:
            # boxplot per group
            df.boxplot(column=column, by=group_by, ax=ax)
            ax.set_title(f"{column} by {group_by}")
            ax.set_ylabel(column)
            plt.suptitle("")  # remove the automatic suptitle
        else:
            ax.plot(df.index, df[column], marker='o', linestyle='-')
            ax.set_xlabel("Index")
            ax.set_ylabel(column)
            ax.set_title(column)
        st.pyplot(fig)

        st.subheader("Summary statistics")
        st.dataframe(df[num_cols].describe().transpose())

# ---- Quiz & Pledge ----
elif mode == "Quiz & Pledge":
    st.header("Quick Quiz — Test your knowledge")
    score = 0
    # Simple 3-question MCQ
    q1 = st.radio("1) Which of the following is an abiotic factor?", ("Trees", "Soil pH", "Bacteria", "Fungi"))
    q2 = st.radio("2) Which is a biotic component?", ("Water", "Sunlight", "Algae", "Temperature"))
    q3 = st.radio("3) Which abiotic factor strongly affects species distribution?", ("Soil texture", "Birds", "Mushrooms", "Decomposers"))

    if st.button("Submit Quiz"):
        if q1 == "Soil pH":
            score += 1
        if q2 == "Algae":
            score += 1
        if q3 == "Soil texture":
            score += 1
        st.success(f"You scored {score} / 3")
        if score == 3:
            st.balloons()
        st.write("Correct answers: 1) Soil pH, 2) Algae, 3) Soil texture")

    st.markdown("---")
    st.header("Awareness Pledge")
    st.write("Write a short pledge to protect your local environment. We'll save it (anonymously if you prefer) to the app storage.")
    with st.form("pledge_form"):
        name = st.text_input("Name (optional)")
        email = st.text_input("Email (optional)")
        pledge_text = st.text_area("Your pledge", max_chars=500, help="Example: I will plant 1 tree this year and avoid single-use plastic.")
        submitted = st.form_submit_button("Submit pledge")
        if submitted:
            if not pledge_text or pledge_text.strip() == "":
                st.error("Please write a short pledge before submitting.")
            else:
                saved = save_pledge(name or "Anonymous", email or "", pledge_text)
                if saved:
                    st.success("Thank you — your pledge has been saved.")
                    st.write("---")
                    st.write("Latest pledges (most recent 5):")
                    if os.path.exists("pledges.csv"):
                        pledges_df = pd.read_csv("pledges.csv")
                        st.dataframe(pledges_df.tail(5).iloc[::-1].reset_index(drop=True))
                    else:
                        st.info("No pledges saved yet.")
# ---- Upload data / Admin ----
elif mode == "Upload Data / Admin":
    st.header("Upload dataset for use across app")
    st.markdown("Upload a CSV that contains site rows and abiotic numeric columns like Temperature, Soil_pH, Moisture, etc. Use column `Site` for site names if present.")
    uploaded = st.file_uploader("Upload CSV to save as dataset (will replace previous 'uploaded_dataset.csv')", type=["csv"])
    if uploaded:
        try:
            df_uploaded = pd.read_csv(uploaded)
            df_uploaded.to_csv("uploaded_dataset.csv", index=False)
            st.success("Uploaded and saved as `uploaded_dataset.csv` in app storage.")
            st.dataframe(df_uploaded.head(20))
        except Exception as e:
            st.error("Failed to save uploaded CSV. Error: " + str(e))

    if os.path.exists("uploaded_dataset.csv"):
        st.write("Previously uploaded dataset preview:")
        st.dataframe(pd.read_csv("uploaded_dataset.csv").head(20))
    else:
        st.info("No saved uploaded dataset found. The app will use the built-in sample dataset.")

# ---- Footer ----
st.markdown("---")
st.markdown("**Project (MCA)** — Interactive educational app on Biotic & Abiotic environmental components. Developed with Streamlit.")
