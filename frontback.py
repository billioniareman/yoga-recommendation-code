import streamlit as st
import requests
import pandas as pd

# Set your Modelbit API endpoint URL
MODEL_ENDPOINT = "https://ayushpatidar.us-east-1.modelbit.com/v1/YogaRecommendationSystem/latest"

# Load dataset with descriptions and other details
data = pd.read_csv("processed_yoga_data.csv")

# Create a dictionary to map pose names to their details
pose_details = data.set_index('Name of the Pose').to_dict(orient='index')

# Streamlit page configuration
st.title("Yoga Pose Recommendation System")
st.write("Enter the name of a yoga pose to get recommendations for similar poses.")

# User input
pose_name = st.text_input("Yoga Pose Name")

if st.button("Get Recommendations"):
    if pose_name:
        try:
            # Make a request to the Modelbit API
            response = requests.post(
                MODEL_ENDPOINT,
                data=f'{{"data": "{pose_name}"}}',
                headers={"Content-Type": "application/json"}
            )

            # Parse JSON response
            response_json = response.json()

            # Extract recommendations from the "data" key
            recommendations = response_json.get("data", [])

            # Display recommendations with details from the dataset
            if recommendations:
                st.write("**Recommended Poses:**")
                for rec in recommendations:
                    details = pose_details.get(rec, {})
                    st.write(f"**{rec}**")
                    st.write(f"**Description:** {details.get('Description', 'No description available.')}")
                    st.write(f"**Duration:** {details.get('Duration', 'No duration available.')}")
                    st.write(f"**Benefits:** {details.get('Benefits', 'No benefits available.')}")
                    st.write(f"**Contraindications:** {details.get('Contraindications', 'No contraindications available.')}")
                    st.write("---")
            else:
                st.write("No recommendations found.")
        except requests.RequestException as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("Please enter a yoga pose name.")
