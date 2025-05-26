import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.db.seed import seed_database
import sqlite3

def setup_database():
    # Read and execute schema
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    
    # Seed the database
    seed_database()
    print("Database setup and seeded successfully!")

if __name__ == "__main__":
    setup_database()