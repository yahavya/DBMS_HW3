"""
Database Creation Script for MovieFinder Application
Creates the database schema, tables, and indices on MySQL server.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3305)),
    'user': os.getenv('DB_USER', 'yarony'),
    'password': os.getenv('DB_PASSWORD'),
}

DATABASE_NAME = 'yarony'


def get_connection(include_db=False):
    """
    Establish connection to MySQL server.

    Args:
        include_db (bool): Whether to connect to specific database

    Returns:
        mysql.connector.connection: Database connection object
    """
    try:
        config = DB_CONFIG.copy()
        if include_db:
            config['database'] = DATABASE_NAME

        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f"Successfully connected to MySQL server at {DB_CONFIG['host']}")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_database(connection):
    """
    Create the movie database if it doesn't exist.

    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()

        # Drop database if exists (for clean slate during development)
        # Comment out in production
        cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
        print(f"Dropped existing database '{DATABASE_NAME}' (if it existed)")

        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created successfully")

        cursor.execute(f"USE {DATABASE_NAME}")
        print(f"Using database '{DATABASE_NAME}'")

        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")
        raise


def create_tables(connection):
    """
    Create all tables for the movie database.

    Args:
        connection: MySQL connection object
    """
    cursor = connection.cursor()

    try:
        # Table 1: movies
        movies_table = """
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            overview TEXT,
            release_date DATE,
            runtime INT,
            budget BIGINT,
            revenue BIGINT,
            vote_average DECIMAL(3,1),
            vote_count INT,
            popularity DECIMAL(10,3),
            original_language VARCHAR(10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(movies_table)
        print("✓ Table 'movies' created successfully")

        # Table 2: genres
        genres_table = """
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INT PRIMARY KEY,
            genre_name VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(genres_table)
        print("✓ Table 'genres' created successfully")

        # Table 3: movie_genres (junction table)
        movie_genres_table = """
        CREATE TABLE IF NOT EXISTS movie_genres (
            movie_id INT,
            genre_id INT,
            PRIMARY KEY (movie_id, genre_id),
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(movie_genres_table)
        print("✓ Table 'movie_genres' created successfully")

        # Table 4: people (actors, directors, crew)
        # Only keeping fields we can reliably populate from movie credits
        people_table = """
        CREATE TABLE IF NOT EXISTS people (
            person_id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            popularity DECIMAL(10,3)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(people_table)
        print("✓ Table 'people' created successfully")

        # Table 5: movie_cast
        movie_cast_table = """
        CREATE TABLE IF NOT EXISTS movie_cast (
            id INT PRIMARY KEY AUTO_INCREMENT,
            movie_id INT,
            person_id INT,
            character_name VARCHAR(255),
            cast_order INT,
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY (person_id) REFERENCES people(person_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(movie_cast_table)
        print("✓ Table 'movie_cast' created successfully")

        # Table 6: movie_crew
        movie_crew_table = """
        CREATE TABLE IF NOT EXISTS movie_crew (
            id INT PRIMARY KEY AUTO_INCREMENT,
            movie_id INT,
            person_id INT,
            job VARCHAR(100),
            department VARCHAR(100),
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY (person_id) REFERENCES people(person_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(movie_crew_table)
        print("✓ Table 'movie_crew' created successfully")

        connection.commit()
        print("\nAll tables created successfully!")

    except Error as e:
        print(f"Error creating tables: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def create_indices(connection):
    """
    Create all indices for query optimization.

    Args:
        connection: MySQL connection object
    """
    cursor = connection.cursor()

    indices = [
        # FULLTEXT indices for text search queries
        ("CREATE FULLTEXT INDEX idx_movie_overview ON movies(overview)",
         "FULLTEXT index on movies.overview"),

        ("CREATE FULLTEXT INDEX idx_movie_title ON movies(title)",
         "FULLTEXT index on movies.title"),

        # Regular indices for filtering and joins
        ("CREATE INDEX idx_movie_vote_average ON movies(vote_average)",
         "Index on movies.vote_average"),

        ("CREATE INDEX idx_movie_release_date ON movies(release_date)",
         "Index on movies.release_date"),

        ("CREATE INDEX idx_movie_cast_person ON movie_cast(person_id)",
         "Index on movie_cast.person_id"),

        ("CREATE INDEX idx_movie_cast_order ON movie_cast(cast_order)",
         "Index on movie_cast.cast_order"),

        ("CREATE INDEX idx_movie_crew_person_job ON movie_crew(person_id, job)",
         "Composite index on movie_crew(person_id, job)"),

        ("CREATE INDEX idx_movie_genres_genre ON movie_genres(genre_id)",
         "Index on movie_genres.genre_id"),

        ("CREATE INDEX idx_people_name ON people(name)",
         "Index on people.name"),
    ]

    try:
        for sql, description in indices:
            try:
                cursor.execute(sql)
                print(f"✓ Created {description}")
            except Error as e:
                # Index might already exist, continue
                if "Duplicate key name" in str(e) or "already exists" in str(e):
                    print(f"⚠ {description} already exists, skipping")
                else:
                    print(f"✗ Error creating {description}: {e}")

        connection.commit()
        print("\nAll indices created successfully!")

    except Error as e:
        print(f"Error creating indices: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def show_schema_info(connection):
    """
    Display information about created tables and indices.

    Args:
        connection: MySQL connection object
    """
    cursor = connection.cursor()

    try:
        print("\n" + "="*60)
        print("DATABASE SCHEMA SUMMARY")
        print("="*60)

        # Show all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nTotal Tables: {len(tables)}")
        for table in tables:
            table_name = table[0]

            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")

        print("\n" + "="*60)

    except Error as e:
        print(f"Error displaying schema info: {e}")
    finally:
        cursor.close()


def main():
    """
    Main function to create database, tables, and indices.
    """
    connection = None

    try:
        print("Starting database setup for MovieFinder application...")
        print("="*60 + "\n")

        # Step 1: Connect to MySQL server
        connection = get_connection(include_db=False)

        # Step 2: Create database
        print("\nStep 1: Creating database...")
        create_database(connection)

        # Reconnect with database selected
        connection.close()
        connection = get_connection(include_db=True)

        # Step 3: Create tables
        print("\nStep 2: Creating tables...")
        create_tables(connection)

        # Step 4: Create indices
        print("\nStep 3: Creating indices...")
        create_indices(connection)

        # Step 5: Display schema info
        show_schema_info(connection)

        print("\n" + "="*60)
        print("Database setup completed successfully!")
        print("="*60)

    except Error as e:
        print(f"\nFATAL ERROR: {e}")
        print("Database setup failed!")
        return 1

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")

    return 0


if __name__ == "__main__":
    exit(main())
