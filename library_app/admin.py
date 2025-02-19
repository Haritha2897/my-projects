
from django.contrib import admin
from .models import User, Book, Review, Wishlist

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'date_of_birth', 'date_of_joining', 'gender', 'membership_type', 'agree_to_terms')
    list_filter = ('date_of_joining', 'gender', 'membership_type')
    search_fields = ('username', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date')
    list_filter = ('category', 'publication_date')
    search_fields = ('title', 'author')
   
@admin.register(Review)
class ReviewAdmAin(admin.ModelAdmin):
    list_display = ('book', 'user', 'comment', 'rating', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('book__title', 'user__username')
    readonly_fields = ('book', 'user', 'comment', 'rating', 'created_at', 'updated_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_read', 'added_at')
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('user', 'book', 'is_read', 'added_at')