from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from contact.models import ContactUs


class ContactAdmin(UnfoldModelAdmin):
    list_display=('first_name','last_name','email','phone','subject','message')
    list_filter=('first_name','last_name','phone')

admin.site.register(ContactUs,ContactAdmin)

# Register your models here.
