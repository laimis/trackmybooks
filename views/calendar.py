from google.appengine.ext import db

from django.shortcuts import render_to_response

from models import Reader
from models import Book
from models import ReaderBook

import datetime

def index(request):
	
	reader = Reader().byCurrentUser()
	fromDate = getPastDate(1)
	finished = ReaderBook.finishedBooks(reader, fromDate)

	# 12 months where each is a list to a book
	months = [[] for i in range(12)]
	
	for b in finished:
		if b.finishedDate:
			months[b.finishedDate.month - 1].append(b.book.title)
		
	tv = {}
	tv["months"] = months
	
	return render(tv)
	
def layout(request):

	# get all the books within x amount of time layed out by date
	# go by each day from the earliest day
	# output day and the book that is being read on that day
	# and continue doing that until all the books have been output
	reader = Reader().byCurrentUser()
	fromDate = getPastDate(2)
	finished = ReaderBook.finishedBooks(reader, fromDate)
	
	currentDate = fromDate
	byDate = {}
	while currentDate <= datetime.date.today() + datetime.timedelta(days=1):
		list = matchedBookByDate(currentDate, finished)
		byDate[currentDate] = []
		for b in list:
			byDate[currentDate].append(b.book.title)
		currentDate = currentDate + datetime.timedelta(days=1)
	
	return render_to_response('layout.html', {"data" : sorted(byDate.iteritems())})
	
def matchedBookByDate(currentDate, bookList):
	list = []
	for b in bookList:
		startedDate = b.inProgressDate
		finishedDate = b.finishedDate
		if startedDate == None:
			startedDate = finishedDate - datetime.timedelta(days=5)
		startedDate = startedDate.date()
		finishedDate = finishedDate.date()
		
		if currentDate >= startedDate and currentDate <= finishedDate:
			list.append(b)
			
	return list
	
def getPastDate(years):
	today = datetime.date.today()
	return today.replace(year=today.year - years)
	
def render(template_values):
	return render_to_response('calendar.html', template_values)