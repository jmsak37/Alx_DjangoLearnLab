import os
import django

# Bootstrap Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Library, Librarian

def run_queries(author_name, library_name):
    # 1. Query all books by a specific author.
    author = Author.objects.get(name=author_name)
    print(f"Books by {author_name}:")
    for book in author.books.all():
        print(" -", book.title)

    # 2. List all books in a library.
    library = Library.objects.get(name=library_name)
    print(f"\nBooks in {library_name}:")
    for book in library.books.all():
        print(" -", book.title)

    # 3. Retrieve the librarian for a library.
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian at {library_name}: {librarian.name}")

if __name__ == '__main__':
    # TODO: replace these with actual names in your DB
    run_queries('Some Author', 'Central Library')
