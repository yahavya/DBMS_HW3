"""
Quick test to verify TMDb API works (no database needed)
"""

import os
import requests
import time

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def test_api():
    """Test TMDb API connection and fetch sample data"""

    print("Testing TMDb API connection...")
    print("="*60)

    # Test 1: Fetch genres
    print("\n1. Fetching movie genres...")
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {'api_key': TMDB_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'genres' in data:
            print(f"✓ SUCCESS! Found {len(data['genres'])} genres:")
            for genre in data['genres'][:5]:
                print(f"   - {genre['name']} (ID: {genre['id']})")
            print(f"   ... and {len(data['genres'])-5} more")
        else:
            print("✗ FAILED: No genres in response")
            return False

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

    time.sleep(0.5)

    # Test 2: Fetch popular movies
    print("\n2. Fetching popular movies (page 1)...")
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'sort_by': 'popularity.desc',
        'page': 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'results' in data:
            print(f"✓ SUCCESS! Found {len(data['results'])} movies on page 1:")
            for i, movie in enumerate(data['results'][:5], 1):
                title = movie.get('title', 'Unknown')
                rating = movie.get('vote_average', 'N/A')
                print(f"   {i}. {title} - Rating: {rating}/10")
            print(f"   ... and {len(data['results'])-5} more")
            print(f"\nTotal pages available: {data.get('total_pages', 'Unknown')}")
            print(f"Total movies available: {data.get('total_results', 'Unknown')}")
        else:
            print("✗ FAILED: No results in response")
            return False

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

    time.sleep(0.5)

    # Test 3: Fetch movie details with credits
    print("\n3. Fetching detailed movie info with credits...")
    movie_id = data['results'][0]['id']  # Get first movie ID
    movie_title = data['results'][0]['title']

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': TMDB_API_KEY,
        'append_to_response': 'credits'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        movie_data = response.json()

        print(f"✓ SUCCESS! Fetched details for: {movie_title}")
        print(f"   Overview: {movie_data.get('overview', 'N/A')[:100]}...")
        print(f"   Runtime: {movie_data.get('runtime', 'N/A')} minutes")
        print(f"   Budget: ${movie_data.get('budget', 0):,}")
        print(f"   Revenue: ${movie_data.get('revenue', 0):,}")

        if 'credits' in movie_data:
            cast = movie_data['credits'].get('cast', [])
            crew = movie_data['credits'].get('crew', [])
            print(f"   Cast members: {len(cast)}")
            print(f"   Crew members: {len(crew)}")

            if cast:
                print(f"   Top 3 actors:")
                for actor in cast[:3]:
                    print(f"      - {actor['name']} as {actor.get('character', 'Unknown')}")
        else:
            print("   ⚠ Warning: No credits in response")

    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

    # Summary
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)
    print("\nYour TMDb API key is working correctly.")
    print("You can fetch:")
    print("  - Genres")
    print("  - Movie lists")
    print("  - Detailed movie info")
    print("  - Cast and crew data")
    print("\nOnce you have MySQL credentials, you'll be ready to populate the database!")

    return True


if __name__ == "__main__":
    print("\nTMDb API Connection Test")
    print("This test does NOT require MySQL credentials\n")

    if not TMDB_API_KEY:
        print("✗ ERROR: TMDB_API_KEY environment variable not set!")
        print("Please set it in your .env file or export it:")
        print("  export TMDB_API_KEY='your_api_key_here'")
        exit(1)

    success = test_api()

    if not success:
        print("\n⚠ API test failed! Check your internet connection.")
        exit(1)
    else:
        print("\n🎉 Everything is ready! Just waiting for MySQL credentials.")
        exit(0)
