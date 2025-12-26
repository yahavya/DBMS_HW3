# How to Convert Documentation to PDF

You need to convert these markdown files to PDF for submission:
- `documentation/user_manual_template.md` → `documentation/user_manual.pdf`
- `documentation/system_docs_template.md` → `documentation/system_docs.pdf`

Here are several methods to do this:

---

## Method 1: Using Pandoc (Best Quality)

### Install Pandoc
**On macOS:**
```bash
brew install pandoc
brew install --cask basictex  # For PDF support
```

**On Windows:**
Download from: https://pandoc.org/installing.html

**On Linux:**
```bash
sudo apt-get install pandoc texlive-latex-base
```

### Convert to PDF
```bash
cd ~/dbms_assignment3/documentation

# Convert user manual
pandoc user_manual_template.md -o user_manual.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  --toc \
  --highlight-style=tango

# Convert system docs
pandoc system_docs_template.md -o system_docs.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  --toc \
  --highlight-style=tango
```

### Options Explained:
- `--pdf-engine=xelatex` - Use XeLaTeX for better Unicode support
- `-V geometry:margin=1in` - Set 1-inch margins
- `--toc` - Add table of contents
- `--highlight-style=tango` - Syntax highlighting for code blocks

---

## Method 2: Using VS Code Extension

### Install Extension
1. Open VS Code
2. Install "Markdown PDF" extension by yzane

### Convert
1. Open the `.md` file in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Markdown PDF: Export (pdf)"
4. Press Enter

The PDF will be created in the same directory!

---

## Method 3: Online Converters (Quick & Easy)

### Option A: Markdown to PDF
Website: https://www.markdowntopdf.com/

Steps:
1. Copy all content from `user_manual_template.md`
2. Paste into the website
3. Click "Convert"
4. Download as `user_manual.pdf`
5. Repeat for `system_docs_template.md`

### Option B: Dillinger
Website: https://dillinger.io/

Steps:
1. Open the website
2. Click "Import from..." → "From Disk"
3. Select the `.md` file
4. Click "Export as" → "PDF"
5. Save with correct filename

### Option C: md2pdf
Website: https://md2pdf.netlify.app/

Steps:
1. Paste markdown content
2. Click "Convert to PDF"
3. Download

---

## Method 4: Using Google Docs

### Steps:
1. Open Google Docs: https://docs.google.com
2. Create new document
3. **For user_manual.pdf:**
   - Copy content from `user_manual_template.md`
   - Paste into Google Docs
   - Format manually:
     - Title: Large, bold
     - Headings: Use "Heading 1", "Heading 2", etc.
     - Code blocks: Use monospace font (Courier New)
     - Tables: Insert → Table
   - File → Download → PDF Document (.pdf)
   - Rename to `user_manual.pdf`

4. **Repeat for system_docs_template.md** → `system_docs.pdf`

**Pros:** Easy, no installation needed
**Cons:** Manual formatting required

---

## Method 5: Using Microsoft Word

### Steps:
1. Open Word
2. File → Open → Select `.md` file
3. Word will import the markdown
4. Format as needed:
   - Apply styles (Heading 1, Heading 2, etc.)
   - Format code blocks (monospace font)
   - Adjust tables
5. File → Save As → PDF
6. Rename to correct filename

---

## Recommended Approach

**Best for quality:** Method 1 (Pandoc)
**Best for simplicity:** Method 3 (Online converter)
**Best for customization:** Method 4 (Google Docs)

---

## After Conversion: Verify PDFs

Make sure your PDFs include:

### user_manual.pdf should have:
- [ ] Application overview section
- [ ] All 5 features described
- [ ] UI mockups (the ASCII art diagrams)
- [ ] "How to Use" instructions for each feature
- [ ] ~10-15 pages

### system_docs.pdf should have:
- [ ] Database schema section with ER diagram
- [ ] All 6 table descriptions
- [ ] Design decisions section
- [ ] All 9 index explanations
- [ ] All 5 query explanations with SQL code
- [ ] API integration section
- [ ] Code structure section
- [ ] ~20-25 pages

---

## File Naming

Make sure final PDFs are named exactly:
- `user_manual.pdf` (NOT user_manual_template.pdf)
- `system_docs.pdf` (NOT system_docs_template.pdf)

---

## Placement

PDFs should be in:
```
dbms_assignment3/
└── documentation/
    ├── user_manual.pdf       ← Required for submission
    ├── system_docs.pdf       ← Required for submission
    ├── name_and_id.txt
    └── mysql_and_user_password.txt
```

---

## Troubleshooting

### Problem: Code blocks not formatted properly
**Solution:** Use monospace font (Courier New, Consolas, or Monaco)

### Problem: Tables are broken
**Solution:**
- Simplify table formatting
- Use online converter that handles tables better
- Manually recreate tables in Word/Google Docs

### Problem: Special characters not displaying
**Solution:**
- Use Pandoc with `--pdf-engine=xelatex`
- Or replace special characters with simpler ones

### Problem: File too large
**Solution:**
- PDFs should be 1-5 MB, which is fine
- If larger, use PDF compression tool

---

## Quick Command Reference

### Using Pandoc (One Command):
```bash
cd ~/dbms_assignment3/documentation
pandoc user_manual_template.md -o user_manual.pdf --pdf-engine=xelatex -V geometry:margin=1in
pandoc system_docs_template.md -o system_docs.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

### Verify files were created:
```bash
ls -lh user_manual.pdf system_docs.pdf
```

---

Good luck with the conversion! The markdown files are designed to convert well to PDF with any of these methods.
