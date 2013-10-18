import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

from django.http import HttpResponse
from django.http import HttpResponseRedirect	
from django.template.loader import get_template
from django.template import Context

from models import Book
from models import Reader
from models import ReaderBook
from models import BookList
from helpers import mapping

def index(request):
	reader = Reader().byCurrentUser()
	user = users.get_current_user()
	
	template_values = {}
	
	if user: template_values["isLoggedIn"] = True
	else: template_values["isLoggedIn"] = False
		
	if not reader:
		template_values["loginUrl"] = users.create_login_url('/reader')	
	
	addedBooks = BookList.getUnread()
	finishedBooks = BookList.getFinished()
	inprogressBooks = BookList.getInProgress()
	
	template_values["addedBooks"] = []
	template_values["finishedBooks"] = []
	template_values["inprogressBooks"] = []
	
	def appendBooks(bookList, viewList):
		if bookList is None:
			bookList = BookList()
			
		if bookList.list is None: 
			bookList.list = ()
			
		for key in bookList.list[0:5]:
			bookKey = db.Key(key)
			if bookKey.app() == "trackmybooks":
				bookKey = db.Key.from_path(*bookKey.to_path())
			book = Book.get(bookKey)
			if book: viewList.append( mapping.toReaderBookTemplate(book, None) )
	
	appendBooks(addedBooks, template_values["addedBooks"])
	appendBooks(finishedBooks, template_values["finishedBooks"])	
	appendBooks(inprogressBooks, template_values["inprogressBooks"])
	
	t = get_template('index.html')
	html = t.render(Context(template_values))
	
	return HttpResponse(html)