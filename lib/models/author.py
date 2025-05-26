from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self._name = None
        self.name = name  # Use setter for validation
        if id is None:
            self._save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def _save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?) RETURNING id",
                (self.name,)
            )
            self._id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to save author: {e}")
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def add_article(self, magazine, title):
        from .article import Article
        return Article(title, self, magazine)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [row['category'] for row in results]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return cls(result['name'], result['id']) if result else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        return cls(result['name'], result['id']) if result else None