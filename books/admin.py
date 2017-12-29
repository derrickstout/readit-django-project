from django.contrib import admin
from .models import Author, Book

@admin.register(Book)

# This custom class organizes the book object fields in the Admin by group
# It also allows you to manipulate the fields as read only, etc
class BookAdmin(admin.ModelAdmin):
	fieldsets = [
		("Book Details", {"fields": ["title", "authors"]}),
		("Review", {"fields": ["is_favorite", "review", "reviewed_by", "date_reviewed"]}),
	]

	readonly_fields = ("date_reviewed",)

	# this method takes the object as an additional argument, not just self
	# purpose is to generate a list of authors for the book object in question
	# to display in the book list view
	def book_authors(self, obj):
		# This "list_authors" method was created in models.py
		return obj.list_authors ()

	book_authors.short_description = "Author(s)"

	#The list_display property contains columns we see in the book list page
	list_display = ("title", "book_authors","reviewed_by", "date_reviewed", "is_favorite",)

	# This allows you to edit the fields specified in the book list page
	list_editable = ("is_favorite",)

	# This allows you to sort these fields by clicking on the column header in 
	# the book list page. Also turns these fields into links that take you to object view
	list_display_links = ("title", "date_reviewed",)

	# This property allows you to filter the list by the fields specified
	list_filter = ("is_favorite",)

	# This property allows you to search by fields specified
	# We want to search by author name, and get there by using the double underscore
	# after "author" to access the value inside of the model/class
	search_fields = ("title", "authors__name",)

# Register your models here.

admin.site.register(Author)
# This line was removed because we are using a shortcut; the register decorator
# up top "@admin.register(Book)". Why is BookAdmin not in there? I do not know.
#admin.site.register(Book, BookAdmin)
