# DBMS Assignment 3 - Submission Checklist

Use this checklist to ensure everything is ready before submitting.

---

## ☑️ Pre-Submission Tasks

### 1. Configure Database Credentials

- [ ] Edit `src/create_db_script.py` (lines 12-14)
  - [ ] Add MySQL username
  - [ ] Add MySQL password

- [ ] Edit `src/api_data_retrieve.py` (lines 16-20)
  - [ ] Add MySQL username
  - [ ] Add MySQL password

- [ ] Edit `src/queries_execution.py` (lines 12-16)
  - [ ] Add MySQL username
  - [ ] Add MySQL password

### 2. Run All Scripts (In Order)

- [ ] Install dependencies: `pip install -r requirements.txt`

- [ ] Create database: `python src/create_db_script.py`
  - [ ] Verify: Script completes without errors
  - [ ] Verify: Shows "All tables created successfully"
  - [ ] Verify: Shows "All indices created successfully"

- [ ] Populate database: `python src/api_data_retrieve.py`
  - [ ] Warning: This takes 30-45 minutes!
  - [ ] Verify: Script completes successfully
  - [ ] Verify: Shows final table counts (~19,000 total records)
  - [ ] Verify: Movies table has ~1000 records

- [ ] Test queries: `python src/queries_execution.py`
  - [ ] Verify: All queries execute without errors
  - [ ] Verify: Results look reasonable (not empty)
  - [ ] Verify: Query 1 returns relevant movies for search terms
  - [ ] Verify: Query 2 returns movies with matching titles
  - [ ] Verify: Query 3 shows genre statistics
  - [ ] Verify: Query 4 shows actor collaborations
  - [ ] Verify: Query 5 shows director's films

### 3. Fill in Documentation Files

- [ ] Edit `documentation/name_and_id.txt`
  - [ ] Add Student 1 name and ID
  - [ ] Add Student 2 name and ID

- [ ] Edit `documentation/mysql_and_user_password.txt`
  - [ ] Add MySQL username
  - [ ] Add MySQL password

### 4. Create PDF Documentation

- [ ] Convert `documentation/user_manual_template.md` to PDF
  - [ ] File is named exactly: `user_manual.pdf`
  - [ ] File is in `documentation/` folder
  - [ ] PDF includes all sections (overview, features, mockups, usage)
  - [ ] PDF is 10-15 pages
  - [ ] Tables and diagrams are readable

- [ ] Convert `documentation/system_docs_template.md` to PDF
  - [ ] File is named exactly: `system_docs.pdf`
  - [ ] File is in `documentation/` folder
  - [ ] PDF includes all sections (schema, design, indices, queries, API, code)
  - [ ] PDF is 20-25 pages
  - [ ] SQL code is properly formatted
  - [ ] ER diagram is visible

**Conversion methods:** See `CONVERT_TO_PDF_GUIDE.md`

---

## ☑️ File Structure Verification

Verify your project has this exact structure:

```
dbms_assignment3/
├── src/
│   ├── create_db_script.py          ✓ Required
│   ├── api_data_retrieve.py         ✓ Required
│   ├── queries_db_script.py         ✓ Required
│   └── queries_execution.py         ✓ Required
├── documentation/
│   ├── name_and_id.txt              ✓ Required (filled in)
│   ├── user_manual.pdf              ✓ Required (created from .md)
│   ├── system_docs.pdf              ✓ Required (created from .md)
│   └── mysql_and_user_password.txt  ✓ Required (filled in)
└── requirements.txt                 ✓ Required
```

**Check each file exists:**

- [ ] `src/create_db_script.py` exists
- [ ] `src/api_data_retrieve.py` exists
- [ ] `src/queries_db_script.py` exists
- [ ] `src/queries_execution.py` exists
- [ ] `documentation/name_and_id.txt` exists AND is filled in
- [ ] `documentation/user_manual.pdf` exists (NOT .md)
- [ ] `documentation/system_docs.pdf` exists (NOT .md)
- [ ] `documentation/mysql_and_user_password.txt` exists AND is filled in
- [ ] `requirements.txt` exists

