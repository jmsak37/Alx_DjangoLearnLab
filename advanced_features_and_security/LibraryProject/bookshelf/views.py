from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

# Create your views here.
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # …

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    # …

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    # …
