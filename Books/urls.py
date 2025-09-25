from django.contrib import admin
from django.urls import path, include
from Books import views

urlpatterns = [
   path('',views.books,name="books"),
    path('borrowbook/<int:id>/',views.borrowbook,name='borrow_book'),
    path('borrowed_book/',views.borrowed_book,name="borrowed_book"),
    path('returnbook/<int:id>/',views.return_book,name="return_book"),
    path('pay-penalty/<int:id>/', views.pay_penalty, name='pay_penalty')
]
