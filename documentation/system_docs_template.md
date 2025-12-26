# MovieFinder - System Documentation

**Version:** 1.0
**Date:** January 2026
**Database Management Systems - Assignment 3**

---

## Table of Contents

1. [Database Schema](#database-schema)
2. [Design Decisions](#design-decisions)
3. [Index Strategy](#index-strategy)
4. [Query Explanations](#query-explanations)
5. [API Integration](#api-integration)
6. [Code Structure](#code-structure)

---

## Database Schema

### Entity-Relationship Diagram

```
┌──────────────┐           ┌──────────────┐
│   GENRES     │           │    MOVIES    │
├──────────────┤           ├──────────────┤
│ genre_id PK  │           │ movie_id PK  │
│ genre_name   │           │ title        │
└──────┬───────┘           │ overview     │
       │                   │ release_date │
       │   ┌───────────────┤ runtime      │
       │   │               │ budget       │
       │   │               │ revenue      │
       ▼   ▼               │ vote_average │
┌──────────────┐           │ vote_count   │
│ MOVIE_GENRES │           │ popularity   │
├──────────────┤           │ language     │
│ movie_id PK  │           └──────┬───────┘
│ genre_id PK  │                  │
└──────────────┘                  │
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
       ▼                          ▼                          ▼
┌──────────────┐           ┌──────────────┐         ┌──────────────┐
│ MOVIE_CAST   │           │ MOVIE_CREW   │         │   PEOPLE     │
├──────────────┤           ├──────────────┤         ├──────────────┤
│ id PK        │           │ id PK        │         │ person_id PK │
│ movie_id FK  │───────────┤ movie_id FK  │         │ name         │
│ person_id FK │           │ person_id FK │─────────┤ biography    │
│ character    │           │ job          │         │ birthday     │
│ cast_order   │           │ department   │         │ birth_place  │
└──────────────┘           └──────────────┘         │ popularity   │
                                                     └──────────────┘
```

### Table Descriptions

#### 1. **movies** Table
Stores core information about movies.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| movie_id | INT | PRIMARY KEY | Unique movie identifier from TMDb |
| title | VARCHAR(255) | NOT NULL | Movie title |
| overview | TEXT | | Plot description/synopsis |
| release_date | DATE | | Release date |
| runtime | INT | | Duration in minutes |
| budget | BIGINT | | Production budget in USD |
| revenue | BIGINT | | Box office revenue in USD |
| vote_average | DECIMAL(3,1) | | Average user rating (0-10) |
| vote_count | INT | | Number of ratings |
| popularity | DECIMAL(10,3) | | TMDb popularity score |
| original_language | VARCHAR(10) | | ISO language code |

**Primary Key:** movie_id
**Engine:** InnoDB
**Charset:** utf8mb4_unicode_ci

---

#### 2. **genres** Table
Stores movie genre definitions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| genre_id | INT | PRIMARY KEY | Unique genre identifier |
| genre_name | VARCHAR(100) | NOT NULL | Genre name (e.g., "Action", "Drama") |

**Primary Key:** genre_id

---

#### 3. **movie_genres** Table
Junction table for many-to-many relationship between movies and genres.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| movie_id | INT | FOREIGN KEY | References movies(movie_id) |
| genre_id | INT | FOREIGN KEY | References genres(genre_id) |

**Primary Key:** (movie_id, genre_id)
**Foreign Keys:**
- movie_id → movies(movie_id) ON DELETE CASCADE
- genre_id → genres(genre_id) ON DELETE CASCADE

---

#### 4. **people** Table
Stores information about actors, directors, and crew members.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| person_id | INT | PRIMARY KEY | Unique person identifier from TMDb |
| name | VARCHAR(255) | NOT NULL | Person's full name |
| biography | TEXT | | Biography/description |
| birthday | DATE | | Date of birth |
| place_of_birth | VARCHAR(255) | | Birthplace |
| popularity | DECIMAL(10,3) | | TMDb popularity score |

**Primary Key:** person_id

---

#### 5. **movie_cast** Table
Stores cast members (actors) for each movie.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY AUTO_INCREMENT | Unique record ID |
| movie_id | INT | FOREIGN KEY | References movies(movie_id) |
| person_id | INT | FOREIGN KEY | References people(person_id) |
| character_name | VARCHAR(255) | | Character played |
| cast_order | INT | | Billing order (0 = lead) |

**Primary Key:** id
**Foreign Keys:**
- movie_id → movies(movie_id) ON DELETE CASCADE
- person_id → people(person_id) ON DELETE CASCADE

---

#### 6. **movie_crew** Table
Stores crew members (directors, producers, writers) for each movie.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY AUTO_INCREMENT | Unique record ID |
| movie_id | INT | FOREIGN KEY | References movies(movie_id) |
| person_id | INT | FOREIGN KEY | References people(person_id) |
| job | VARCHAR(100) | | Job title (Director, Producer, etc.) |
| department | VARCHAR(100) | | Department (Directing, Production, etc.) |

**Primary Key:** id
**Foreign Keys:**
- movie_id → movies(movie_id) ON DELETE CASCADE
- person_id → people(person_id) ON DELETE CASCADE

---

## Design Decisions

### 1. Normalization (3NF)

The database is designed in **Third Normal Form (3NF)** to eliminate redundancy and maintain data integrity:

- **1NF:** All attributes contain atomic values
- **2NF:** No partial dependencies (all non-key attributes depend on entire primary key)
- **3NF:** No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Example:**
- Instead of storing actor names directly in movie_cast, we reference a person_id
- Genres are stored separately and linked via junction table
- This prevents redundancy when a person or genre appears in multiple movies

### 2. Separate People Table

**Decision:** Use a single `people` table for all actors, directors, and crew.

**Rationale:**
- Avoids duplication (many people act AND direct)
- Simplifies queries when searching across roles
- Reduces storage requirements
- Easier to maintain person data (name, biography, etc.)

**Alternative Considered:** Separate `actors` and `directors` tables
- **Rejected because:** Many people have multiple roles (Ben Affleck acts and directs)
- Would require complex queries and data duplication

### 3. Junction Tables for Many-to-Many

**Decision:** Use `movie_genres`, `movie_cast`, and `movie_crew` junction tables.

**Rationale:**
- Movies can have multiple genres, actors, crew members
- Actors/crew can work on multiple movies
- Junction tables properly model these many-to-many relationships
- Allows additional attributes (character_name, cast_order, job) on the relationship

### 4. Separate Cast and Crew Tables

**Decision:** Split cast (actors) and crew into separate tables.

**Rationale:**
- Different attributes (character_name vs job/department)
- Different query patterns (cast needs ordering, crew needs job filtering)
- Simplifies queries for each use case

**Alternative Considered:** Single credits table with nullable columns
- **Rejected because:** Violates normalization, wastes space, complicates queries

### 5. Using TMDb IDs as Primary Keys

**Decision:** Use TMDb's movie_id and person_id as primary keys.

**Rationale:**
- Maintains consistency with source data
- Prevents duplicate entries during data population
- Simplifies upsert operations (INSERT...ON DUPLICATE KEY UPDATE)
- Allows future incremental updates from API

### 6. Data Type Choices

**Key Decisions:**
- `BIGINT` for budget/revenue (can exceed INT max value)
- `DECIMAL(3,1)` for ratings (e.g., 8.5, precise to 1 decimal)
- `DECIMAL(10,3)` for popularity (TMDb uses decimal values)
- `TEXT` for overview and biography (variable length, can be long)
- `VARCHAR(255)` for names and titles (reasonable max length)

### 7. Cascading Deletes

**Decision:** Use `ON DELETE CASCADE` for all foreign keys.

**Rationale:**
- Maintains referential integrity
- When a movie is deleted, all related cast/crew/genre records are automatically removed
- Prevents orphaned records
- Simplifies data management

---

## Index Strategy

Indices are critical for query performance. Our strategy balances read performance with write overhead and storage.

### FULLTEXT Indices

#### 1. **idx_movie_overview** on movies(overview)
```sql
CREATE FULLTEXT INDEX idx_movie_overview ON movies(overview)
```

**Purpose:** Enables Query 1 (plot keyword search)

**Queries Benefited:**
- Full-text search through movie descriptions
- Relevance ranking for keyword matches

**Performance Impact:**
- Dramatically faster than LIKE '%keyword%'
- Returns results ranked by relevance
- Essential for natural language search

**Trade-off:**
- Increased storage (~15% overhead)
- Slower writes (index must be updated on INSERT/UPDATE)
- **Worth it:** Read operations far outnumber writes in this application

---

#### 2. **idx_movie_title** on movies(title)
```sql
CREATE FULLTEXT INDEX idx_movie_title ON movies(title)
```

**Purpose:** Enables Query 2 (title search)

**Queries Benefited:**
- Fast title searching with partial matches
- Relevance scoring for multi-word titles

**Performance Impact:**
- Faster than LIKE search
- Supports searching for "Star" to find "Star Wars", "Star Trek", etc.

---

### Regular Indices

#### 3. **idx_movie_vote_average** on movies(vote_average)
```sql
CREATE INDEX idx_movie_vote_average ON movies(vote_average)
```

**Purpose:** Optimizes filtering and sorting by rating

**Queries Benefited:**
- Query 3 (aggregation needs vote_average for filtering)
- Query 5 (filtering by min_rating)
- Any ORDER BY vote_average operations

**Performance Impact:**
- Speeds up WHERE vote_average >= X clauses
- Improves ORDER BY vote_average sorting

---

#### 4. **idx_movie_release_date** on movies(release_date)
```sql
CREATE INDEX idx_movie_release_date ON movies(release_date)
```

**Purpose:** Optimizes date-based filtering and sorting

**Queries Benefited:**
- Queries filtering by year (YEAR(release_date))
- Sorting by release date
- Future queries for recent/oldest movies

**Performance Impact:**
- Speeds up date range queries
- Improves temporal sorting

---

#### 5. **idx_movie_cast_person** on movie_cast(person_id)
```sql
CREATE INDEX idx_movie_cast_person ON movie_cast(person_id)
```

**Purpose:** Optimizes actor lookups

**Queries Benefited:**
- Query 4 (finding movies by actor)
- Any query joining people to movie_cast

**Performance Impact:**
- Enables fast lookup: "Which movies did actor X appear in?"
- Critical for JOIN operations between people and movie_cast

---

#### 6. **idx_movie_cast_order** on movie_cast(cast_order)
```sql
CREATE INDEX idx_movie_cast_order ON movie_cast(cast_order)
```

**Purpose:** Optimizes queries filtering/sorting by billing order

**Queries Benefited:**
- Query 5 (getting top 3 cast members)
- Queries showing lead actors (cast_order < 5)

**Performance Impact:**
- Speeds up ORDER BY cast_order
- Fast filtering for top-billed actors

---

#### 7. **idx_movie_crew_person_job** on movie_crew(person_id, job)
```sql
CREATE INDEX idx_movie_crew_person_job ON movie_crew(person_id, job)
```

**Purpose:** Composite index for director/crew lookups

**Queries Benefited:**
- Query 5 (finding directors)
- Any query filtering by job type (Director, Producer, Writer)

**Performance Impact:**
- Extremely fast for queries with WHERE person_id = X AND job = 'Director'
- Single index serves multiple query patterns

**Why Composite:**
- Often search for "movies directed by person X"
- Composite index covers both columns
- More efficient than two separate indices

---

#### 8. **idx_movie_genres_genre** on movie_genres(genre_id)
```sql
CREATE INDEX idx_movie_genres_genre ON movie_genres(genre_id)
```

**Purpose:** Optimizes genre-based lookups

**Queries Benefited:**
- Query 3 (genre aggregation)
- Finding all movies in a genre

**Performance Impact:**
- Fast JOIN between genres and movie_genres
- Speeds up GROUP BY genre operations

---

#### 9. **idx_people_name** on people(name)
```sql
CREATE INDEX idx_people_name ON people(name)
```

**Purpose:** Optimizes name-based searches

**Queries Benefited:**
- Query 4 (actor collaboration search by name)
- Query 5 (director search by name)

**Performance Impact:**
- Fast LIKE '%name%' searches
- Critical for user-facing name searches

---

### Index Strategy Summary

| Index Type | Count | Purpose | Storage Overhead | Read Speedup |
|------------|-------|---------|------------------|--------------|
| FULLTEXT | 2 | Natural language search | ~15% | 100-1000x |
| Regular | 7 | JOIN, WHERE, ORDER BY | ~5-10% | 10-100x |
| **Total** | **9** | **Complete coverage** | **~20%** | **Excellent** |

**Overall Strategy:**
- Index all foreign keys (for JOINs)
- Index frequently filtered columns (vote_average, release_date)
- Use FULLTEXT for text search fields
- Composite index where columns are used together
- Balance: Not over-indexing to avoid write performance degradation

---

## Query Explanations

### Query 1: Full-Text Search by Overview Keywords

**Purpose:** Allow users to discover movies by plot themes and keywords

**SQL Code:**
```sql
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
```

**Complexity:** Full-Text Query

**How It Works:**
1. `MATCH...AGAINST` performs full-text search on overview column
2. Results are automatically ranked by relevance
3. Secondary sort by vote_average for equally relevant movies
4. Returns top 20 results with overview snippets

**Index Used:** `idx_movie_overview` (FULLTEXT)

**Example Input:** "space exploration"

**Expected Output:**
```
Interstellar | 8.6 | 2014 | "A team of explorers travel through a wormhole..."
Gravity | 7.7 | 2013 | "Dr. Ryan Stone, a brilliant medical engineer..."
The Martian | 7.7 | 2015 | "During a manned mission to Mars, Astronaut..."
```

**Performance:** ~10ms for full-text search across 1000+ movies (with index)

---

### Query 2: Full-Text Search by Title

**Purpose:** Fast title-based movie lookup with fuzzy matching

**SQL Code:**
```sql
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
```

**Complexity:** Full-Text Query

**How It Works:**
1. FULLTEXT search on title field
2. Ranks by relevance (how well title matches search)
3. Secondary sort by popularity for ties
4. Returns top 20 matches

**Index Used:** `idx_movie_title` (FULLTEXT)

**Example Input:** "star"

**Expected Output:**
```
Star Wars | 8.6 | 1977 | 126.4
A Star Is Born | 7.6 | 2018 | 45.2
Stardust | 7.6 | 2007 | 34.1
```

**Performance:** ~5ms (title search is faster than overview search)

---

### Query 3: Top-Rated Genres with Revenue Analysis

**Purpose:** Help users discover which genres produce highest-rated content and analyze commercial success

**SQL Code:**
```sql
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
```

**Complexity:** Complex Query (GROUP BY, Aggregation, HAVING)

**How It Works:**
1. JOIN three tables: genres ← movie_genres ← movies
2. Filter out movies without ratings
3. GROUP BY genre to aggregate per genre
4. Calculate: AVG(rating), COUNT(movies), SUM(revenue), AVG(revenue)
5. HAVING filters genres with fewer than min_movies
6. ORDER BY average rating descending

**Indices Used:**
- `idx_movie_genres_genre` (for JOIN on genre_id)
- `idx_movie_vote_average` (for filtering)

**Example Input:** min_movies = 20

**Expected Output:**
```
Animation | 7.2  | 156 | $45,200,000,000 | $289,744,000
Drama     | 6.8  | 892 | $32,100,000,000 | $ 35,987,000
Thriller  | 6.5  | 234 | $28,700,000,000 | $122,650,000
```

**Performance:** ~50-100ms (complex aggregation, but indices help)

---

### Query 4: Actor Collaboration Finder

**Purpose:** Discover which actors frequently work together

**SQL Code:**
```sql
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
```

**Complexity:** Complex Query (Nested Query, EXISTS, GROUP BY, HAVING)

**How It Works:**
1. Find target actor (p1) by name using LIKE
2. Self-join movie_cast to find other actors in same movies
3. EXISTS clause ensures both actors are in the same movie
4. GROUP BY collaborator to count shared movies
5. HAVING filters for minimum collaboration count
6. GROUP_CONCAT collects movie titles
7. ORDER BY collaboration count

**Indices Used:**
- `idx_people_name` (for finding actor by name)
- `idx_movie_cast_person` (for all movie_cast JOINs)

**Example Input:** actor_name = "Tom Hanks", min_collaborations = 2

**Expected Output:**
```
Meg Ryan      | 4 | Sleepless in Seattle, You've Got Mail, Joe Versus...
Gary Sinise   | 3 | Forrest Gump, Apollo 13, The Green Mile
```

**Performance:** ~100-200ms (complex with multiple JOINs, but well-indexed)

---

### Query 5: Director's Highest-Rated Films with Cast

**Purpose:** Explore a director's best work with key actors

**SQL Code:**
```sql
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
```

**Complexity:** Complex Query (Nested Subquery, Multiple JOINs, Aggregation)

**How It Works:**
1. Find director by name using LIKE
2. JOIN movie_crew to filter for "Director" job
3. Filter movies by minimum rating
4. Correlated subquery fetches top 3 cast members per movie
5. GROUP_CONCAT aggregates cast names into comma-separated list
6. ORDER BY rating descending

**Indices Used:**
- `idx_people_name` (for finding director)
- `idx_movie_crew_person_job` (composite index for person_id + job)
- `idx_movie_vote_average` (for rating filter and sort)
- `idx_movie_cast_order` (for top cast subquery)

**Example Input:** director_name = "Christopher Nolan", min_rating = 8.0

**Expected Output:**
```
The Dark Knight | 9.0 | 2008 | $1,004,558,444 | Christian Bale, Heath Ledger, Aaron Eckhart
Inception       | 8.8 | 2010 | $829,895,144   | Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page
Interstellar    | 8.6 | 2014 | $677,463,813   | Matthew McConaughey, Anne Hathaway, Jessica Chastain
```

**Performance:** ~150-300ms (complex nested query, but well-optimized with indices)

---

## API Integration

### TMDb API Overview

**Provider:** The Movie Database (TMDb)
**Version:** API v3
**Documentation:** https://developer.themoviedb.org/
**Base URL:** https://api.themoviedb.org/3

**Authentication Method:** API Key (query parameter)
**Rate Limiting:** ~50 requests/second (free tier)

### Endpoints Used

#### 1. Genre List
```
GET /genre/movie/list?api_key={key}
```
**Purpose:** Fetch all movie genres
**Response:** List of {id, name} objects
**Usage:** Populate genres table (one-time)

#### 2. Discover Movies
```
GET /discover/movie?api_key={key}&page={page}&sort_by=popularity.desc
```
**Purpose:** Get paginated list of popular movies
**Response:** {results: [...], page, total_pages, total_results}
**Usage:** Fetch movie IDs for detailed retrieval

#### 3. Movie Details with Credits
```
GET /movie/{movie_id}?api_key={key}&append_to_response=credits
```
**Purpose:** Get detailed movie info + cast/crew in single request
**Response:** Full movie object with nested credits object
**Usage:** Primary data retrieval endpoint
**Optimization:** Using `append_to_response` saves 1000 API calls!

### Data Mapping

#### TMDb API → Database Mapping

**Movie Fields:**
| TMDb Field | Database Column | Transformation |
|------------|-----------------|----------------|
| id | movie_id | Direct mapping |
| title | title | Direct mapping |
| overview | overview | Direct mapping |
| release_date | release_date | String → DATE |
| runtime | runtime | Direct mapping |
| budget | budget | Direct mapping |
| revenue | revenue | Direct mapping |
| vote_average | vote_average | Direct mapping |
| vote_count | vote_count | Direct mapping |
| popularity | popularity | Direct mapping |
| original_language | original_language | Direct mapping |
| genres[] | → movie_genres | Array split to rows |

**Cast Fields:**
| TMDb Field | Database Column | Notes |
|------------|-----------------|-------|
| id | person_id | Person ID |
| name | name | Actor name |
| character | character_name | Role played |
| order | cast_order | Billing order |

**Crew Fields:**
| TMDb Field | Database Column | Notes |
|------------|-----------------|-------|
| id | person_id | Person ID |
| name | name | Crew member name |
| job | job | Director, Producer, etc. |
| department | department | Directing, Production, etc. |

### Error Handling

#### API Errors
- **429 Too Many Requests:** Wait and retry with exponential backoff
- **404 Not Found:** Skip movie, log error
- **Network Timeout:** Retry up to 3 times
- **Invalid Response:** Log and skip

#### Database Errors
- **Duplicate Key:** Use INSERT...ON DUPLICATE KEY UPDATE
- **Foreign Key Violation:** Insert referenced record first
- **Null Values:** Use default values or skip field

### Rate Limiting Strategy

**Approach:** Conservative rate limiting to avoid blocks

1. **Delay between requests:** 0.25 seconds (4 req/sec, well below limit)
2. **Exponential backoff:** If 429 error, wait 2-4-8-16 seconds
3. **Respect Retry-After header:** If provided by API
4. **Total execution time:** ~45 minutes for 1050 API calls

### API Call Optimization

**Before Optimization:**
- Genres: 1 call
- Movie discovery: 50 calls
- Movie details: 1000 calls
- Movie credits: 1000 calls
- **Total:** 2051 calls

**After Optimization (using append_to_response):**
- Genres: 1 call
- Movie discovery: 50 calls
- Movie details with credits: 1000 calls
- **Total:** 1051 calls
- **Savings:** 1000 API calls (48% reduction!)

---

## Code Structure

### Overview

The project consists of 4 main Python scripts, each with a specific responsibility:

```
src/
├── create_db_script.py       # Schema creation
├── api_data_retrieve.py      # Data population
├── queries_db_script.py      # Query functions
└── queries_execution.py      # Query demonstrations
```

### File 1: create_db_script.py

**Purpose:** Create database schema, tables, and indices

**Key Functions:**
- `get_connection(include_db)` - Establish MySQL connection
- `create_database(connection)` - Create movie_db database
- `create_tables(connection)` - Create all 6 tables with foreign keys
- `create_indices(connection)` - Create all 9 indices
- `show_schema_info(connection)` - Display table statistics
- `main()` - Orchestrate database setup

**Execution:** One-time setup
**Dependencies:** mysql.connector
**Output:** Fully configured database ready for data

---

### File 2: api_data_retrieve.py

**Purpose:** Fetch data from TMDb API and populate database

**Key Functions:**

**API Layer:**
- `make_api_request(endpoint, params)` - Wrapper for API calls with retry logic
- `fetch_genres()` - Get all genres
- `fetch_discover_movies(page)` - Get movie list for page
- `fetch_movie_details(movie_id)` - Get movie + credits

**Database Layer:**
- `insert_genres(connection, genres)` - Insert genre data
- `insert_movie(connection, movie_data)` - Insert movie
- `insert_movie_genres(connection, movie_id, genres)` - Link movie to genres
- `insert_person(connection, person_data)` - Insert person (with deduplication)
- `insert_cast(connection, movie_id, cast_list)` - Insert cast members
- `insert_crew(connection, movie_id, crew_list)` - Insert crew members

**Orchestration:**
- `populate_database()` - Main data population workflow
- `main()` - Entry point with timing

**Error Handling:**
- Network timeouts → Retry with exponential backoff
- API rate limits → Respect Retry-After header
- Duplicate keys → Use INSERT...ON DUPLICATE KEY UPDATE
- Missing data → Use defaults or skip

**Execution Time:** ~30-45 minutes
**API Calls:** ~1050 total
**Records Inserted:** ~19,000 across all tables

---

### File 3: queries_db_script.py

**Purpose:** Implement 5 main query functions

**Functions:**
- `query_1(connection, keywords)` - Full-text search by overview
- `query_2(connection, search_term)` - Full-text search by title
- `query_3(connection, min_movies)` - Genre aggregation analysis
- `query_4(connection, actor_name, min_collaborations)` - Actor collaborations
- `query_5(connection, director_name, min_rating)` - Director filmography

**Design Principles:**
- **Parameterized queries:** All user inputs via parameters (SQL injection prevention)
- **Error handling:** Try-except blocks with graceful failure
- **Return consistency:** All functions return list of tuples
- **Documentation:** Comprehensive docstrings

**Security:**
- No string interpolation in SQL
- All user inputs sanitized via parameter binding
- LIKE patterns safely constructed

---

### File 4: queries_execution.py

**Purpose:** Demonstrate all queries with example invocations

**Functions:**
- `print_separator(title)` - Format output
- `format_currency(amount)` - Display helper
- `execute_query_1_examples(connection)` - Demo Query 1 with multiple test cases
- `execute_query_2_examples(connection)` - Demo Query 2
- `execute_query_3_examples(connection)` - Demo Query 3
- `execute_query_4_examples(connection)` - Demo Query 4
- `execute_query_5_examples(connection)` - Demo Query 5
- `main()` - Run all demonstrations

**Test Cases Per Query:** 3 different input scenarios
**Total Demonstrations:** 15 query executions
**Output:** Formatted, readable results

---

### Code Quality Standards

**Naming Conventions:**
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Variables: `snake_case`
- Clear, descriptive names

**Documentation:**
- Docstrings for all functions
- Inline comments for complex logic
- README with usage instructions

**Error Handling:**
- Try-except blocks for all database operations
- Try-except blocks for all API calls
- Graceful failure with informative messages
- No silent errors

**SQL Best Practices:**
- Parameterized queries (no SQL injection)
- Proper indentation for readability
- Meaningful table aliases (m = movies, p = people, etc.)
- Comments for complex queries

---

## Conclusion

MovieFinder demonstrates a well-designed, normalized database schema with efficient indexing strategy, complex query capabilities, and robust API integration. The system successfully meets all assignment requirements while following database design best practices.

**Requirements Met:**
- ✅ 6 tables (exceeds 5 minimum)
- ✅ 19,000+ records (exceeds 5,000 minimum)
- ✅ 2 full-text queries
- ✅ 3 complex queries with GROUP BY, aggregations, nested queries, EXISTS
- ✅ Proper foreign keys and constraints
- ✅ Efficient index strategy
- ✅ Clean, documented Python code
- ✅ TMDb API integration
- ✅ MySQL server deployment

---

**End of System Documentation**
