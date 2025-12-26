"""
Database Query Functions for MovieFinder Application
Implements 5 main queries: 2 full-text searches and 3 complex queries.
"""

import mysql.connector
from mysql.connector import Error


def query_1(connection, keywords):
    """
    Query 1: Full-Text Search for Movies by Overview Keywords (FULLTEXT)

    Find all movies whose overview/description contains specific keywords,
    ordered by relevance and rating.

    Args:
        connection: MySQL connection object
        keywords (str): Search keywords (e.g., "space exploration", "time travel")

    Returns:
        list: List of tuples (title, rating, year, overview_snippet)
    """
    cursor = connection.cursor()

    try:
        # Full-text search with MATCH AGAINST
        # Uses natural language mode for relevance ranking
        query = """
        SELECT
            m.title,
            m.vote_average AS rating,
            YEAR(m.release_date) AS year,
            LEFT(m.overview, 150) AS overview_snippet,
            MATCH(m.overview) AGAINST(%s) AS relevance_score
        FROM movies m
        WHERE MATCH(m.overview) AGAINST(%s IN NATURAL LANGUAGE MODE)
        ORDER BY relevance_score DESC, m.vote_average DESC
        LIMIT 20
        """

        cursor.execute(query, (keywords, keywords))
        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"Error executing query_1: {e}")
        return []

    finally:
        cursor.close()


def query_2(connection, search_term):
    """
    Query 2: Full-Text Search for Movies by Title (FULLTEXT)

    Search for movies with titles matching or similar to a search term,
    showing title, year, and rating.

    Args:
        connection: MySQL connection object
        search_term (str): Title search term (e.g., "star", "dark knight")

    Returns:
        list: List of tuples (title, rating, year, popularity)
    """
    cursor = connection.cursor()

    try:
        # Full-text search on title with relevance scoring
        query = """
        SELECT
            m.title,
            m.vote_average AS rating,
            YEAR(m.release_date) AS year,
            m.popularity,
            MATCH(m.title) AGAINST(%s) AS relevance_score
        FROM movies m
        WHERE MATCH(m.title) AGAINST(%s IN NATURAL LANGUAGE MODE)
        ORDER BY relevance_score DESC, m.popularity DESC
        LIMIT 20
        """

        cursor.execute(query, (search_term, search_term))
        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"Error executing query_2: {e}")
        return []

    finally:
        cursor.close()


def query_3(connection, min_movies=20):
    """
    Query 3: Top-Rated Movies by Genre with Revenue Analysis (Complex - GROUP BY, Aggregation)

    For each genre, find the average rating, total number of movies, and total revenue,
    but only for genres with at least min_movies movies, ordered by average rating descending.

    Args:
        connection: MySQL connection object
        min_movies (int): Minimum number of movies required for a genre (default: 20)

    Returns:
        list: List of tuples (genre_name, avg_rating, movie_count, total_revenue)
    """
    cursor = connection.cursor()

    try:
        # Complex query with joins, grouping, aggregation, and HAVING clause
        query = """
        SELECT
            g.genre_name,
            ROUND(AVG(m.vote_average), 2) AS avg_rating,
            COUNT(DISTINCT m.movie_id) AS movie_count,
            SUM(m.revenue) AS total_revenue,
            ROUND(AVG(m.revenue), 0) AS avg_revenue
        FROM genres g
        INNER JOIN movie_genres mg ON g.genre_id = mg.genre_id
        INNER JOIN movies m ON mg.movie_id = m.movie_id
        WHERE m.vote_average IS NOT NULL
        GROUP BY g.genre_id, g.genre_name
        HAVING COUNT(DISTINCT m.movie_id) >= %s
        ORDER BY avg_rating DESC, movie_count DESC
        """

        cursor.execute(query, (min_movies,))
        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"Error executing query_3: {e}")
        return []

    finally:
        cursor.close()


