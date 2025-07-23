from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Author, Book, Library, Librarian

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'date_of_birth', 'is_staff', 'is_superuser')
    ordering = ('email',)
    fieldsets = (
        (None,             {'fields': ('email', 'password')}),
        ('Personal info',  {'fields': ('date_of_birth', 'profile_photo')}),
        ('Permissions',    {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates',{'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)

# Also explicitly register CustomUser with CustomUserAdmin for clarity
admin.site.register(CustomUser, CustomUserAdmin)
