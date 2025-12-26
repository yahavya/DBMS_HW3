"""
Query Execution Examples for MovieFinder Application
Demonstrates usage of all 5 main queries with example parameters.
"""

import mysql.connector
from mysql.connector import Error
from queries_db_script import query_1, query_2, query_3, query_4, query_5, test_connection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration (should match other scripts)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3305)),
    'user': os.getenv('DB_USER', 'yarony'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'yarony')
}


def print_separator(title=""):
    """Print a formatted separator line."""
    if title:
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    else:
        print("-"*70)


def format_currency(amount):
    """Format number as currency string."""
    if amount is None or amount == 0:
        return "$0"
    return f"${amount:,.0f}"


def execute_query_1_examples(connection):
    """Execute and display results for Query 1 - Full-text search by overview."""

    print_separator("QUERY 1: Full-Text Search by Movie Overview (Keywords)")
    print("Purpose: Find movies by plot themes and keywords\n")

    test_cases = [
        "space exploration",
        "time travel",
        "artificial intelligence",
    ]

    for keywords in test_cases:
        print(f"\n🔍 Searching for movies about: '{keywords}'")
        print_separator()

        results = query_1(connection, keywords)

        if results:
            print(f"Found {len(results)} movies:\n")
            for i, (title, rating, year, snippet, relevance) in enumerate(results[:10], 1):
                print(f"{i}. {title} ({year})")
                print(f"   Rating: {rating}/10 | Relevance: {relevance:.2f}")
                print(f"   Overview: {snippet}...")
                print()
        else:
            print("No movies found for this search term.\n")


def execute_query_2_examples(connection):
    """Execute and display results for Query 2 - Full-text search by title."""

    print_separator("QUERY 2: Full-Text Search by Movie Title")
    print("Purpose: Find movies by title keywords\n")

    test_cases = [
        "Star",
        "Dark",
        "Spider",
    ]

    for search_term in test_cases:
        print(f"\n🔍 Searching for movie titles containing: '{search_term}'")
        print_separator()

        results = query_2(connection, search_term)

        if results:
            print(f"Found {len(results)} movies:\n")
            for i, (title, rating, year, popularity, relevance) in enumerate(results[:10], 1):
                year_str = year if year else "N/A"
                rating_str = f"{rating}/10" if rating else "N/A"
                print(f"{i}. {title} ({year_str}) - Rating: {rating_str}")
                print(f"   Popularity: {popularity:.1f} | Relevance: {relevance:.2f}")
        else:
            print("No movies found for this search term.")

        print()


def execute_query_3_examples(connection):
    """Execute and display results for Query 3 - Genre analysis with aggregation."""

    print_separator("QUERY 3: Top-Rated Genres with Revenue Analysis")
    print("Purpose: Analyze which genres produce highest-rated content\n")

    test_cases = [
        ("Genres with 20+ movies", 20),
        ("Genres with 50+ movies", 50),
        ("Genres with 10+ movies", 10),
    ]

    for description, min_movies in test_cases:
        print(f"\n📊 {description}:")
        print_separator()

        results = query_3(connection, min_movies)

        if results:
            print(f"Found {len(results)} genres:\n")
            print(f"{'Rank':<6}{'Genre':<20}{'Avg Rating':<12}{'Movies':<10}{'Total Revenue':<20}{'Avg Revenue'}")
            print("-"*90)

            for i, (genre, avg_rating, count, total_rev, avg_rev) in enumerate(results[:15], 1):
                total_rev_str = format_currency(total_rev)
                avg_rev_str = format_currency(avg_rev)
                print(f"{i:<6}{genre:<20}{avg_rating:<12}{count:<10}{total_rev_str:<20}{avg_rev_str}")
        else:
            print("No genres found matching criteria.")

        print()


def execute_query_4_examples(connection):
    """Execute and display results for Query 4 - Actor collaborations."""

    print_separator("QUERY 4: Actor Collaboration Finder")
    print("Purpose: Find which actors frequently work together\n")

    test_cases = [
        ("Tom Hanks", 2),
        ("Leonardo DiCaprio", 2),
        ("Samuel L. Jackson", 2),
    ]

    for actor_name, min_collab in test_cases:
        print(f"\n🎬 Finding actors who've worked with '{actor_name}' in {min_collab}+ movies:")
        print_separator()

        results = query_4(connection, actor_name, min_collab)

        if results:
            print(f"Found {len(results)} frequent collaborators:\n")

            for i, (collaborator, count, movies) in enumerate(results[:10], 1):
                print(f"{i}. {collaborator}")
                print(f"   Collaborations: {count} movies")

                # Show up to 3 movie titles
                movie_list = movies.split(', ') if movies else []
                if len(movie_list) > 3:
                    display_movies = ', '.join(movie_list[:3]) + f" (+{len(movie_list)-3} more)"
                else:
                    display_movies = movies

                print(f"   Movies: {display_movies}")
                print()
        else:
            print(f"No collaborators found for '{actor_name}' with {min_collab}+ movies together.")
            print("This could mean:")
            print("  - The actor name is not in the database")
            print("  - The actor hasn't worked with anyone multiple times")
            print("  - Try lowering min_collaborations or checking the exact name\n")


def execute_query_5_examples(connection):
    """Execute and display results for Query 5 - Director's best films."""

    print_separator("QUERY 5: Director's Highest-Rated Films with Cast")
    print("Purpose: Explore a director's best work and key actors\n")

    test_cases = [
        ("Christopher Nolan", 7.0),
        ("Steven Spielberg", 7.5),
        ("Quentin Tarantino", 7.0),
    ]

    for director, min_rating in test_cases:
        print(f"\n🎥 Best films by '{director}' (rating >= {min_rating}):")
        print_separator()

        results = query_5(connection, director, min_rating)

        if results:
            print(f"Found {len(results)} films:\n")

            for i, (title, rating, year, revenue, cast) in enumerate(results[:10], 1):
                year_str = year if year else "N/A"
                revenue_str = format_currency(revenue)
                cast_str = cast if cast else "Cast info not available"

                print(f"{i}. {title} ({year_str})")
                print(f"   Rating: {rating}/10 | Revenue: {revenue_str}")
                print(f"   Starring: {cast_str}")
                print()
        else:
            print(f"No films found for director '{director}' with rating >= {min_rating}")
            print("This could mean:")
            print("  - The director name is not in the database")
            print("  - None of their films meet the rating threshold")
            print("  - Try lowering min_rating or checking the exact name\n")


def main():
    """
    Main function to demonstrate all queries.
    """
    connection = None

    try:
        print("\n" + "="*70)
        print("  MOVIEFINDER - DATABASE QUERY DEMONSTRATIONS")
        print("="*70)

        # Connect to database
        print("\nConnecting to database...")
        connection = mysql.connector.connect(**DB_CONFIG)

        if not connection.is_connected():
            print("Failed to connect to database!")
            return 1

        # Test connection
        print()
        if not test_connection(connection):
            print("Database appears to be empty. Please run api_data_retrieve.py first.")
            return 1

        # Execute all query examples
        execute_query_1_examples(connection)
        execute_query_2_examples(connection)
        execute_query_3_examples(connection)
        execute_query_4_examples(connection)
        execute_query_5_examples(connection)

        print_separator("All Query Demonstrations Completed Successfully!")

    except Error as e:
        print(f"\nDatabase Error: {e}")
        return 1

    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        return 1

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")

    return 0


if __name__ == "__main__":
    print("\n" + "*"*70)
    print("*  MovieFinder Query Execution Script")
    print("*  This script demonstrates all 5 main database queries")
    print("*"*70)

    exit(main())
