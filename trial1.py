# Importing required libraries
import streamlit as st
import pandas as pd

# Load your clustered dataset
clustered_dataset = pd.read_csv("Country_data.csv")

# Streamlit UI
st.title("Fund Allocation Based on Clustering")

# Input Section
st.sidebar.title("Input Section")

# Data Input Fields
gdpp = st.sidebar.number_input("Enter GDP per capita (gdpp):", min_value=0)
income = st.sidebar.number_input("Enter Net Income per person (Income):", min_value=0)
child_mort = st.sidebar.number_input("Enter Child Mortality (child_mort):", min_value=0)

submit_button = st.sidebar.button("Submit")

# Function to classify country
def classify_country(gdpp, income, child_mort):
    if gdpp > 50000 or income > 40000:
        return "Developed"
    elif gdpp < 10000 or income < 1000 or child_mort > 50:
        return "Underdeveloped"
    else:
        return "Developing"

# Output Section
if submit_button:
    st.subheader("Input Values:")
    st.write(f"GDP per capita (gdpp): {gdpp}")
    st.write(f"Net Income per person (Income): {income}")
    st.write(f"Child Mortality (child_mort): {child_mort}")
    
    # Classify country based on input values
    classification = classify_country(gdpp, income, child_mort)
    st.subheader("Country Classification:")
    st.write(f"The provided values correspond to a {classification} country.")
