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

def test_magazine_initialization(setup_database):
    magazine = Magazine("Tech Today", "Technology")
    assert magazine.name == "Tech Today"
    assert magazine.category == "Technology"
    assert magazine.id is not None

def test_magazine_validation(setup_database):
    with pytest.raises(ValueError):
        Magazine("", "Technology")
    with pytest.raises(ValueError):
        Magazine("Tech Today", "")
    with pytest.raises(ValueError):
        Magazine(123, "Technology")

def test_magazine_articles(setup_database):
    magazine = Magazine("Health Matters", "Health")
    author = Author("John Doe")
    Article("Health Article", author, magazine)
    articles = magazine.articles()
    assert len(articles) == 1
    assert articles[0]['title'] == "Health Article"

def test_magazine_contributors(setup_database):
    magazine = Magazine("Tech Today", "Technology")
    author1 = Author("Jane Smith")
    author2 = Author("Alice Johnson")
    Article("Article 1", author1, magazine)
    Article("Article 2", author2, magazine)
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert {c.name for c in contributors} == {"Jane Smith", "Alice Johnson"}

def test_magazine_article_titles(setup_database):
    magazine = Magazine("Fashion Weekly", "Fashion")
    author = Author("Bob Brown")
    Article("Trend 1", author, magazine)
    Article("Trend 2", author, magazine)
    titles = magazine.article_titles()
    assert set(titles) == {"Trend 1", "Trend 2"}

def test_magazine_contributing_authors(setup_database):
    magazine = Magazine("Tech Today", "Technology")
    author1 = Author("John Doe")
    author2 = Author("Jane Smith")
    Article("Article 1", author1, magazine)
    Article("Article 2", author1, magazine)
    Article("Article 3", author1, magazine)
    Article("Article 4", author2, magazine)
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "John Doe"

def test_top_publisher(setup_database):
    mag1 = Magazine("Tech Today", "Technology")
    mag2 = Magazine("Health Matters", "Health")
    author = Author("Alice Johnson")
    Article("Article 1", author, mag1)
    Article("Article 2", author, mag1)
    Article("Article 3", author, mag2)
    top = Magazine.top_publisher()
    assert top.name == "Tech Today"