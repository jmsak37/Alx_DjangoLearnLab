import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

from django import setup
setup()

from relationship_app.models import Author, Book, Library

def run_queries():
    # 1. All books by a specific author:
    author = Author.objects.get(name='Jane Austen')
    print('Books by Jane Austen:', list(author.books.all()))

    # 2. All books in a library:
    library = Library.objects.get(name='Central Library')
    print('Books in Central Library:', list(library.books.all()))

    # 3. The librarian for a library:
    print('Librarian at Central Library:', library.librarian.name)

if __name__ == '__main__':
    run_queries()
