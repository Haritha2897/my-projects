from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)
    agree_to_terms = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.email})'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    summary = models.TextField()
    publication_date = models.DateField()
    pdf = models.FileField(upload_to='books/pdfs/')
    image = models.ImageField(upload_to='books/images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ['title']

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.user} on {self.book}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
