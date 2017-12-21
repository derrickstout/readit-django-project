from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Functional view, defined as function
# takes request object, returns response object
# This one returns the username of the logged in user
def list_books(request):
	return HttpResponse(request.user.username)