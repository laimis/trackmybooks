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

def index(request, state=None, page=1):
	reader = Reader().byCurrentUser()
	user = users.get_current_user()
	page = int(page)
	template_values = {}
	
	if state:
		template_values["currentState"] = state
	else:
		template_values["currentState"] = ""
	
	if user: template_values["isLoggedIn"] = True
	else: template_values["isLoggedIn"] = False
		
	if not reader:
		template_values["loginUrl"] = users.create_login_url('/reader')	
	else:
		template_values["hasReader"] = True
		template_values["books"] = []
		template_values["toReadCount"] = reader.toReadCount
		template_values["inProgressCount"] = reader.inProgressCount
		template_values["finishedCount"] = reader.finishedCount
		template_values["totalCount"] = reader.totalCount
		template_values["showRatings"] = True
	
		# paging stuff
		paging.preparePagingTemplateForBookcase(template_values, reader, state, page)
		# end paging stuff
	
		if state == "unrated":
			collection = ReaderBook.byReaderUnrated(reader, page - 1)
		else:
			collection = ReaderBook.byReaderAndState(reader, state, page - 1)
			
		for readerBook in collection:
			template_values["books"].append(mapping.toReaderBookTemplate(readerBook.book, readerBook))
	
	template_values["navRoot"] = "/bookcase"
	template_values["viewtype"] = "searchresult.html"
	
	return render(template_values)
	
def render(template_values):
	return render_to_response('bookcase.html', template_values)