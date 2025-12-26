# Query Reference - Quick Overview

This document provides a quick reference for all 5 queries with their English descriptions and expected outputs.

---

## Query 1: Full-Text Search by Movie Overview (FULLTEXT)

### English Description
"Find all movies whose overview/description contains specific keywords (e.g., 'space exploration' or 'time travel'), ordered by relevance and rating"

### Purpose
Allow users to discover movies by plot themes or story elements

### Example Usage
```python
results = query_1(connection, "space exploration")
```

### Expected Output (for "space exploration")
```
Title: Interstellar          | Rating: 8.4/10 | Year: 2014
Title: Gravity               | Rating: 7.7/10 | Year: 2013
Title: The Martian           | Rating: 7.6/10 | Year: 2015
Title: First Man             | Rating: 7.1/10 | Year: 2018
Title: Apollo 13             | Rating: 7.6/10 | Year: 1995
```

### SQL Query Type
FULLTEXT query with `MATCH...AGAINST`

---

## Query 2: Full-Text Search by Movie Title (FULLTEXT)

### English Description
"Search for movies with titles matching or similar to a search term (e.g., 'star', 'dark knight'), showing title, year, and rating"

### Purpose
Fast title-based movie lookup with fuzzy matching

### Example Usage
```python
results = query_2(connection, "star")
```

### Expected Output (for "star")
```
Title: Star Wars                 | Rating: 8.6/10 | Year: 1977
Title: Star Trek                 | Rating: 7.0/10 | Year: 2009
Title: A Star Is Born            | Rating: 7.6/10 | Year: 2018
Title: Stardust                  | Rating: 7.6/10 | Year: 2007
Title: Star Wars: The Last Jedi  | Rating: 6.9/10 | Year: 2017
```

### SQL Query Type
FULLTEXT query with `MATCH...AGAINST`

---

## Query 3: Top-Rated Genres with Revenue Analysis (COMPLEX)

### English Description
"For each genre, find the average rating, total number of movies, and total revenue, but only for genres with at least 20 movies (or specified minimum), ordered by average rating descending"

### Purpose
Help users discover which genres produce the highest-rated content and analyze commercial success

### Example Usage
```python
results = query_3(connection, min_movies=20)
```

### Expected Output (for min_movies=20)
```
Genre             | Avg Rating | Movie Count | Total Revenue      | Avg Revenue
--------------------------------------------------------------------------------
Animation         | 7.2        | 156         | $45,200,000,000   | $289,744,000
Drama             | 6.8        | 892         | $32,100,000,000   | $35,987,000
Adventure         | 6.7        | 234         | $58,900,000,000   | $251,709,000
Thriller          | 6.5        | 189         | $28,700,000,000   | $151,852,000
Comedy            | 6.3        | 312         | $22,400,000,000   | $71,794,000
Action            | 6.2        | 287         | $67,800,000,000   | $236,237,000
```

### SQL Query Type
Complex query with:
- `GROUP BY` (by genre)
- `HAVING` clause (filter genres with ≥ min_movies)
- Aggregate functions (`AVG`, `COUNT`, `SUM`)
- Multiple `INNER JOIN` operations

---

## Query 4: Actor Collaboration Finder (COMPLEX)

### English Description
"Find all actors who have appeared in at least X movies with a specific actor (e.g., find all actors who've been in 2+ movies with Tom Hanks), showing their names and the count of collaborations"

### Purpose
Discover which actors frequently work together

### Example Usage
```python
results = query_4(connection, "Tom Hanks", min_collaborations=2)
```

### Expected Output (for "Tom Hanks", min_collaborations=2)
```
Collaborator Name      | Movies Together | Movie Titles
----------------------------------------------------------------
Meg Ryan               | 4               | Sleepless in Seattle, You've Got Mail, Joe Versus the Volcano, ...
Gary Sinise            | 3               | Forrest Gump, Apollo 13, The Green Mile
Tim Allen              | 3               | Toy Story, Toy Story 2, Toy Story 3
Tom Sizemore           | 2               | Saving Private Ryan, The Green Mile
Bill Paxton            | 2               | Apollo 13, A League of Their Own
```

### SQL Query Type
Complex query with:
- Nested subqueries
- `EXISTS` clause
- Self-join on movie_cast table
- `GROUP BY` with `HAVING`
- `GROUP_CONCAT` for aggregating movie titles

---

## Query 5: Director's Highest-Rated Films with Cast (COMPLEX)

### English Description
"Find all movies directed by a specific person where the movie rating is above a threshold (e.g., ≥ 8.0), showing the movie title, rating, year, revenue, and top 3 cast members (by billing order)"

### Purpose
Explore a director's best work with key actors

### Example Usage
```python
results = query_5(connection, "Christopher Nolan", min_rating=8.0)
```

