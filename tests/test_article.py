import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
    """)
    conn.commit()
    conn.close()

def test_article_initialization(setup_database):
    author = Author("John Doe")
    magazine = Magazine("Tech Today", "Technology")
    article = Article("Test Article", author, magazine)
    assert article.title == "Test Article"
    assert article.author == author
    assert article.magazine == magazine
    assert article.id is not None

def test_article_title_validation(setup_database):
    author = Author("Jane Smith")
    magazine = Magazine("Health Matters", "Health")
    with pytest.raises(ValueError):
        Article("", author, magazine)
    with pytest.raises(ValueError):
        Article(123, author, magazine)

def test_find_by_id(setup_database):
    author = Author("Alice Johnson")
    magazine = Magazine("Tech Today", "Technology")
    article = Article("Tech Article", author, magazine)
    found = Article.find_by_id(article.id)
    assert found.title == "Tech Article"
    assert found.author.name == "Alice Johnson"
    assert found.magazine.name == "Tech Today"