# MovieFinder - User Manual

**Version:** 1.0
**Date:** January 2026
**Database Management Systems - Assignment 3**

---

## Table of Contents

1. [Application Overview](#application-overview)
2. [Application Features](#application-features)
3. [User Interface Mockups](#user-interface-mockups)
4. [How to Use Each Feature](#how-to-use-each-feature)

---

## Application Overview

### What is MovieFinder?

MovieFinder is a web application designed for **movie enthusiasts** who want to discover and explore films based on various criteria such as plot themes, actors, directors, genres, and ratings. The application provides powerful search and analysis tools to help users find their next favorite movie.

### Target Audience

- **Movie Fans**: People looking to discover new movies based on their interests
- **Film Students**: Users researching movies, directors, and actor collaborations
- **Casual Browsers**: Anyone exploring movies by genre, ratings, or popularity

### Key Capabilities

- Search movies by plot keywords and themes
- Find movies by title
- Analyze genre trends and ratings
- Discover actor collaborations
- Explore director filmographies

---

## Application Features

### Feature 1: Plot Keyword Search
**Query Used:** Full-Text Search on Movie Overview

Search for movies by entering keywords related to the plot or theme. For example:
- "space exploration"
- "time travel"
- "artificial intelligence"

The system searches through movie descriptions and ranks results by relevance and rating.

**Use Case:** Finding all sci-fi movies about space exploration

---

### Feature 2: Title Search
**Query Used:** Full-Text Search on Movie Title

Quickly find movies by searching for keywords in the title. The search supports partial matches and ranks by relevance.

**Use Case:** Finding all movies with "Star" in the title (Star Wars, Star Trek, etc.)

---

### Feature 3: Genre Analytics Dashboard
**Query Used:** Aggregation with GROUP BY and HAVING

View comprehensive statistics for each genre including:
- Average rating
- Number of movies
- Total and average revenue

Filter by minimum number of movies to focus on well-represented genres.

**Use Case:** Discovering which genres tend to have the highest-rated content

---

### Feature 4: Actor Collaboration Finder
**Query Used:** Nested Query with EXISTS

Discover which actors frequently work together. Enter an actor's name and find all their collaborators who have appeared in multiple movies with them.

**Use Case:** Finding all actors who have worked with Tom Hanks in 3 or more movies

---

### Feature 5: Director Filmography Explorer
**Query Used:** Complex JOIN with Nested Subquery

Explore a director's highest-rated films along with their top cast members. Filter by minimum rating to see only their best work.

**Use Case:** Viewing Christopher Nolan's films rated 8.0 or higher with their lead actors

---

## User Interface Mockups

### Page 1: Home Page

```
┌─────────────────────────────────────────────────────────────┐
│                        MOVIEFINDER                           │
│                   Discover Your Next Favorite Film           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Search Options:                                             │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔍  Search by Plot Keywords                        │   │
│  │      (e.g., "space exploration", "time travel")     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎬  Search by Movie Title                          │   │
│  │      (e.g., "Star", "Dark Knight")                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📊  Genre Analytics                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  👥  Actor Collaborations                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎥  Director Filmography                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Page 2: Plot Keyword Search Results

```
┌─────────────────────────────────────────────────────────────┐
│  MovieFinder > Search > "space exploration"                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Found 15 movies matching "space exploration"               │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Interstellar (2014)                    ⭐ 8.6   │   │
│  │     A team of explorers travel through a wormhole   │   │
│  │     in space in an attempt to ensure humanity's...  │   │
│  │     [View Details]                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2. The Martian (2015)                     ⭐ 7.7   │   │
│  │     An astronaut becomes stranded on Mars after     │   │
│  │     his team assume he is dead, and must rely on... │   │
│  │     [View Details]                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [More results...]                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Page 3: Genre Analytics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  MovieFinder > Analytics > Genres (20+ movies)              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Genre Performance Analysis                                 │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Genre        Avg Rating  Movies  Total Revenue     │   │
│  │  ────────────────────────────────────────────────   │   │
│  │  Animation      7.2       156     $45.2B           │   │
│  │  Drama          6.8       892     $32.1B           │   │
│  │  Adventure      6.7       234     $58.9B           │   │
│  │  Thriller       6.5       189     $28.7B           │   │
│  │  Comedy         6.3       312     $22.4B           │   │
│  │  ...                                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Filter: [Minimum Movies: 20 ▼]  [Apply]                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Page 4: Actor Collaboration Finder

```
┌─────────────────────────────────────────────────────────────┐
│  MovieFinder > Collaborations > "Tom Hanks"                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Actors who frequently worked with Tom Hanks:               │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Meg Ryan                          4 collaborations │   │
│  │  Movies: Sleepless in Seattle, You've Got Mail,     │   │
│  │          Joe Versus the Volcano, ...                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Gary Sinise                       3 collaborations │   │
│  │  Movies: Forrest Gump, Apollo 13, The Green Mile    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [Show more...]                                             │
│                                                              │
│  Minimum collaborations: [2 ▼]  [Search another actor]     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Page 5: Director Filmography

```
┌─────────────────────────────────────────────────────────────┐
│  MovieFinder > Directors > "Christopher Nolan"              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Christopher Nolan's Highest-Rated Films (Rating ≥ 8.0)    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  The Dark Knight (2008)              ⭐ 9.0         │   │
│  │  Revenue: $1.00B                                     │   │
│  │  Starring: Christian Bale, Heath Ledger,            │   │
│  │            Aaron Eckhart                             │   │
│  │  [View Details]                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Inception (2010)                    ⭐ 8.8         │   │
│  │  Revenue: $829M                                      │   │
│  │  Starring: Leonardo DiCaprio, Joseph Gordon-Levitt, │   │
│  │            Elliot Page                               │   │
│  │  [View Details]                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Minimum rating: [8.0 ▼]  [Search another director]        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## How to Use Each Feature

### Using Plot Keyword Search

1. From the home page, click **"Search by Plot Keywords"**
2. Enter keywords describing the plot or theme (e.g., "time travel", "heist")
3. Click **Search**
4. Browse results ranked by relevance and rating
5. Click **View Details** on any movie for more information

**Backend Query:** `query_1(connection, keywords)`

---

### Using Title Search

1. From the home page, click **"Search by Movie Title"**
2. Enter a word or phrase from the movie title
3. Click **Search**
4. Results show movies with matching titles, ranked by relevance
5. Click on any movie to view details

**Backend Query:** `query_2(connection, search_term)`

---

### Using Genre Analytics

1. From the home page, click **"Genre Analytics"**
2. Select minimum number of movies to filter genres (default: 20)
3. View the table showing:
   - Average rating per genre
   - Number of movies in each genre
   - Total revenue by genre
4. Sort by any column to analyze different aspects

**Backend Query:** `query_3(connection, min_movies)`

---

### Finding Actor Collaborations

1. From the home page, click **"Actor Collaborations"**
2. Enter an actor's name
3. Set minimum number of collaborations (default: 2)
4. Click **Search**
5. View list of actors who frequently worked together
6. See the movies they appeared in together

**Backend Query:** `query_4(connection, actor_name, min_collaborations)`

---

### Exploring Director Filmography

1. From the home page, click **"Director Filmography"**
2. Enter a director's name
3. Set minimum rating threshold (default: 7.0)
4. Click **Search**
5. View the director's highest-rated films
6. See top cast members for each film
7. View revenue information

**Backend Query:** `query_5(connection, director_name, min_rating)`

---

## Conclusion

MovieFinder provides a comprehensive and intuitive interface for movie discovery and analysis. Each feature is powered by efficient database queries that leverage full-text search, complex joins, and aggregations to deliver fast, relevant results.

For technical documentation and implementation details, please refer to the **System Documentation**.

---

**Note:** This is a documentation-only submission. The actual web interface is not implemented, but all backend queries are fully functional and tested.