---

## ☑️ Code Quality Checks

### Python Scripts

- [ ] All scripts run without syntax errors
- [ ] No hardcoded credentials left as empty strings
- [ ] All imports are in requirements.txt
- [ ] Code has comments and docstrings
- [ ] Functions have meaningful names

### Database

- [ ] Database exists on MySQL server
- [ ] Database is populated with data
- [ ] All 6 tables exist
- [ ] All tables have records
- [ ] All indices are created

### Queries

- [ ] All 5 queries execute successfully
- [ ] Query 1 uses FULLTEXT search
- [ ] Query 2 uses FULLTEXT search
- [ ] Query 3 uses GROUP BY and aggregation
- [ ] Query 4 uses nested query and EXISTS
- [ ] Query 5 uses nested subquery
- [ ] All queries use parameterized inputs (no SQL injection risk)

---

## ☑️ Assignment Requirements

### Database Requirements

- [ ] At least 5 tables (we have 6 ✓)
- [ ] At least 5,000 records (we have ~19,000 ✓)
- [ ] Foreign keys implemented (all junction tables have FK ✓)
- [ ] Meaningful names (all tables/columns named clearly ✓)
- [ ] Indices for optimization (9 indices ✓)

### Query Requirements

- [ ] 2 full-text queries (Query 1 & 2 ✓)
- [ ] 3 complex queries (Query 3, 4, 5 ✓)
  - [ ] At least one uses nested queries (Query 4, 5 ✓)
  - [ ] At least one uses GROUP BY (Query 3, 4 ✓)
  - [ ] At least one uses aggregations (Query 3, 4, 5 ✓)
  - [ ] At least one uses EXISTS (Query 4 ✓)

### Code Requirements

- [ ] Python creates database (create_db_script.py ✓)
- [ ] Python populates database (api_data_retrieve.py ✓)
- [ ] Query functions named query_NUM (query_1 through query_5 ✓)
- [ ] Functions take user inputs as parameters ✓
- [ ] Code is readable and documented ✓
- [ ] No SQL queries auto-generated by library ✓

### Data Source

- [ ] Using TMDb API (free, reliable ✓)
- [ ] API calls are in Python code ✓
- [ ] Data insertion via Python (not manual ✓)

### MySQL Server

- [ ] Using mysqlsrv1.cs.tau.ac.il ✓
- [ ] Have valid credentials ✓
- [ ] Database is on remote server ✓

### Documentation

- [ ] User manual PDF exists
  - [ ] Includes application overview
  - [ ] Shows GUI mockups
  - [ ] Lists all features
  - [ ] Explains how to use each feature

- [ ] System documentation PDF exists
  - [ ] Describes database schema
  - [ ] Includes ER diagram
  - [ ] Explains design decisions
  - [ ] Details all indices
  - [ ] Explains all 5 queries with SQL code
  - [ ] Documents API usage
  - [ ] Describes code structure

---

## ☑️ Final Submission Steps

### 1. Clean Up (Optional)

Remove files not needed for submission:

```bash
cd ~/dbms_assignment3
rm -f IMPLEMENTATION_SUMMARY.md
rm -f QUERIES_REFERENCE.md
rm -f CONVERT_TO_PDF_GUIDE.md
rm -f SUBMISSION_CHECKLIST.md
rm -f README.md
rm -f documentation/user_manual_template.md
rm -f documentation/system_docs_template.md
```

**Keep only required files!**

### 2. Verify Student IDs

- [ ] Determine your team's ID numbers
- [ ] Example format: ID1-ID2 becomes `123456789-987654321.zip`

### 3. Create Submission ZIP

```bash
cd ~/dbms_assignment3
zip -r ID1-ID2.zip src/ documentation/ requirements.txt
```

Replace `ID1-ID2` with your actual student IDs.

**Example:**
```bash
zip -r 123456789-987654321.zip src/ documentation/ requirements.txt
```

### 4. Verify ZIP Contents

```bash
unzip -l ID1-ID2.zip
```

