# Articles Code Challenge

A Python project modeling Authors, Articles, and Magazines with a SQLite database, using raw SQL queries (no SQLAlchemy).

## Project Structure
code-challenge/
├── lib/                    # Code directory
│   ├── models/            # Author, Article, Magazine classes
│   ├── db/                # Database connection, schema, seed
│   ├── controllers/       # Optional business logic
│   ├── debug.py           # Interactive debugging
├── tests/                 # Test files for all models
├── scripts/               # Setup and query scripts
├── README.md              # This file
└── .gitignore             # Git ignore

text

Copy

## Setup
1. **Prerequisites**: Python 3.8+, `pipenv` or `venv`, SQLite.
2. **Install Dependencies**:
   - Pipenv: `pipenv install pytest`
   - Venv: `python -m venv env`, activate, then `pip install pytest`
3. **Database Setup**:
   ```bash
   python scripts/setup_db.py
# Usage
Run Tests: pytest
Debug: python lib/debug.py
Run Queries: python scripts/run_queries.py
# Features
Schema: Tables for Authors, Articles, Magazines with foreign keys.
Models: Classes with SQL methods for data and relationships.
Queries: Efficient SQL for relationships and aggregates.
Transactions: Safe database operations with error handling.
Tests: Full coverage of functionality and edge cases.
Bonus: Magazine.top_publisher() for most articles.
# Notes
Uses parameterized SQL to prevent injection.
Follows OOP principles and DRY.
Git repository with incremental commits (e.g., [Feature]: Add schema).
