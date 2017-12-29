from django.core.urlresolvers import reverse
# Count lets us count book for each author
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
# Import View model so we can sub-class it for class-based views
# Need to sub-class DetailView for generic class-based views
from django.views.generic import DetailView, View
# importing to subclass for CreateAuthor page
from django.views.generic.edit import CreateView
# Import Classes from forms.py
from .forms import BookForm, ReviewForm
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



class ReviewList(View):
	"""
	List all of the books that we want to review.
	"""
	def get(self, request):
		books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
		
		context = {
			'books': books,
			'form': BookForm,
		}
		
		return render(request, "list-to-review.html", context)

	def post(self, request):
		form = BookForm(request.POST)
		books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

		if form.is_valid():
			form.save()
			return redirect('review-books')

		context = {
			'form': form,
			'books': books
		}

		return render(request, "list-to-review.html", context)

	
# Functional view using forms

def review_book(request, pk):
	"""
	Review an individual book
	"""
	# This is a shortcut function
	book = get_object_or_404(Book, pk=pk)

	if request.method == 'POST':
		# process our form (bind request data to form)
		form = ReviewForm(request.POST)

		# checking validity with built in is_valid method
		# save the info and redirect to review_books view
		if form.is_valid():
			# setting object values from form data
			book.is_favorite = form.cleaned_data['is_favorite']
			book.review = form.cleaned_data['review']
			# Set this field to be the logged in user, so if logged in user submits
			# a review that was assigned to someone else, field updates correctly
			book.reviewed_by = request.user
			book.save()

			# redirect users to page by name
			# redirect is a shortcut, must be imported from Django
			return redirect('review-books')

	else:
		# render empty form
		form = ReviewForm
	
	context = {
		'book': book,
		'form': form,
	}
	
	return render(request, "review-book.html", context)

class CreateAuthor(CreateView):
	model = Author
	fields = ['name',]
	template_name = "create-author.html"

	def get_success_url(self):
		return reverse('review-books')