Should show:
```
src/create_db_script.py
src/api_data_retrieve.py
src/queries_db_script.py
src/queries_execution.py
documentation/name_and_id.txt
documentation/user_manual.pdf
documentation/system_docs.pdf
documentation/mysql_and_user_password.txt
requirements.txt
```

- [ ] Verify all required files are in the ZIP
- [ ] Verify no extra files are included
- [ ] Verify file paths are correct (src/, documentation/)

### 5. Test ZIP File

```bash
# Extract to temp directory
mkdir /tmp/test_submission
unzip ID1-ID2.zip -d /tmp/test_submission
cd /tmp/test_submission

# Verify structure
ls -R
```

- [ ] All files extracted successfully
- [ ] Folder structure is correct
- [ ] Files open without errors

### 6. Final Checks

- [ ] ZIP file is named correctly (ID1-ID2.zip)
- [ ] ZIP file size is reasonable (should be < 10 MB)
- [ ] Database is populated on MySQL server
- [ ] Documentation PDFs are readable

---

## ☑️ Submission

### Before Submitting

- [ ] Re-read assignment requirements PDF
- [ ] Verify due date: **January 18, 2026, 23:59**
- [ ] Check submission platform/method
- [ ] Keep backup of ZIP file

### Submit

- [ ] Upload `ID1-ID2.zip` to submission system
- [ ] Verify upload successful
- [ ] Save confirmation email/screenshot

### After Submitting

- [ ] **DO NOT** delete database from MySQL server
  - Graders will check your populated database
  - Keep it accessible until grades are released

- [ ] Keep local copy of all files
- [ ] Keep copy of ZIP file

---

## ☑️ Common Issues to Avoid

### ❌ Don't Do This:

- [ ] ❌ Submitting .md files instead of .pdf
- [ ] ❌ Leaving credentials empty in Python files
- [ ] ❌ Submitting without running api_data_retrieve.py
- [ ] ❌ Having empty database on server
- [ ] ❌ Forgetting to fill in name_and_id.txt
- [ ] ❌ Wrong ZIP file name format
- [ ] ❌ Including .git, __pycache__, or .DS_Store files
- [ ] ❌ Submitting after deadline

### ✅ Do This:

- [ ] ✅ Submit PDFs (not markdown)
- [ ] ✅ Fill in all credentials
- [ ] ✅ Populate database before submission
- [ ] ✅ Test all scripts work
- [ ] ✅ Fill in all .txt files
- [ ] ✅ Use correct ZIP naming
- [ ] ✅ Clean submission with only required files
- [ ] ✅ Submit well before deadline

---

## 📊 Expected File Sizes

Use this as a reference:

| File | Expected Size |
|------|---------------|
| create_db_script.py | ~8-12 KB |
| api_data_retrieve.py | ~15-20 KB |
| queries_db_script.py | ~8-12 KB |
| queries_execution.py | ~8-12 KB |
| requirements.txt | ~100 bytes |
| name_and_id.txt | ~200 bytes |
| mysql_and_user_password.txt | ~200 bytes |
| user_manual.pdf | ~500 KB - 2 MB |
| system_docs.pdf | ~800 KB - 3 MB |
| **Total ZIP** | **~2-8 MB** |

---

## 🎯 Success Criteria

Your submission is ready if:

- ✅ All checkboxes above are checked
- ✅ All scripts run without errors
- ✅ Database has ~19,000 records
- ✅ All 5 queries return results
- ✅ Both PDFs are complete and readable
- ✅ ZIP file contains exactly the required files
- ✅ File naming is correct

---

## 📞 If You Need Help

If something isn't working:

1. Check error messages carefully
2. Verify credentials are correct
3. Ensure database is populated
4. Re-read documentation files
5. Check `IMPLEMENTATION_SUMMARY.md` for troubleshooting
6. Contact course staff if needed

---

## 🎉 You're Ready!

Once all items are checked, you're ready to submit!

**Good luck with your submission!** 🚀

---

**Last updated:** Before submission
**Assignment due:** January 18, 2026, 23:59
