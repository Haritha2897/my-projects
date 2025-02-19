from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore_books, name='explore_books'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('password_reset/',views.password_reset, name='password_reset'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard
    path('book/<int:pk>/', views.book_detail, name='book_detail'),  # Book detail page
    path('review/<int:pk>/', views.review_book, name='review_book'),  # Review submission
    path('add_review/', views.add_review, name='add_review'),  # Adding review (separate page or form)
    path('edit_review/<int:pk>/', views.edit_review, name='edit_review'),  # Edit review
    path('delete_review/<int:pk>/', views.delete_review, name='delete_review'),  # Delete review
    path('add_to_wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add book to wishlist
    path('remove_from_wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # Remove from wishlist
    path('mark_as_read/<int:book_id>/', views.mark_as_read, name='mark_as_read'),  # Mark book as read/unread
    path('logout/', views.logout_view, name='logout'),  # Logout
]
