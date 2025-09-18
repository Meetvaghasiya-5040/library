from django.contrib import admin
from Books.models import Book,Borrow_book
from unfold.admin import ModelAdmin as UnfoldModelAdmin

class BookAdmin(UnfoldModelAdmin):
    list_display=('book_title','book_autor','isbn_num','book_price','copies')


admin.site.register(Book,BookAdmin)

class BorrowAdmin(UnfoldModelAdmin):
    list_display=('user','book','borrow_date','return_date','borrow_price')

    def get_queryset(self, request):
        qs=super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()

admin.site.register(Borrow_book,BorrowAdmin)
# Register your models here.
