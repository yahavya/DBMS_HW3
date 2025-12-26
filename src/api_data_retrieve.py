"""
TMDb API Data Retrieval and Database Population Script
Fetches movie data from The Movie Database API and populates MySQL database.
"""

import requests
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TMDb API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Database configuration (should match create_db_script.py)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3305)),
    'user': os.getenv('DB_USER', 'yarony'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'yarony')
}

# Configuration for data fetching
NUM_PAGES_TO_FETCH = 25  # 25 pages × 20 movies = 500 movies (reduces to ~10K total records)
REQUEST_DELAY = 0.25  # Delay between API requests (4 requests/second to be safe)


def get_db_connection():
    """
    Establish connection to MySQL database.

    Returns:
        mysql.connector.connection: Database connection object
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def make_api_request(endpoint, params=None):
    """
    Make a request to TMDb API with error handling and rate limiting.

    Args:
        endpoint (str): API endpoint path
        params (dict): Query parameters

    Returns:
        dict: JSON response data or None if error
    """
    if params is None:
        params = {}

    params['api_key'] = TMDB_API_KEY
    url = f"{TMDB_BASE_URL}/{endpoint}"

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            time.sleep(REQUEST_DELAY)  # Rate limiting delay
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                return None

    return None


def fetch_genres():
    """
    Fetch all movie genres from TMDb API.

    Returns:
        list: List of genre dictionaries with 'id' and 'name'
    """
    print("Fetching genres...")
    data = make_api_request('genre/movie/list')

    if data and 'genres' in data:
        print(f"✓ Fetched {len(data['genres'])} genres")
        return data['genres']
    else:
        print("✗ Failed to fetch genres")
        return []


def fetch_discover_movies(page=1):
    """
    Fetch movies from discover endpoint (paginated).

    Args:
        page (int): Page number to fetch

    Returns:
        list: List of basic movie data
    """
    params = {
        'sort_by': 'popularity.desc',
        'page': page,
        'include_adult': 'false',
        'language': 'en-US'
    }

    data = make_api_request('discover/movie', params)

    if data and 'results' in data:
        return data['results']
    else:
        print(f"✗ Failed to fetch movies page {page}")
        return []


def fetch_movie_details(movie_id):
    """
    Fetch detailed movie information including credits.
    Uses append_to_response to get credits in same request.

    Args:
        movie_id (int): TMDb movie ID

    Returns:
        dict: Detailed movie data with credits, or None if error
    """
    params = {
        'append_to_response': 'credits'
    }

    data = make_api_request(f'movie/{movie_id}', params)
    return data


def insert_genres(connection, genres):
    """
    Insert genres into the database.

    Args:
        connection: MySQL connection object
        genres (list): List of genre dictionaries
    """
    cursor = connection.cursor()

    try:
        insert_query = """
        INSERT INTO genres (genre_id, genre_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE genre_name = VALUES(genre_name)
        """

        for genre in genres:
            cursor.execute(insert_query, (genre['id'], genre['name']))

        connection.commit()
        print(f"✓ Inserted {len(genres)} genres into database")

    except Error as e:
        print(f"Error inserting genres: {e}")
        connection.rollback()
    finally:
        cursor.close()


def parse_date(date_string):
    """
    Parse date string to Python date object.

    Args:
        date_string (str): Date in YYYY-MM-DD format

    Returns:
        datetime.date or None: Parsed date or None if invalid
    """
    if not date_string:
        return None

    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None


def insert_movie(connection, movie_data):
    """
    Insert a movie into the database.

    Args:
        connection: MySQL connection object
        movie_data (dict): Movie data from TMDb API

    Returns:
        bool: True if successful, False otherwise
    """
    cursor = connection.cursor()

    try:
        insert_query = """
        INSERT INTO movies (
            movie_id, title, overview, release_date, runtime,
            budget, revenue, vote_average, vote_count,
            popularity, original_language
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            overview = VALUES(overview),
            vote_average = VALUES(vote_average),
            vote_count = VALUES(vote_count),
            popularity = VALUES(popularity)
        """

        values = (
            movie_data.get('id'),
            movie_data.get('title', 'Unknown'),
            movie_data.get('overview'),
            parse_date(movie_data.get('release_date')),
            movie_data.get('runtime'),
            movie_data.get('budget', 0),
            movie_data.get('revenue', 0),
            movie_data.get('vote_average'),
            movie_data.get('vote_count', 0),
            movie_data.get('popularity', 0.0),
            movie_data.get('original_language')
        )

        cursor.execute(insert_query, values)
        connection.commit()
        return True

    except Error as e:
        print(f"Error inserting movie {movie_data.get('id')}: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


def insert_movie_genres(connection, movie_id, genres):
    """
    Insert movie-genre relationships.

    Args:
        connection: MySQL connection object
        movie_id (int): Movie ID
        genres (list): List of genre dictionaries
    """
    if not genres:
        return

    cursor = connection.cursor()

    try:
        insert_query = """
        INSERT INTO movie_genres (movie_id, genre_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE movie_id = movie_id
        """

        for genre in genres:
            cursor.execute(insert_query, (movie_id, genre['id']))

        connection.commit()

    except Error as e:
        print(f"Error inserting movie genres for movie {movie_id}: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_person(connection, person_data):
    """
    Insert a person (actor/director/crew) into the database.
    Uses INSERT IGNORE to avoid duplicates.

    Args:
        connection: MySQL connection object
        person_data (dict): Person data from TMDb API

    Returns:
        bool: True if successful, False otherwise
    """
    cursor = connection.cursor()

    try:
        insert_query = """
        INSERT INTO people (person_id, name, popularity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            popularity = VALUES(popularity)
        """

        values = (
            person_data.get('id'),
            person_data.get('name', 'Unknown'),
            person_data.get('popularity', 0.0)
        )

        cursor.execute(insert_query, values)
        connection.commit()
        return True

    except Error as e:
        print(f"Error inserting person {person_data.get('id')}: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


def insert_cast(connection, movie_id, cast_list):
    """
    Insert cast members for a movie.

    Args:
        connection: MySQL connection object
        movie_id (int): Movie ID
        cast_list (list): List of cast member dictionaries
    """
    if not cast_list:
        return

    cursor = connection.cursor()

    try:
        # First insert people
        for cast_member in cast_list:
            insert_person(connection, cast_member)

        # Then insert cast relationships
        insert_query = """
        INSERT INTO movie_cast (movie_id, person_id, character_name, cast_order)
        VALUES (%s, %s, %s, %s)
        """

        for cast_member in cast_list:
            values = (
                movie_id,
                cast_member.get('id'),
                cast_member.get('character'),
                cast_member.get('order', 999)
            )
            cursor.execute(insert_query, values)

        connection.commit()

    except Error as e:
        print(f"Error inserting cast for movie {movie_id}: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_crew(connection, movie_id, crew_list):
    """
    Insert crew members for a movie.
    Filters to keep only directors, producers, and writers to avoid too much data.

    Args:
        connection: MySQL connection object
        movie_id (int): Movie ID
        crew_list (list): List of crew member dictionaries
    """
    if not crew_list:
        return

    # Filter crew to important roles
    important_jobs = {'Director', 'Producer', 'Executive Producer', 'Writer', 'Screenplay', 'Story'}
    filtered_crew = [c for c in crew_list if c.get('job') in important_jobs]

    if not filtered_crew:
        return

    cursor = connection.cursor()

    try:
        # First insert people
        for crew_member in filtered_crew:
            insert_person(connection, crew_member)

        # Then insert crew relationships
        insert_query = """
        INSERT INTO movie_crew (movie_id, person_id, job, department)
        VALUES (%s, %s, %s, %s)
        """

        for crew_member in filtered_crew:
            values = (
                movie_id,
                crew_member.get('id'),
                crew_member.get('job'),
                crew_member.get('department')
            )
            cursor.execute(insert_query, values)

        connection.commit()

    except Error as e:
        print(f"Error inserting crew for movie {movie_id}: {e}")
        connection.rollback()
    finally:
        cursor.close()


def populate_database():
    """
    Main function to populate the database with movie data.
    """
    connection = None

    try:
        # Connect to database
        connection = get_db_connection()
        print("Connected to database successfully\n")

        # Step 1: Fetch and insert genres
        print("="*60)
        print("STEP 1: Fetching and inserting genres")
        print("="*60)
        genres = fetch_genres()
        if genres:
            insert_genres(connection, genres)
        print()

        # Step 2: Fetch and process movies
        print("="*60)
        print(f"STEP 2: Fetching and inserting {NUM_PAGES_TO_FETCH} pages of movies (~500 movies)")
        print("="*60)

        total_movies = 0
        successful_movies = 0

        for page in range(1, NUM_PAGES_TO_FETCH + 1):
            print(f"\nProcessing page {page}/{NUM_PAGES_TO_FETCH}...")

            # Fetch basic movie list from discover
            movies = fetch_discover_movies(page)

            if not movies:
                print(f"  No movies found on page {page}, skipping...")
                continue

            print(f"  Found {len(movies)} movies on this page")

            # For each movie, fetch detailed info and insert
            for i, movie_basic in enumerate(movies, 1):
                movie_id = movie_basic.get('id')
                total_movies += 1

                print(f"    [{i}/{len(movies)}] Fetching details for movie ID {movie_id}...", end=' ')

                # Fetch detailed info with credits
                movie_details = fetch_movie_details(movie_id)

                if not movie_details:
                    print("FAILED")
                    continue

                # Insert movie
                if insert_movie(connection, movie_details):
                    print(f"✓ '{movie_details.get('title', 'Unknown')}'")
                    successful_movies += 1

                    # Insert genres
                    if 'genres' in movie_details:
                        insert_movie_genres(connection, movie_id, movie_details['genres'])

                    # Insert cast and crew (if credits available)
                    if 'credits' in movie_details:
                        credits = movie_details['credits']

                        if 'cast' in credits:
                            # Limit to top 8 cast members per movie (reduced for smaller DB size)
                            insert_cast(connection, movie_id, credits['cast'][:8])

                        if 'crew' in credits:
                            insert_crew(connection, movie_id, credits['crew'])
                else:
                    print("FAILED")

            print(f"\nPage {page} completed: {successful_movies}/{total_movies} movies inserted successfully")

        # Final summary
        print("\n" + "="*60)
        print("DATABASE POPULATION SUMMARY")
        print("="*60)
        print(f"Total movies processed: {total_movies}")
        print(f"Successfully inserted: {successful_movies}")
        print(f"Failed: {total_movies - successful_movies}")

        # Show table counts
        cursor = connection.cursor()
        tables = ['movies', 'genres', 'movie_genres', 'people', 'movie_cast', 'movie_crew']

        print("\nFinal table record counts:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count:,} records")

        cursor.close()
        print("\n" + "="*60)
        print("Database population completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        print("Database population failed!")
        return 1

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")

    return 0


def main():
    """
    Entry point for the script.
    """
    print("Starting TMDb API data retrieval and database population...")
    print("This process will take approximately 30-45 minutes.")
    print("Please be patient and do not interrupt.\n")

    start_time = time.time()
    result = populate_database()
    elapsed_time = time.time() - start_time

    print(f"\nTotal execution time: {elapsed_time/60:.2f} minutes")
    return result


if __name__ == "__main__":
    exit(main())
