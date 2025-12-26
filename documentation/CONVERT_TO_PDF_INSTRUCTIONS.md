# Converting HTML Files to PDF - Quick Guide

## ✅ Files Ready for Conversion

1. **technical_database_report.html** → Convert to **system_docs.pdf**
2. **user_manual.html** → Convert to **user_manual.pdf**

---

## 📝 Method 1: Browser Print (Recommended - 2 minutes)

### For macOS (Chrome, Safari, or Firefox):

**Step 1: Open the first HTML file**
```bash
open /Users/ron/dbms_assignment3/documentation/technical_database_report.html
```

**Step 2: Print to PDF**
1. Press **⌘ + P** (Command + P) to open print dialog
2. In the print dialog, find the **PDF** button (bottom left)
3. Click **PDF** → **Save as PDF**
4. Save as: `system_docs.pdf`
5. Location: `/Users/ron/dbms_assignment3/documentation/`

**Step 3: Repeat for user manual**
```bash
open /Users/ron/dbms_assignment3/documentation/user_manual.html
```

1. Press **⌘ + P**
2. Click **PDF** → **Save as PDF**
3. Save as: `user_manual.pdf`
4. Location: `/Users/ron/dbms_assignment3/documentation/`

**Done!** ✅

---

## 📋 Verify PDFs Created

After conversion, check that you have:
```
/Users/ron/dbms_assignment3/documentation/
├── system_docs.pdf          ✅ (converted from technical_database_report.html)
├── user_manual.pdf          ✅ (converted from user_manual.html)
├── name_and_id.txt          ⚠️ (fill in your names/IDs)
└── mysql_and_user_password.txt  ✅
```

---

## 🎯 Next Steps After PDF Conversion

1. Fill in student names/IDs in `name_and_id.txt`
2. Create submission ZIP file
3. Submit!

---

## 💡 Tips for Best Results

- **Use Chrome or Safari** for most accurate PDF rendering
- **Check page breaks**: The CSS is optimized for clean page breaks
- **Margins**: Leave default print margins (they're already optimized)
- **Orientation**: Portrait (default)
- **Background graphics**: Enable if available (preserves colors)

---

## Alternative: Command Line (if you prefer)

If you have wkhtmltopdf installed:
```bash
cd /Users/ron/dbms_assignment3/documentation

# Convert technical report
wkhtmltopdf technical_database_report.html system_docs.pdf

# Convert user manual
wkhtmltopdf user_manual.html user_manual.pdf
```

To install wkhtmltopdf (if needed):
```bash
brew install wkhtmltopdf
```

---

## ✅ Both HTML Files Are Complete

### system_docs.pdf (from technical_database_report.html)
Includes ALL required sections:
- ✅ Database schema structure with ER diagram
- ✅ Design reasoning and alternative designs
- ✅ Index strategy and query optimization
- ✅ All 5 queries with SQL, purpose, and results
- ✅ Code structure overview
- ✅ API usage and data mapping

### user_manual.pdf (from user_manual.html)
Includes ALL required sections:
- ✅ Application overview and target audience
- ✅ 5 feature descriptions with use cases
- ✅ Visual mockups for all 5 pages
- ✅ Step-by-step usage instructions
- ✅ Backend query references

Both documents use matching professional styling with:
- Purple gradient headers
- Clean typography
- Visual mockups/wireframes
- Comprehensive content
- Print-optimized CSS
