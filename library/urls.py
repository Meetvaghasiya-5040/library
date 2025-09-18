"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', view.home, name='home'),
    path('login/', view.loginview, name='login'),
    path('register/', view.registerview, name='register'),
    path('logout/', view.logoutview, name='logout'),
    path('books/',view.books,name="books"),
    path('borrowbook/<int:id>/',view.borrowbook,name='borrow_book'),
    path('borrowed_book/',view.borrowed_book,name="borrowed_book"),
    path('returnbook/<int:id>/',view.return_book,name="return_book")
]
