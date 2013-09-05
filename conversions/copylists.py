from models import LatestBooks
from models import BookList

from django.shortcuts import render_to_response

import logging
import urllib

def copyLists(request):

	books = LatestBooks.get()
	
	BookList.createUnread(books.added)
	BookList.createFinished(books.finished)
	BookList.createInProgress(books.inprogress)
	
	return createResponse(None)
	
def createResponse(book, errorMsg = None, interval = 2):
	
	response = {
		"success" : True
	}
	
	return render_to_response('conversionCopyLists.html', response)	