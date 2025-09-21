# omdb_utils.py

import requests

def get_movie_details(title, api_key):
    """
    Fetches the Plot, Poster, and IMDb Rating for a movie from the OMDB API.
    """
    url = f"http://www.omdbapi.com/?t={title}&plot=full&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Checks for HTTP errors
        res = response.json()

        if res.get("Response") == "True":
            # Fetch all three details. Use .get() for safety.
            plot = res.get("Plot", "N/A")
            poster = res.get("Poster", "N/A")
            rating = res.get("imdbRating", "N/A")
            return plot, poster, rating
            
    except requests.exceptions.RequestException as e:
        # This will catch connection errors, timeouts, etc.
        print(f"API request failed: {e}")

    # Return a 3-item tuple in all cases for consistency
    return "N/A", "N/A", "N/A"