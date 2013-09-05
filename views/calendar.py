from google.appengine.ext import db

from django.shortcuts import render_to_response

from models import Reader
from models import Book
from models import ReaderBook

import datetime

def index(request):
	
	reader = Reader().byCurrentUser()
	fromDate = datetime.date(2011,1,1)
	finished = ReaderBook.finishedBooks(reader, fromDate)

	# 12 months where each is a list to a book
	months = [[] for i in range(12)]
	
	for b in finished:
		if b.finishedDate:
			months[b.finishedDate.month - 1].append(b.book.title)
		
	tv = {}
	tv["months"] = months
	
	return render(tv)
	
def render(template_values):
	return render_to_response('calendar.html', template_values)