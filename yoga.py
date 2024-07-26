import modelbit,os
import pandas as pd
import numpy as np


os.environ['MB_WORKSPACE_NAME'] = 'ayushpatidar'
os.environ['MB_API_KEY'] = 'miQlzXiwsJ:mswnafFJrOMZb7cROcOrK+NOnkQN0b2rN6SXvY82j1moQ='

mb = modelbit.login(region='us-east-1')
# Load the processed data
data = pd.read_csv('processed_yoga_data.csv')

# Load the cosine similarity matrix
cosine_sim = np.load('cosine_sim_matrix.npy')

# Function to get recommendations based on content
def get_content_recommendations(pose_name):
    indices = pd.Series(data.index, index=data['Name of the Pose']).drop_duplicates()
    idx = indices[pose_name]

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the poses based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 5 similar poses
    sim_indices = [i[0] for i in sim_scores[1:6]]

    # Return the top 5 similar poses
    return data['Name of the Pose'].iloc[sim_indices].tolist()

# Deploy the recommendation function to Modelbit
mb.deploy(get_content_recommendations, name="YogaRecommendationSystem")
