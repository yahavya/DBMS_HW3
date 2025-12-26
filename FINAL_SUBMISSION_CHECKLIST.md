# DBMS Assignment 3 - Final Submission Checklist

## ✅ COMPLETE - What You Have

### 1. src/ Directory
**Location:** `/Users/ron/dbms_assignment3/src/`

✅ **create_db_script.py** (176 lines)
- Creates database 'yarony' on mysqlsrv1.cs.tau.ac.il
- Creates 6 tables: movies, genres, movie_genres, people, movie_cast, movie_crew
- Creates 9 indices (2 FULLTEXT + 7 B-tree)
- All functions documented with docstrings

✅ **api_data_retrieve.py** (560 lines)
- Fetches data from TMDb API
- Populates 495 movies with cast, crew, and genre data
- Total: 15,696 records across 6 tables
- Includes error handling, rate limiting, retry logic

✅ **queries_db_script.py** (301 lines)
- query_1(): Full-text search on movie overview (**FULLTEXT**)
- query_2(): Full-text search on movie title (**FULLTEXT**)
- query_3(): Genre analytics with GROUP BY, HAVING, aggregation (**COMPLEX**)
- query_4(): Actor collaborations with nested query, EXISTS (**COMPLEX**)
- query_5(): Director films with joins, nested subquery (**COMPLEX**)

✅ **queries_execution.py** (268 lines)
- Example invocations for all 5 queries
- Test cases with multiple parameters
- Formatted output displays

### 2. documentation/ Directory
**Location:** `/Users/ron/dbms_assignment3/documentation/`

✅ **mysql_and_user_password.txt**
- Contains: yarony / saaryaron

⚠️ **name_and_id.txt** (EXISTS - needs your names/IDs filled in)
- Has placeholder structure
- **ACTION REQUIRED:** Replace [YOUR NAME] and [PARTNER'S NAME] with actual names and IDs

⚠️ **user_manual.pdf** (MISSING - needs conversion)
- Source available: `user_manual_template.md` (comprehensive markdown with ASCII mockups)
- **ACTION REQUIRED:** Convert to PDF

⚠️ **system_docs.pdf** (MISSING - needs conversion)
- Source available: `technical_database_report.html` (COMPLETE - just enhanced!)
- **Includes ALL requirements:**
  ✅ Database schema structure with ER diagram
  ✅ Design reasoning and alternative designs discussed
  ✅ Index strategy and which queries they optimize
  ✅ All 5 queries detailed with SQL, purpose, and sample results
  ✅ Code structure overview
  ✅ API usage and data mapping
- **ACTION REQUIRED:** Convert HTML to PDF

### 3. Root Directory

✅ **requirements.txt**
```
mysql-connector-python==8.2.0
requests==2.31.0
python-dotenv==1.0.0
```

---

## 📋 REQUIRED ACTIONS BEFORE SUBMISSION

### Action 1: Fill in Student Information
**File:** `/Users/ron/dbms_assignment3/documentation/name_and_id.txt`

Open the file and replace:
- `[YOUR NAME]` → Your actual name
- `[YOUR ID NUMBER]` → Your actual student ID
- `[PARTNER'S NAME]` → Partner's name (if applicable)
- `[PARTNER'S ID NUMBER]` → Partner's ID (if applicable)

### Action 2: Create system_docs.pdf
**Source:** `/Users/ron/dbms_assignment3/documentation/technical_database_report.html`

**Option A - Browser (Recommended):**
```bash
open /Users/ron/dbms_assignment3/documentation/technical_database_report.html
```
Then: File → Print → Save as PDF
Save as: `system_docs.pdf` in the documentation/ folder

**Option B - Command line (if you have wkhtmltopdf):**
```bash
cd /Users/ron/dbms_assignment3/documentation
wkhtmltopdf technical_database_report.html system_docs.pdf
```

### Action 3: Create user_manual.pdf
**Source:** `/Users/ron/dbms_assignment3/documentation/user_manual_template.md`

**Option A - Markdown to PDF converter:**
- Use online converter: https://www.markdowntopdf.com/
- Or use Pandoc: `pandoc user_manual_template.md -o user_manual.pdf`

**Option B - Create in PowerPoint/Google Slides (as assignment suggests):**
- Copy content from `user_manual_template.md`
- Create visual mockups/wireframes for the 5 features
- Export as PDF

### Action 4: Create Submission ZIP
Once you have all files, create the submission:

```bash
cd /Users/ron/dbms_assignment3
zip -r ID1-ID2.zip src/ documentation/ requirements.txt
```

Replace `ID1-ID2` with actual student IDs (e.g., `12345-67890.zip`)

---

## 📊 Submission Verification Checklist

Before submitting, verify you have:

### Inside ID1-ID2.zip:
```
ID1-ID2.zip/
├── src/
│   ├── create_db_script.py          ✅
│   ├── api_data_retrieve.py         ✅
│   ├── queries_db_script.py         ✅
│   └── queries_execution.py         ✅
├── documentation/
│   ├── name_and_id.txt              ⚠️ (fill in names/IDs)
│   ├── user_manual.pdf              ⚠️ (needs creation)
│   ├── system_docs.pdf              ⚠️ (needs conversion from HTML)
│   └── mysql_and_user_password.txt  ✅
└── requirements.txt                  ✅
```

### Database on MySQL Server:
- ✅ Database 'yarony' is populated with 15,696 records
- ✅ All 6 tables exist and are populated
- ✅ All 9 indices are created

### Requirements Met:
- ✅ Movie-related web application concept (MovieFinder)
- ✅ 6 tables (exceeds 5 minimum)
- ✅ 15,696 records (exceeds 5,000 minimum)
- ✅ 2 full-text queries (Query 1, Query 2)
- ✅ 3 complex queries (Query 3, 4, 5 with GROUP BY, nested queries, EXISTS, aggregations)
- ✅ Data from TMDb API
- ✅ Database on mysqlsrv1.cs.tau.ac.il
- ✅ Python 3.x compatible (should work on 3.14)
- ✅ All code is documented and readable
- ✅ Foreign keys implemented
- ✅ Indices optimize queries

---

## 🎯 Summary

**Status:** ~95% Complete

**Remaining Work:**
1. Fill in student names and IDs in `name_and_id.txt` (2 minutes)
2. Convert `technical_database_report.html` to `system_docs.pdf` (5 minutes)
3. Create `user_manual.pdf` from template (10-30 minutes depending on method)
4. Create final ZIP file (1 minute)

**Estimated Time to Complete:** 20-40 minutes

All the hard work is done! The database is populated, all queries work, and comprehensive documentation exists. You just need to finalize the PDF documents and create the ZIP file.
