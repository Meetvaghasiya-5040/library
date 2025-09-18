from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render
from django.contrib import messages
from Books.models import Book,Borrow_book
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Books.utils import check_internet


def home(request):
    internet=check_internet()
    return render(request,'index.html',{'internet':internet})

def loginview(request):
    if request.method=='POST':
        loginuser=request.POST.get('username')
        loginpassword=request.POST.get('password')
        user=authenticate(username=loginuser,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,'SuccessFully Logged In!')
            return redirect('home')
        
        else:
            messages.error(request,'Invalid Crendentials , Please try again!')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def registerview(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        lname=request.POST.get('lname')
        fname=request.POST.get('fname')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request,'Password not Match')
            return redirect('home')
        


        myuser=User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"You Library Account Was Created!")

        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
    

def logoutview(request):
    logout(request)
    messages.success(request,'Successfully Logged Out !')
    return redirect('home')
    


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
