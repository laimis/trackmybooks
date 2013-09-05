from models import Book
from amazon import AmazonInterface

from django.shortcuts import render_to_response

import logging
import urllib

def setPages(request):

	title = request.GET["title"]
	
	if not title:
		book = Book.all().order('title').get()
	else:
		book = Book.all().order('title').filter('title >', title).get()
	
	if not book:
		errorMsg = "Finished converting books"
		logging.info(errorMsg)
		return createErrorResponse(errorMsg)
	
	if book.tags:
		errorMsg = "Skipping conversion of book " + book.title
		logging.info(errorMsg)
		return createResponse(book)
	
	fromSearchResults = AmazonInterface().getBookByIsbn(book.isbn)
	
	if not fromSearchResults:
		errorMsg = "Couldn't load the book from amazon: " + book.isbn
		logging.error(errorMsg)
		return createResponse(book, errorMsg, 5)
		
	book.numberOfPages = fromSearchResults.numberOfPages
	book.put()
	
	return createResponse(book)

def createErrorResponse(msg):
	return render_to_response('conversionBookPages.html', {"error" : msg})
	
def createResponse(book, errorMsg = None, interval = 2):
	
	response = {
		"currentBook" : book.title + str(book.numberOfPages),
		"currentBookEscaped" : urllib.quote_plus(book.title.replace(u'\xa0', ' ')),
		"success" : True,
		"internval" : interval
	}
	
	return render_to_response('conversionBookPages.html', response)	