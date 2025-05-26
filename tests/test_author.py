import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
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

def test_author_initialization(setup_database):
    author = Author("John Doe")
    assert author.name == "John Doe"
    assert author.id is not None

def test_author_name_validation(setup_database):
    with pytest.raises(ValueError):
        Author("")
    with pytest.raises(ValueError):
        Author(123)

def test_author_articles(setup_database):
    author = Author("Jane Smith")
    magazine = Magazine("Tech Today", "Technology")
    author.add_article(magazine, "Test Article")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0]['title'] == "Test Article"

def test_author_magazines(setup_database):
    author = Author("Alice Johnson")
    mag1 = Magazine("Tech Today", "Technology")
    mag2 = Magazine("Health Matters", "Health")
    author.add_article(mag1, "Tech Article")
    author.add_article(mag2, "Health Article")
    magazines = author.magazines()
    assert len(magazines) == 2
    assert {m['name'] for m in magazines} == {"Tech Today", "Health Matters"}

def test_author_topic_areas(setup_database):
    author = Author("Bob Brown")
    mag1 = Magazine("Tech Today", "Technology")
    mag2 = Magazine("Health Matters", "Health")
    author.add_article(mag1, "Tech Article")
    author.add_article(mag2, "Health Article")
    topics = author.topic_areas()
    assert set(topics) == {"Technology", "Health"}

def test_find_by_id(setup_database):
    author = Author("John Doe")
    found = Author.find_by_id(author.id)
    assert found.name == "John Doe"
    assert found.id == author.id

def test_find_by_name(setup_database):
    Author("Jane Smith")
    found = Author.find_by_name("Jane Smith")
    assert found.name == "Jane Smith"