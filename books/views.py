from django.shortcuts import render
from .models import Book

# Create your views here.

# Functional view, defined as function
# takes request object, returns response object
# This one returns the username of the logged in user
def list_books(request):
	"""
	List the books that have reviews
	"""

	books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

	# Creates a dictionary to pass to render function,
	# so we can reference this info in our template
	# Best practice is to name this "context"
	context = {
		'books': books,
	}

	return render(request, "list.html", context)