def query_4(connection, actor_name, min_collaborations=2):
    """
    Query 4: Actor Collaboration Finder (Complex - Nested Query, EXISTS)

    Find all actors who have appeared in at least X movies with a specific actor,
    showing their names and the count of collaborations.

    Args:
        connection: MySQL connection object
        actor_name (str): Name of the actor to find collaborators for
        min_collaborations (int): Minimum number of movies together (default: 2)

    Returns:
        list: List of tuples (collaborator_name, collaboration_count, movie_titles)
    """
    cursor = connection.cursor()

    try:
        # Complex query with nested subquery and EXISTS clause
        query = """
        SELECT
            p2.name AS collaborator_name,
            COUNT(DISTINCT mc2.movie_id) AS collaboration_count,
            GROUP_CONCAT(
                DISTINCT m.title
                ORDER BY m.vote_average DESC
                SEPARATOR ', '
            ) AS movie_titles
        FROM people p1
        INNER JOIN movie_cast mc1 ON p1.person_id = mc1.person_id
        INNER JOIN movie_cast mc2 ON mc1.movie_id = mc2.movie_id
        INNER JOIN people p2 ON mc2.person_id = p2.person_id
        INNER JOIN movies m ON mc1.movie_id = m.movie_id
        WHERE
            p1.name LIKE %s
            AND p2.person_id != p1.person_id
            AND EXISTS (
                SELECT 1
                FROM movie_cast mc3
                WHERE mc3.movie_id = mc1.movie_id
                  AND mc3.person_id = p2.person_id
            )
        GROUP BY p2.person_id, p2.name
        HAVING COUNT(DISTINCT mc2.movie_id) >= %s
        ORDER BY collaboration_count DESC, p2.name
        LIMIT 20
        """

        # Use LIKE for partial name matching
        search_pattern = f"%{actor_name}%"
        cursor.execute(query, (search_pattern, min_collaborations))
        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"Error executing query_4: {e}")
        return []

    finally:
        cursor.close()


def query_5(connection, director_name, min_rating=7.0):
    """
    Query 5: Director's Highest-Rated Films with Cast (Complex - Nested Query, Aggregation)

    Find all movies directed by a specific person where the movie rating is above a threshold,
    showing the movie title, rating, year, and top 3 cast members (by billing order).

    Args:
        connection: MySQL connection object
        director_name (str): Name of the director
        min_rating (float): Minimum movie rating (default: 7.0)

    Returns:
        list: List of tuples (title, rating, year, revenue, cast_names)
    """
    cursor = connection.cursor()

    try:
        # Complex query with multiple joins, nested query, and aggregation
        query = """
        SELECT DISTINCT
            m.title,
            m.vote_average AS rating,
            YEAR(m.release_date) AS year,
            m.revenue,
            (
                SELECT GROUP_CONCAT(p_cast.name ORDER BY mc.cast_order SEPARATOR ', ')
                FROM movie_cast mc
                INNER JOIN people p_cast ON mc.person_id = p_cast.person_id
                WHERE mc.movie_id = m.movie_id
                  AND mc.cast_order < 3
                ORDER BY mc.cast_order
            ) AS top_cast
        FROM movies m
        INNER JOIN movie_crew mcr ON m.movie_id = mcr.movie_id
        INNER JOIN people p_dir ON mcr.person_id = p_dir.person_id
        WHERE
            p_dir.name LIKE %s
            AND mcr.job = 'Director'
            AND m.vote_average >= %s
        ORDER BY m.vote_average DESC, m.popularity DESC
        LIMIT 20
        """

        # Use LIKE for partial name matching
        search_pattern = f"%{director_name}%"
        cursor.execute(query, (search_pattern, min_rating))
        results = cursor.fetchall()

        return results

    except Error as e:
        print(f"Error executing query_5: {e}")
        return []

    finally:
        cursor.close()


# Additional helper function for debugging and testing
def test_connection(connection):
    """
    Test database connection and display basic statistics.

    Args:
        connection: MySQL connection object

    Returns:
        bool: True if connection is valid and database has data
    """
    cursor = connection.cursor()

    try:
        # Test query
        cursor.execute("SELECT COUNT(*) FROM movies")
        movie_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM people")
        people_count = cursor.fetchone()[0]

        print(f"Database connection successful!")
        print(f"  - Movies: {movie_count:,}")
        print(f"  - People: {people_count:,}")

        return movie_count > 0

    except Error as e:
        print(f"Database connection test failed: {e}")
        return False

    finally:
        cursor.close()
