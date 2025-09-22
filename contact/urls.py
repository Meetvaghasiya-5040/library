from django.urls import path, include
from contact import views
urlpatterns = [
    path('',views.about,name="about"),
    path('contact/',views.contact,name="contact")
]
