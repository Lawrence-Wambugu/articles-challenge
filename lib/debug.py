from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
import code

# Create some sample data for debugging
if __name__ == "__main__":
    print("Starting interactive debugging session...")
    author = Author("John Doe")
    magazine = Magazine("Tech Today", "Technology")
    article = Article("Debug Article", author, magazine)
    
    # Start interactive console
    code.interact(local=locals())