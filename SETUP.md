# MovieFinder Setup Guide

## Prerequisites

- Python 3.14+
- MySQL Server access (via SSH tunnel)
- TMDb API key

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yaronya/DBMS_HW3.git
cd DBMS_HW3
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# TMDb API Configuration
TMDB_API_KEY=your_tmdb_api_key_here

# MySQL Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3305
DB_USER=yarony
DB_PASSWORD=your_mysql_password_here
DB_NAME=yarony
```

**Important:** Never commit the `.env` file to git. It's already in `.gitignore`.

### 4. Set Up SSH Tunnel (if using remote MySQL)

```bash
ssh -L 3305:mysqlsrv1.cs.tau.ac.il:3306 yarony@nova.cs.tau.ac.il
```

Keep this terminal open while running the scripts.

### 5. Create Database Schema

```bash
cd src
python3 create_db_script.py
```

### 6. Populate Database (Optional - takes 30-40 minutes)

```bash
python3 api_data_retrieve.py
```

**Note:** The database is already populated on the server. You only need to run this if starting fresh.

### 7. Test Queries

```bash
python3 queries_execution.py
```

## Getting TMDb API Key

1. Go to https://www.themoviedb.org/
2. Create an account
3. Navigate to Settings > API
4. Request an API key (choose "Developer")
5. Copy the "API Key (v3 auth)"

## Security Notes

- ⚠️ **Never commit `.env` file**
- ⚠️ **Never hardcode credentials in Python files**
- All sensitive configuration is in `.env` file
- `.env.example` provides the template without secrets
