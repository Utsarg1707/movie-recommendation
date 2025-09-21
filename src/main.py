# app.py

import streamlit as st
import json
from recommend import df, recommend_movies  # Assuming these are in your local files
from omdb_utils import get_movie_details    # Assuming these are in your local files

# --- CONFIGURATION ---
# Load configuration from a JSON file for better management of secrets.
# NEW CODE for src/main.py

# Access the secret directly from Streamlit's secrets manager
OMDB_API_KEY = st.secrets.get("OMDB_API_KEY")

# Check if the secret was loaded correctly
if not OMDB_API_KEY:
    st.error("🚨 OMDB_API_KEY not found. Please add it to your Streamlit secrets.")
    st.stop()

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Cinematch",
    page_icon="🍿",
    layout="wide",  # Use the full page width
    initial_sidebar_state="expanded"
)

# --- CACHING ---
# Cache the data loading and movie list generation to run only once.
@st.cache_data
def get_movie_list():
    """Returns a sorted list of unique movie titles."""
    return sorted(df['title'].dropna().unique())

# Cache the API calls. This is a HUGE performance improvement.
# The function will only run if the combination of movie_title and api_key is new.
@st.cache_data
def fetch_movie_details(movie_title, api_key):
    """Fetches movie details from OMDB API and caches the result."""
    return get_movie_details(movie_title, api_key)


# --- SIDEBAR ---
with st.sidebar:
    st.title("🍿 Cinematch Recommender")
    st.markdown("Find movies similar to your favorites!")

    movie_list = get_movie_list()
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown:",
        movie_list,
        index=None, # Set default to None for a placeholder
        placeholder="Select a movie...",
    )

    # Number of recommendations to show
    num_recommendations = st.slider(
        "Number of recommendations:",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    recommend_button = st.button("🚀 Find Similar Movies", use_container_width=True)


# --- MAIN PAGE ---
st.header(f"Recommendations for '{selected_movie}'" if selected_movie else "Discover Your Next Favorite Movie")

# --- RECOMMENDATION LOGIC ---
if recommend_button and selected_movie:
    with st.spinner("Casting the recommendation spell... ✨"):
        # Get a specified number of recommendations
        recommendations = recommend_movies(selected_movie, num_recommendations)

        if recommendations is None or recommendations.empty:
            st.warning(f"Sorry, we couldn't find any recommendations for **{selected_movie}**.")
        else:
            # Display recommendations in a grid
            st.success(f"Found {len(recommendations)} great matches for you!")

            # Define number of columns for the grid
            cols = st.columns(5) # Create 5 columns
            
            # Iterate over recommendations and display them in columns
            # +++ NEW CODE for app.py +++
        # Iterate over recommendations and display them in columns
        for idx, row in recommendations.iterrows():
            movie_title = row['title']
            
            # 1. Unpack all three values from the cached function
            plot, poster, rating = fetch_movie_details(movie_title, OMDB_API_KEY
                                                       )

            # Place each movie card in a column, cycling through the columns
            with cols[idx % 5]:
                with st.container(border=True):
                    if poster != "N/A":
                        st.image(poster, use_container_width=True)

                    # Display title and rating
                    st.markdown(f"**{movie_title}**")
                    if rating != "N/A":
                        st.caption(f"⭐ IMDb: {rating}") # 2. Display the rating!

                    # Expander for the plot
                    with st.expander("See Plot"):
                        st.write(plot if plot != "N/A" else "Plot details not found.")
else:
    st.info("Select a movie from the sidebar and click the button to get started!")