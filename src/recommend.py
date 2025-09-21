# recommend.py

# Standard library imports
import logging
from pathlib import Path

# Third-party imports
import joblib
import pandas as pd
import streamlit as st

# --- Setup logging ---
# Kept from your original code
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

# --- Load Data Files Robustly ---
# This section is updated to use absolute paths for Streamlit deployment.
logging.info("🔁 Loading data files...")
try:
    # Get the absolute path to the directory containing this script
    current_dir = Path(__file__).parent

    # Define the full paths to your data files
    df_path = current_dir / 'df_cleaned.pkl'
    cosine_sim_path = current_dir / 'cosine_sim.pkl'

    # Load the data using the full paths
    df = joblib.load(df_path)
    cosine_sim = joblib.load(cosine_sim_path)
    logging.info("✅ Data loaded successfully.")

except Exception as e:
    # Log the error for debugging
    logging.error("❌ Failed to load required files: %s", str(e))
    # Display an error in the Streamlit app and stop execution
    st.error(f"Fatal Error: Could not load model files. Please check the logs. Error: {e}")
    st.stop()


def recommend_movies(movie_name, top_n=10):
    """
    Recommends a list of similar movies based on cosine similarity.

    Args:
        movie_name (str): The name of the movie to get recommendations for.
        top_n (int): The number of recommendations to return.

    Returns:
        pandas.DataFrame: A DataFrame containing the titles of recommended movies.
                          Returns an empty DataFrame if the movie is not found.
    """
    logging.info("🎬 Recommending movies for: '%s'", movie_name)

    # Find the index of the movie in the dataframe
    try:
        # Using .index[0] assumes a unique movie title match
        idx = df[df['title'].str.lower() == movie_name.lower()].index[0]
    except IndexError:
        logging.warning("⚠️ Movie '%s' not found in dataset.", movie_name)
        return pd.DataFrame() # Return an empty DataFrame if movie not found

    # Get similarity scores and sort them
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    # Get the indices of the top N similar movies
    movie_indices = [i[0] for i in sim_scores]

    logging.info("✅ Top %d recommendations ready.", top_n)

    # Return a DataFrame with the recommended movie titles
    return df[['title']].iloc[movie_indices]