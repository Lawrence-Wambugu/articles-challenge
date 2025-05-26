from lib.models.author import Author
from lib.models.magazine import Magazine

def run_example_queries():
    print("Running example queries...")
    
    # Example: Get all articles by an author
    author = Author.find_by_name("John Doe")
    if author:
        print(f"\nArticles by {author.name}:")
        for article in author.articles():
            print(f"- {article['title']}")

    # Example: Get magazines an author contributed to
    if author:
        print(f"\nMagazines {author.name} contributed to:")
        for magazine in author.magazines():
            print(f"- {magazine['name']} ({magazine['category']})")

    # Example: Get top publisher
    top_mag = Magazine.top_publisher()
    if top_mag:
        print(f"\nTop Publisher: {top_mag.name} ({top_mag.category})")

if __name__ == "__main__":
    run_example_queries()