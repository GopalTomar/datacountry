import streamlit as st
import pandas as pd

# Load your clustered dataset
clustered_dataset = pd.read_csv("Country_data.csv")

st.title("Fund Allocation Based on Clustering")

# Input Section
st.sidebar.title("Input Section")

# Data Input Fields
gdpp = st.sidebar.number_input("Enter GDP per capita (gdpp):", min_value=0)
income = st.sidebar.number_input("Enter Net Income per person (Income):", min_value=0)
child_mort = st.sidebar.number_input("Enter Child Mortality (child_mort):", min_value=0)

submit_button = st.sidebar.button("Submit")

# Function to classify country based on clustering labels
def classify_country_by_cluster(cluster_id_km, cluster_id_hc):
    if cluster_id_km == 0 or cluster_id_hc == 0:
        return "Underdeveloped"
    elif cluster_id_km == 1 or cluster_id_hc == 1:
        return "Developing"
    else:
        return "Developed"

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
    
    # Find closest matching country
    closest_country = find_closest_country(gdpp, income, child_mort)
    
    # Check if the closest_country is in the dataset
    if closest_country in clustered_dataset['country'].values:
        closest_country_row = clustered_dataset.loc[clustered_dataset['country'] == closest_country]
        
        # Check if the columns exist in the closest_country_row
        if 'cluster_id_km' in closest_country_row.columns and 'cluster_id_hc' in closest_country_row.columns:
            cluster_id_km = closest_country_row['cluster_id_km'].values[0]
            cluster_id_hc = closest_country_row['cluster_id_hc'].values[0]
            
            # Classify country based on clustering labels
            classification = classify_country_by_cluster(cluster_id_km, cluster_id_hc)
            
            st.subheader("Country Classification:")
            st.write(f"The provided values correspond to a {classification} country.")
            
            st.subheader("Closest Matching Country:")
            st.write(f"The closest matching country is: {closest_country}")
        else:
            st.write("Error: Required columns not found in the dataset.")
    else:
        st.write(f"Error: {closest_country} not found in the dataset.")
