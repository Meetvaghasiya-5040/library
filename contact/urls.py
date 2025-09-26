from django.urls import include, path

from contact import views

urlpatterns = [
    path('',views.about,name="about"),
    path('contact/',views.contact,name="contact")
]
