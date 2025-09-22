from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from .models import Book,Borrow_book
from .utils import check_internet
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone

def books(request):
    books=Book.objects.all()
    internet=check_internet()
    if request.method=='POST':
        bt=request.POST.get('book_name')
        if bt != None:
            books=Book.objects.filter(book_title__icontains=bt)

    return render(request,'books.html',{'books':books,'internet':internet})



@login_required
def borrowbook(request,id):
    print("Book id :",id)
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id) 
        borrow_price = float(book.book_price) * 0.1
        already_borrowed=Borrow_book.objects.filter(user=request.user,book=book).exists()
        if already_borrowed:
            messages.error(request,f'Book Already Borrowed a {book.book_title} !')
            return redirect('borrowed_book')
        
        if book.is_avalible and book.copies > 0:   
            Borrow_book.objects.create(
                user=request.user,
                book=book,
                book_title=book.book_title,
                borrow_date=timezone.now(),
                borrow_price=borrow_price
            )
            book.copies -= 1
            if book.copies == 0:
                book.is_available = False
            book.save()
            
            messages.success(request, f'You have successfully borrowed "{book.book_title}"!')
        else:
            messages.error(request, 'This book is not available for borrowing.')
    return redirect('borrowed_book')

@login_required
def borrowed_book(request):
    internet=check_internet()
    borrowed=Borrow_book.objects.filter(user=request.user) 
    return render(request,'borrowbook.html',{'borrowed':borrowed,'internet':internet})

def return_book(request,id):
    if request.method=='POST':
        borrowed=get_object_or_404(Borrow_book,id=id,user=request.user)
        book=borrowed.book

        book.copies += 1
        book.save()

        borrowed.delete()

        messages.success(request,f'You have return {book.book_title} successfully!')
        return redirect('books')


# Create your views here.
