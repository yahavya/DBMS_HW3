# MovieFinder - DBMS Assignment 3

A movie discovery web application database built with MySQL and Python, powered by TMDb API data.

## Project Structure

```
dbms_assignment3/
├── src/
│   ├── create_db_script.py      # Database schema creation
│   ├── api_data_retrieve.py     # Data fetching and population
│   ├── queries_db_script.py     # Query functions
│   └── queries_execution.py     # Query demonstrations
├── documentation/
│   ├── name_and_id.txt          # Team member information
│   ├── user_manual.pdf          # User manual with mockups
│   ├── system_docs.pdf          # System documentation
│   └── mysql_and_user_password.txt  # Database credentials
└── requirements.txt             # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials

Edit the following files and add your MySQL credentials:
- `src/create_db_script.py` (lines 12-14)
- `src/api_data_retrieve.py` (lines 16-20)
- `src/queries_execution.py` (lines 12-16)

Update the `user` and `password` fields with your assigned MySQL credentials for `mysqlsrv1.cs.tau.ac.il`.

### 3. Create Database Schema

```bash
python src/create_db_script.py
```

This will create:
- Database: `movie_db`
- 6 tables: movies, genres, movie_genres, people, movie_cast, movie_crew
- Indices for query optimization (including FULLTEXT indices)

### 4. Populate Database

**IMPORTANT:** This step takes 30-45 minutes due to API rate limiting.

```bash
python src/api_data_retrieve.py
```

This will fetch and insert:
- ~1000 movies
- ~20 genres
- ~2000+ actors/directors
- ~19,000+ total records across all tables

### 5. Run Query Demonstrations

```bash
python src/queries_execution.py
```

This demonstrates all 5 main queries with example parameters.

## Queries Implemented

### Query 1: Full-Text Search by Overview (FULLTEXT)
Search movies by plot keywords and themes.

### Query 2: Full-Text Search by Title (FULLTEXT)
Find movies by title keywords.

### Query 3: Genre Analysis with Aggregation (Complex)
Analyze genres by average rating, movie count, and revenue.

### Query 4: Actor Collaboration Finder (Complex)
Find actors who frequently work together.

### Query 5: Director's Best Films with Cast (Complex)
Explore a director's highest-rated films and their casts.

## Database Schema

### Tables
1. **movies** - Movie details (title, overview, ratings, revenue, etc.)
2. **genres** - Movie genres
3. **movie_genres** - Junction table for many-to-many relationship
4. **people** - Actors, directors, and crew members
5. **movie_cast** - Cast members for each movie
6. **movie_crew** - Crew members (directors, producers, writers)

### Key Indices
- FULLTEXT indices on `movies.overview` and `movies.title`
- Regular indices on frequently queried fields
- Composite index on `movie_crew(person_id, job)`

## Technologies Used

- **Database:** MySQL 5.7+ (on mysqlsrv1.cs.tau.ac.il)
- **Language:** Python 3.14
- **API:** The Movie Database (TMDb) API v3
- **Libraries:** mysql-connector-python, requests

## Notes

- The TMDb API key is embedded in `api_data_retrieve.py`
- All database operations are performed on the remote MySQL server
- The database is designed to 3NF (Third Normal Form)
- Proper foreign keys and constraints are implemented
- SQL injection protection through parameterized queries

## Authors

See `documentation/name_and_id.txt` for team member information.

## Documentation

- **User Manual:** `documentation/user_manual.pdf` - Application features and mockups
- **System Documentation:** `documentation/system_docs.pdf` - Schema design, query explanations, and technical details
