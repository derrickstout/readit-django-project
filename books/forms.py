from django import forms
from .models import Book

class ReviewForm(forms.Form):
	"""
	Form for reviewing a book
	"""

	is_favorite = forms.BooleanField(
		label='Favorite?',
		help_text='In your top 100 books of all time?',
		required=False,
		)

	review = forms.CharField(
		# widget is HTML element that Django uses to render the field
		widget=forms.Textarea,
		min_length=10,
		error_messages={
			'required': 'This field is required. Please enter a review.',
			'min_length': 'Minimum review length is 30 characters. You have written %(show_value)s)'
			}
		)

# A ModelForm directly maps to the fields of a model
class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'authors']

	def clean(self):
		# Super the clean mentod to maintain main validation and error messages
		super(BookForm, self).clean()

		try:
			title = self.cleaned_data.get('title')
			authors = self.cleaned_data.get('authors')
			book = Book.objects.get(title=title, authors=authors)

			raise forms.ValidationError(
					'The book {} by {} already exists'.format(title, book.list_authors()),
					code='bookexists'
				)
		except Book.DoesNotExist:
			return self.cleaned_data