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

# Function to find closest matching country based on input values
def find_closest_country(gdpp, income, child_mort):
    # Calculate differences with input values
    clustered_dataset['gdpp_diff'] = abs(clustered_dataset['gdpp'] - gdpp)
    clustered_dataset['income_diff'] = abs(clustered_dataset['income'] - income)
    clustered_dataset['child_mort_diff'] = abs(clustered_dataset['child_mort'] - child_mort)
    
    # Calculate total difference as a sum of differences
    clustered_dataset['total_diff'] = clustered_dataset['gdpp_diff'] + clustered_dataset['income_diff'] + clustered_dataset['child_mort_diff']
    
    # Find the country with the smallest total difference
    closest_country = clustered_dataset.loc[clustered_dataset['total_diff'].idxmin(), 'country']
    
    return closest_country

# Output Section
if submit_button:
    st.subheader("Input Values:")
    st.write(f"GDP per capita (gdpp): {gdpp}")
    st.write(f"Net Income per person (Income): {income}")
    st.write(f"Child Mortality (child_mort): {child_mort}")
    
    # Classify country based on input values
    classification = classify_country(gdpp, income, child_mort)
    
    # Find closest matching country
    closest_country = find_closest_country(gdpp, income, child_mort)
    
    st.subheader("Country Classification:")
    st.write(f"The provided values correspond to a {classification} country.")
    
    st.subheader("Closest Matching Country:")
    st.write(f"The closest matching country is: {closest_country}")
