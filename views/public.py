import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

from django.http import HttpResponse
from django.http import HttpResponseRedirect	
from django.shortcuts import render_to_response

from models import Book
from models import Reader
from models import ReaderBook

from helpers import paging
from helpers import mapping

def index(request, username=None, state=None, page=1):
	reader = Reader.byUsername(username)
	
	if not reader:
		return HttpResponse('No such username')
	
	page = int(page)
	template_values = {}
	
	template_values["currentState"] = state
	template_values["readOnly"] = True
	template_values["books"] = []
	template_values["toReadCount"] = reader.toReadCount
	template_values["inProgressCount"] = reader.inProgressCount
	template_values["finishedCount"] = reader.finishedCount
	template_values["totalCount"] = reader.totalCount	
	
	# paging stuff
	paging.preparePagingTemplateForBookcase(template_values, reader, state, page)
	# end paging stuff
		
	for readerBook in ReaderBook.byReaderAndState(reader, state, page - 1):
		template_values["books"].append(mapping.toReaderBookTemplate(readerBook.book, readerBook))
	
	template_values["navRoot"] = "/public/" + username
	
	return render(template_values)
	
def render(template_values):
	return render_to_response('bookcase.html', template_values)