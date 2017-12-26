# Count lets us count book for each author
from django.db.models import Count
from django.shortcuts import render
# Import View model so we can sub-class it for class-based views
# Need to sub-class DetailView for generic class-based views
from django.views.generic import DetailView, View
from .models import Author, Book

# Create your views here.

# Functional view, defined as function
# takes request object, returns response object
# This one returns the username of the logged in user
def list_books(request):
	"""
	List the books that have reviews
	"""

	# This "Book.objects" is why we needed to import Book model
	books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

	# Creates a dictionary to pass to render function,
	# so we can reference this info in our template
	# Best practice is to name this "context"
	context = {
		'books': books,
	}

	return render(request, "list.html", context)

# Class-based view
class AuthorList(View):
# get method tells Django how to handle HTTP get requests
# takes request, returns response, like funcitonal view
	def get(self, request):

		# .annotate temporarily stores # of books per author
		# for lifespan of quesry set
		authors = Author.objects.annotate(
			published_books = Count('books')
		).filter(
			published_books__gt=0
		)

		context = {
			'authors': authors,
		}

		return render(request, "authors.html", context)


# Generic Class-based Views, sub-classing DetailView, a built-in model
class BookDetail(DetailView):
	model = Book
	template_name = "book.html"

class AuthorDetail(DetailView):
	model = Author
	template_name = "author.html"
