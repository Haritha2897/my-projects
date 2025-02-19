from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from library_app.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ReviewForm,UserLoginForm,PasswordResetForm
from .models import Book, Review, Wishlist


def home(request):
    featured_books = Book.objects.filter(pk__isnull=False)[:3]  # Ensure all books have a primary key
    return render(request, 'home.html', {'featured_books': featured_books})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('user_dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def explore_books(request):
    categories = ['Fiction', 'Non-Fiction', 'Education', 'Science', 'Biography', 'Children']
    books_by_category = {category: Book.objects.filter(category=category) for category in categories}
    return render(request, 'explore_books.html', {'books_by_category': books_by_category})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


def login_view(request):
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset successfully.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User with provided username and email does not exist.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'password_reset.html', {'form': form})


@login_required
def review_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'book': book})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('user_dashboard')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('user_dashboard')
    return render(request, 'delete_review.html', {'review': review})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not Wishlist.objects.filter(user=request.user, book=book).exists():
        Wishlist.objects.create(user=request.user, book=book)
        messages.success(request, f'{book.title} added to wishlist.')
    else:
        messages.info(request, f'{book.title} is already in your wishlist.')
    return redirect('user_dashboard')

@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, book=book)
        wishlist_item.delete()
        messages.success(request, f'{book.title} removed from wishlist.')
    except Wishlist.DoesNotExist:
        messages.error(request, 'This book is not in your wishlist.')
    return redirect('user_dashboard')

@login_required
def mark_as_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, book=book)
        wishlist_item.is_read = not wishlist_item.is_read
        wishlist_item.save()
        status = 'marked as read' if wishlist_item.is_read else 'marked as unread'
        messages.success(request, f'{book.title} {status}.')
    except Wishlist.DoesNotExist:
        messages.error(request, 'This book is not in your wishlist.')
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        book_id = request.POST.get('book_id')
        if action == 'add_to_wishlist' and book_id:
            return add_to_wishlist(request, book_id)
        elif action == 'mark_as_read' and book_id:
            return mark_as_read(request, book_id)
        else:
            messages.error(request, "Invalid action or no book selected.")
            return redirect('user_dashboard')
    reviews = request.user.reviews.all()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    books = Book.objects.all()
    return render(request, 'user_dashboard.html', {'reviews': reviews, 'wishlist_items': wishlist_items, 'books': books})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
