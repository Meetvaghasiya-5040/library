from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Book(models.Model):
    book_title = models.CharField(max_length=100, default="Unknown")
    book_autor = models.CharField(max_length=100, default="Unknown")
    isbn_num = models.CharField(max_length=13, unique=True)
    book_price = models.DecimalField(max_digits=17, default=0, decimal_places=2)
    is_avalible = models.BooleanField(default=True)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.book_title


class Borrow_book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100, default="Unknown")
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))  # 7 days default
    penalty = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_return = models.BooleanField(default=False)
    penalty_per_day = models.DecimalField(default=10, decimal_places=2, max_digits=20)
    penalty_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} borrowed {self.book.book_title}'
    
    def calculate_penalty(self):
        """Calculate penalty based on overdue days"""
        today = timezone.now().date()
        return_date = self.return_date.date() if hasattr(self.return_date, 'date') else self.return_date
        
        if today > return_date:
            days_late = (today - return_date).days
            calculated_penalty = days_late * float(self.penalty_per_day)
            self.penalty = calculated_penalty
            self.save()
            return calculated_penalty
        else:
            self.penalty = 0
            self.save()
            return 0
    
    def is_overdue(self):
        """Check if book is overdue"""
        today = timezone.now().date()
        return_date = self.return_date.date() if hasattr(self.return_date, 'date') else self.return_date
        return today > return_date
    
    def days_until_due(self):
        """Get days until due date (negative if overdue)"""
        today = timezone.now().date()
        return_date = self.return_date.date() if hasattr(self.return_date, 'date') else self.return_date
        return (return_date - today).days