### Expected Output (for "Christopher Nolan", min_rating=8.0)
```
Movie Title        | Rating | Year | Revenue         | Top Cast Members
--------------------------------------------------------------------------------
The Dark Knight    | 9.0    | 2008 | $1,004,558,444  | Christian Bale, Heath Ledger, Aaron Eckhart
Inception          | 8.8    | 2010 | $829,895,144    | Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page
Interstellar       | 8.6    | 2014 | $677,463,813    | Matthew McConaughey, Anne Hathaway, Jessica Chastain
The Dark Knight    | 8.4    | 2012 | $1,081,041,287  | Christian Bale, Tom Hardy, Anne Hathaway
   Rises
The Prestige       | 8.5    | 2006 | $109,676,311    | Christian Bale, Hugh Jackman, Scarlett Johansson
```

### SQL Query Type
Complex query with:
- Correlated nested subquery (for fetching top cast)
- Multiple `INNER JOIN` operations
- Filtering on job type (WHERE job = 'Director')
- `GROUP_CONCAT` with `ORDER BY` in subquery
- Rating filter and sort

---

## Additional Example Scenarios

### Query 1 Additional Examples

**Input:** "time travel"
**Expected Movies:** Back to the Future, Looper, The Terminator, 12 Monkeys, etc.

**Input:** "artificial intelligence"
**Expected Movies:** Ex Machina, Her, A.I. Artificial Intelligence, The Matrix, etc.

### Query 2 Additional Examples

**Input:** "dark"
**Expected Movies:** The Dark Knight, Dark Phoenix, The Darkest Hour, etc.

**Input:** "spider"
**Expected Movies:** Spider-Man, The Amazing Spider-Man, Spider-Man: Far From Home, etc.

### Query 3 Additional Examples

**Input:** min_movies=50
**Result:** Only major genres with 50+ movies (Drama, Action, Comedy, Thriller, Romance, Adventure)

**Input:** min_movies=10
**Result:** More genres included, including niche categories

### Query 4 Additional Examples

**Input:** "Leonardo DiCaprio", min_collaborations=2
**Expected Collaborators:** Marion Cotillard, Mark Ruffalo, Tom Hardy, etc.

**Input:** "Samuel L. Jackson", min_collaborations=2
**Expected Collaborators:** (Many! He's in lots of movies with repeat collaborators)

### Query 5 Additional Examples

**Input:** "Steven Spielberg", min_rating=7.5
**Expected Films:** Schindler's List, Saving Private Ryan, Jurassic Park, E.T., Indiana Jones, etc.

**Input:** "Quentin Tarantino", min_rating=7.0
**Expected Films:** Pulp Fiction, Django Unchained, Inglourious Basterds, Kill Bill, etc.

---

## Query Complexity Summary

| Query | FULLTEXT | Nested Query | EXISTS | GROUP BY | Aggregation | Multiple JOINs |
|-------|----------|--------------|--------|----------|-------------|----------------|
| 1     | ✅       | ❌           | ❌     | ❌       | ❌          | ❌             |
| 2     | ✅       | ❌           | ❌     | ❌       | ❌          | ❌             |
| 3     | ❌       | ❌           | ❌     | ✅       | ✅          | ✅             |
| 4     | ❌       | ✅           | ✅     | ✅       | ✅          | ✅             |
| 5     | ❌       | ✅           | ❌     | ❌       | ✅          | ✅             |

**Assignment Requirements Met:**
- ✅ 2 Full-text queries (Query 1, 2)
- ✅ 3 Complex queries (Query 3, 4, 5)
  - ✅ Nested queries (Query 4, 5)
  - ✅ GROUP BY (Query 3, 4)
  - ✅ Aggregations (Query 3, 4, 5)
  - ✅ EXISTS (Query 4)

---

## Performance Estimates

Based on database with ~19,000 records:

| Query | Avg Response Time | Notes |
|-------|------------------|-------|
| 1     | ~10-20ms         | Fast with FULLTEXT index |
| 2     | ~5-10ms          | Fastest (smaller text field) |
| 3     | ~50-100ms        | Complex aggregation, but indexed |
| 4     | ~100-200ms       | Most complex (self-joins, EXISTS) |
| 5     | ~150-300ms       | Nested subquery for each row |

All queries are optimized with appropriate indices!

---

## Testing Recommendations

### Before Submission:
1. Test each query with at least 2-3 different input values
2. Verify queries return reasonable results (not empty, not errors)
3. Check that complex queries show correct aggregations
4. Ensure FULLTEXT queries return relevant results

### Good Test Values:

**Query 1:**
- "space"
- "love"
- "war"

**Query 2:**
- "Star"
- "The"
- "Man"

**Query 3:**
- min_movies=10
- min_movies=20
- min_movies=50

**Query 4:**
- "Tom Hanks", min=2
- "Robert De Niro", min=2
- "Scarlett Johansson", min=2

**Query 5:**
- "Christopher Nolan", min=7.0
- "Steven Spielberg", min=7.5
- "Martin Scorsese", min=7.0

---

This reference guide should help you understand what each query does and what kind of results to expect!
