# DBMS Assignment 3

A movie discovery database application built with MySQL and Python, powered by TMDb API data.

## Quick Start

### 1. Prerequisites
- Python 3.8+
- MySQL Server access (via SSH tunnel to `mysqlsrv1.cs.tau.ac.il`)
- TMDb API key ([Get one here](https://www.themoviedb.org/settings/api))

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root:

```env
# TMDb API Configuration
TMDB_API_KEY=your_tmdb_api_key_here

# MySQL Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3305
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

**Note:** If using SSH tunnel:
```bash
ssh -L 3305:mysqlsrv1.cs.tau.ac.il:3306 your_username@nova.cs.tau.ac.il
```

### 4. Setup Database

```bash
# Step 1: Create database schema (10 seconds)
python src/create_db_script.py

# Step 2: Populate database (30-45 minutes - be patient!)
python src/api_data_retrieve.py

# Step 3: Test queries
python src/queries_execution.py
```

## Project Structure

```
DBMS_HW3/
├── src/
│   ├── create_db_script.py      # Database schema creation
│   ├── api_data_retrieve.py     # Data fetching and population
│   ├── queries_db_script.py     # 5 query functions
│   └── queries_execution.py     # Query demonstrations
├── documentation/
│   ├── name_and_id.txt          # Team member information
│   ├── mysql_and_user_password.txt  # MySQL credentials
│   ├── user_manual.html         # User manual (convert to PDF)
│   ├── system_docs.html         # System docs (convert to PDF)
│   ├── user_manual_template.md  # User manual source
│   └── system_docs_template.md   # System docs source
└── requirements.txt             # Python dependencies
```

## Database Schema

**6 Tables:**
- `movies` - Movie details (title, overview, ratings, revenue, etc.)
- `genres` - Movie genres
- `movie_genres` - Junction table (many-to-many)
- `people` - Actors, directors, and crew members
- `movie_cast` - Cast members for each movie
- `movie_crew` - Crew members (directors, producers, writers)

## Queries Implemented

### Query 1: Full-Text Search by Overview (FULLTEXT)
Search movies by plot keywords and themes.
```python
query_1(connection, "space exploration")
```

### Query 2: Full-Text Search by Title (FULLTEXT)
Find movies by title keywords.
```python
query_2(connection, "Star")
```

### Query 3: Genre Analysis (Complex - GROUP BY, Aggregation)
Analyze genres by average rating, movie count, and revenue.
```python
query_3(connection, min_movies=20)
```

### Query 4: Actor Collaboration Finder (Complex - Self-Join, EXISTS)
Find actors who frequently work together.
```python
query_4(connection, "Tom Hanks", min_collaborations=2)
```

### Query 5: Director's Best Films (Complex - Nested Query)
Explore a director's highest-rated films and their casts.
```python
query_5(connection, "Christopher Nolan", min_rating=7.0)
```

## Documentation

- **User Manual:** `documentation/user_manual.html` (convert to PDF)
- **System Documentation:** `documentation/system_docs.html` (convert to PDF)
- **Team Info:** `documentation/name_and_id.txt`
- **MySQL Credentials:** `documentation/mysql_and_user_password.txt`

## Authors
- **Yaron Yahav**
- **Saar Molina** 

## License

This project is for educational purposes only.
