from django.contrib import admin
from contact.models import ContactUs
from unfold.admin import ModelAdmin as UnfoldModelAdmin


class ContactAdmin(UnfoldModelAdmin):
    list_display=('first_name','last_name','email','phone','subject','message')
    list_filter=('first_name','last_name','phone')

admin.site.register(ContactUs,ContactAdmin)

# Register your models here.
