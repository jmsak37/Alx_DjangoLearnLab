import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library

def run_queries():
    # 1. All books by a specific author
    author = Author.objects.first()
    print(f"Books by {author.name}:")
    for b in author.books.all():
        print(" -", b.title)

    # 2. List all books in a library
    library = Library.objects.first()
    print(f"\nBooks in {library.name}:")
    for b in library.books.all():
        print(" -", b.title)

    # 3. Retrieve the librarian for a library
    print(f"\nLibrarian at {library.name}: {library.librarian.name}")

if __name__ == '__main__':
    run_queries()
