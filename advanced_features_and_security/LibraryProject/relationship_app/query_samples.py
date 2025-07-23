import os
import django

# Bootstrap Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries(author_name, library_name):
    # 1. Query all books by a specific author.
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books_by_author:
        print(" -", book.title)

    # 2. List all books in a library.
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library_name}:")
    for book in books_in_library:
        print(" -", book.title)

    # 3. Retrieve the librarian for a library.
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian at {library_name}: {librarian.name}")

if __name__ == '__main__':
    # Replace with actual names from your DB
    run_queries('Some Author', 'Central Library')
