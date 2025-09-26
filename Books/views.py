from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Book, Borrow_book
from .utils import check_internet


def books(request):
    books = Book.objects.all()
    internet = check_internet()
    if request.method == 'POST':
        bt = request.POST.get('book_name')
        if bt is not None:
            books = Book.objects.filter(book_title__icontains=bt)

    return render(request, 'books.html', {'books': books, 'internet': internet})


@login_required
def borrowbook(request, id):
    print("Book id :", id)
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id) 
        borrow_price = float(book.book_price) * 0.1
        
        # Check if user already has this book borrowed and not returned
        already_borrowed = Borrow_book.objects.filter(
            user=request.user, 
            book=book, 
            is_return=False
        ).exists()
        
        if already_borrowed:
            messages.error(request, f'You have already borrowed "{book.book_title}"!')
            return redirect('borrowed_book')
        
        if book.is_avalible and book.copies > 0:   
            # Create borrow record with 7-day return period
            return_date = timezone.now() + timedelta(days=7)
            
            Borrow_book.objects.create(
                user=request.user,
                book=book,
                book_title=book.book_title,
                borrow_date=timezone.now(),
                return_date=return_date,
                borrow_price=borrow_price
            )
            
            # Update book availability
            book.copies -= 1
            if book.copies == 0:
                book.is_avalible = False
            book.save()
            
            messages.success(request, f'You have successfully borrowed "{book.book_title}"! Please return by {return_date.strftime("%Y-%m-%d")}')
        else:
            messages.error(request, 'This book is not available for borrowing.')
    
    return redirect('borrowed_book')


@login_required
def borrowed_book(request):
    internet = check_internet()
    borrowed_books = Borrow_book.objects.filter(user=request.user, is_return=False)
    
    # Calculate penalties for all borrowed books
    for borrowed in borrowed_books:
        borrowed.calculate_penalty()
        
        # Send overdue email notification (only if overdue and not already notified recently)
        if borrowed.is_overdue():
            # You might want to add a field to track when last email was sent
            # to avoid sending emails too frequently
            try:
                email_subject = f'Overdue Book Return Notice - {borrowed.book_title}'
                email_message = (
                    f'Dear {request.user.first_name or request.user.username},\n\n'
                    f'Your borrowed book "{borrowed.book_title}" is now overdue.\n'
                    f'Return date was: {borrowed.return_date.strftime("%Y-%m-%d")}\n'
                    f'Current penalty: ${borrowed.penalty}\n'
                    f'Daily penalty rate: ${borrowed.penalty_per_day}\n\n'
                    f'Please return the book as soon as possible to avoid additional penalties.\n\n'
                    f'Thank you,\nLibrary Management System'
                )
                
                if request.user.email:
                    send_mail(
                        email_subject,
                        email_message,
                        None,  # Use default FROM_EMAIL from settings
                        [request.user.email],
                        fail_silently=True,  # Don't break if email fails
                    )
            except Exception as e:
                print(f"Email sending failed: {e}")
    
    return render(request, 'borrowbook.html', {
        'borrowed': borrowed_books, 
        'internet': internet
    })


@login_required
def return_book(request, id):
    if request.method == 'POST':
        borrowed = get_object_or_404(Borrow_book, id=id, user=request.user)
        book = borrowed.book
        
     
        final_penalty = borrowed.calculate_penalty()
        
        
        if final_penalty > 0 and not borrowed.penalty_paid:
            messages.warning(
                request, 
                f'Book "{book.book_title}" has an outstanding penalty of ${final_penalty:.2f}. '
                f'Please pay the penalty before returning the book.'
            )
            return redirect('borrowed_book')
        
  
        book.copies += 1
        book.is_avalible = True 
        book.save()
        
        
        borrowed.is_return = True
        borrowed.save()
        
        messages.success(request, f'You have successfully returned "{book.book_title}"!')
        return redirect('books')
    
    return redirect('borrowed_book')


@login_required 
def pay_penalty(request, id):
    """Handle penalty payment"""
    if request.method == 'POST':
        borrowed = get_object_or_404(Borrow_book, id=id, user=request.user)
        
        
        current_penalty = borrowed.calculate_penalty()
        
        if current_penalty > 0:
            
            borrowed.penalty_paid = True
            borrowed.save()
            
            messages.success(
                request, 
                f'Penalty of ${current_penalty:.2f} has been paid for "{borrowed.book_title}"!'
            )
        else:
            messages.info(request, 'No penalty to pay for this book.')
    
    return redirect('borrowed_book')


def send_overdue_notifications():
    
    overdue_books = Borrow_book.objects.filter(
        is_return=False,
        return_date__lt=timezone.now()
    )
    
    for borrowed in overdue_books:
        borrowed.calculate_penalty()
        
        try:
            email_subject = f'Overdue Book Notice - {borrowed.book_title}'
            email_message = (
                f'Dear {borrowed.user.first_name or borrowed.user.username},\n\n'
                f'Your book "{borrowed.book_title}" is overdue.\n'
                f'Current penalty: ${borrowed.penalty}\n'
                f'Please return immediately.\n\n'
                f'Library Management System'
            )
            
            if borrowed.user.email:
                send_mail(
                    email_subject,
                    email_message,
                    None,
                    [borrowed.user.email],
                    fail_silently=True,
                )
        except Exception as e:
            print(f"Failed to send email for {borrowed.user.username}: {e}")