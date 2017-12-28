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