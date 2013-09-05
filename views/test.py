import os
import cgi 

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from taggable import Tag

from amazon import AmazonInterface


def index(request):

	tags = Tag.get_tags_by_frequency()
	
	concated = ""
	
	for t in tags:
		concated += t.tag + str(t.tagged_count) + ", "
		
	return HttpResponse("So many tags! " + concated)


def searchTest(request, isbn = None, query = None):
	
	if "query" in request.GET:
		query = request.GET["query"]
	
	if "isbn" in request.GET:
		isbn = request.GET["isbn"]
	
	response = "Not ran."
	
	if isbn:
		response = AmazonInterface().getBookByIsbn(isbn)
	
	if query:
		response = AmazonInterface().searchXml(query, 1)
		
	# return HttpResponse(response.content, mimetype="text/xml");
	return HttpResponse(str(response.numberOfPages));

def render(template_values):
	return render_to_response('book.html', template_values)
	
def redirectToBook(book):
	return HttpResponseRedirect('/book/view/' + book.identifier())