from django import forms

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