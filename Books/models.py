from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime,date,timedelta

class Book(models.Model):
    book_title=models.CharField(max_length=100,default="Unkown")
    book_autor=models.CharField(max_length=100,default="Unkown")
    isbn_num=models.CharField(max_length=13,unique=True)
    book_price=models.DecimalField(max_digits=17,default=0,decimal_places=2)
    is_avalible=models.BooleanField(default=True)
    copies=models.IntegerField(default=1)


class Borrow_book(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="Unknown")
    book=models.ForeignKey(Book,on_delete=models.CASCADE,default="Unknown")
    book_title=models.CharField(max_length=100,default="Unkown")
    borrow_date=models.DateTimeField(default=timezone.now)
    return_date=models.DateTimeField(default=date.today()+timedelta(days=2))
    panalty=models.DecimalField(max_digits=16,decimal_places=2,default=0)
    borrow_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_return=models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.username} borrowed {self.book.book_title}'
    
    def calculate_panalty(self,rate_per_day=10):
        today=date.today()
        if today > self.return_date:
            late_days=(today - self.return_date).days
            return late_days * rate_per_day
        return 0
    
# Create your models here.
