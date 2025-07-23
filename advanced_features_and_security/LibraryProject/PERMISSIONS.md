# Permissions & Groups Setup

## Custom Book Permissions
Defined in `bookshelf/models.py` on `Book.Meta.permissions`:
- `can_view`:   View book details
- `can_create`: Create a new book
- `can_edit`:   Edit existing books
- `can_delete`: Delete books

## Groups
- **Viewers**: can_view  
- **Editors**: can_view, can_create, can_edit  
- **Admins** : can_view, can_create, can_edit, can_delete  

## View Protection
Each book‑action view in `bookshelf/views.py` uses:
```python
@permission_required('bookshelf.can_<action>', raise_exception=True)
