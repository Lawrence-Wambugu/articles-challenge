from .connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    # Insert authors
    authors = [
        ("John Doe",),
        ("Jane Smith",),
        ("Alice Johnson",)
    ]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)

    # Insert magazines
    magazines = [
        ("Tech Today", "Technology"),
        ("Fashion Weekly", "Fashion"),
        ("Health Matters", "Health")
    ]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)

    # Insert articles
    articles = [
        ("Tech Trends 2025", 1, 1),
        ("AI Revolution", 1, 1),
        ("Fashion Forward", 2, 2),
        ("Healthy Living", 2, 3),
        ("Tech Gadgets", 3, 1),
        ("Diet Tips", 3, 3)
    ]
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database()