from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self._name = None
        self._category = None
        self.name = name  # Use setter for validation
        self.category = category  # Use setter for validation
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

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def _save(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id",
                (self.name, self.category)
            )
            self._id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to save magazine: {e}")
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            """,
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in results]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [row['title'] for row in results]

    def contributing_authors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id, a.name
            HAVING COUNT(art.id) > 2
            """,
            (self.id,)
        )
        results = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in results]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return cls(result['name'], result['category'], result['id']) if result else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        return cls(result['name'], result['category'], result['id']) if result else None

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id, m.name, m.category
            ORDER BY COUNT(a.id) DESC
            LIMIT 1
            """
        )
        result = cursor.fetchone()
        conn.close()
        return cls(result['name'], result['category'], result['id']) if result else None