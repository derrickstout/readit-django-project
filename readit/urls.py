"""readit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.contrib import admin
# Django's auth app provides login/out screens
# importing as auth_views to be more specific
from django.contrib.auth import views as auth_views
from books.views import (AuthorDetail, AuthorList, BookDetail, CreateAuthor, 
						list_books,	ReviewList, review_book)

urlpatterns = [
	# Auth
	# The dictionary redirects to books page, rather than default Admin logout screen
	url(r'^logout/$', auth_views.logout, {'next_page': 'books'}, name='logout'),
	url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),

	# Admin
    url(r'^admin/', admin.site.urls),

    # Custom
    url(r'^$', list_books, name='books'),
    # Class-based views need "as_view" method to tell Django
    # to treat it as a view
    url(r'^authors/$', AuthorList.as_view(), name='authors'),
    url(r'^books/(?P<pk>[-\w]+)/$', BookDetail.as_view(), name='book-detail'),
    url(r'^authors/add/$', login_required(CreateAuthor.as_view()), name='add-author'),
    url(r'^authors/(?P<pk>[-\w]+)/$', AuthorDetail.as_view(), name='author-detail'),
    url(r'^review/$', login_required(ReviewList.as_view()), name='review-books'),
	url(r'^review/(?P<pk>[-\w]+)/$', review_book, name='review-book'),
]
