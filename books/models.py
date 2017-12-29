# importing user object to add user data to models (reviewed by)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=150)
	authors = models.ManyToManyField("Author", related_name="books")
	review = models.TextField(blank=True, null=True)
	#like ManyToMany, first argument is model we want to create a relationship with
	reviewed_by = models.ForeignKey(User, blank=True, null=True, related_name="reviews")
	date_reviewed = models.DateTimeField(blank=True, null=True)
	is_favorite = models.BooleanField(default=False, verbose_name="Favorite?")

	def __str__(self):
		return "{} by {}".format(self.title, self.list_authors())

	def list_authors(self):
		return ", ".join([author.name for author in self.authors.all()])

	def save(self, *args, **kwargs):
		if (self.review and self.date_reviewed is None):
			self.date_reviewed = now()

		# super class saves automatically somehow
		super(Book, self).save(*args, **kwargs)

class Author(models.Model):
	name = models.CharField(max_length=70, help_text="Use pen name, not real name", unique=True)

	def __str__(self):
		return self.name

	# Getting the absolute URL is necessary for the form to add new authors to work
	def get_absolute_url(self):
		# reverse function takes URL name and returns URL
		return reverse('author-detail', kwargs={'pk', self.pk})