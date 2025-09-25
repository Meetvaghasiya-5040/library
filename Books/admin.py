from django.contrib import admin
from Books.models import Book,Borrow_book
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin



class BookAdmin(UnfoldModelAdmin):
    list_display=('book_title','book_autor','isbn_num','book_price','copies')


admin.site.register(Book,BookAdmin)

class BorrowAdmin(UnfoldModelAdmin):
    list_display=('user','book_title','borrow_date','return_date','borrow_price','penalty')

    list_filter=('user',)
    search_fields=('user__username','book_title')
    def get_queryset(self, request):
        qs=super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()

admin.site.register(Borrow_book,BorrowAdmin)


class Borrowinline(admin.TabularInline):
    model=Borrow_book
    extra=0

admin.site.unregister(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines=[Borrowinline]
    class Media:
        js=("static/js/admin_refrech.js")

admin.site.register(User,CustomUserAdmin)


