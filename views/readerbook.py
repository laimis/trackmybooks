import os
import cgi 

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from models import Book
from models import ReaderBook
from models import Reader
from tasks import dispatcher
from googlebooks import GoogleBooks
from helpers import mapping

def view(request, identifier):

	book = db.get(db.Key(identifier))
	readerBook = ReaderBook.byReaderAndBook(Reader.byCurrentUser(), book)
	
	return render( mapping.toReaderBookTemplate(book, readerBook) )

def viewByIsbn(request, isbn = ""):
	
	user = users.get_current_user()
	reader = None
	book = None
	readerBook = None
	
	if user:
		reader = Reader.byCurrentUser()
	
	book = fetchCreateByISBN(isbn, invokeSearchByIsbn, True)
	
	readerBook = ReaderBook.byReaderAndBook(reader, book)
		
	template_values = mapping.toReaderBookTemplate(book, readerBook)
	
	if not user:
		template_values["loginUrlToAdd"] = users.create_login_url('/book/isbn/' + isbn)
	else:
		if not reader:
			template_values["signupUrl"] = '/reader'
	
	return render(template_values)

def invokeSearchByIsbn(isbn):
	return GoogleBooks().getBookByIsbn(isbn)

def delete(request, identifier):
	book = Book().get(identifier)
	readerBook = ReaderBook().byReaderAndBook(Reader.byCurrentUser(), book)
	
	readerBook.delete()
	
	return HttpResponseRedirect('/')

class SearchResult:
	pass
	
def addToReader(request):
	
	reader = Reader.byCurrentUser()
	if not reader:
		return HttpResponseRedirect('/')

	bookResult = SearchResult()
	bookResult.isbn = request.POST["isbn"]
	bookResult.detailUrl = request.POST["detailUrl"]
	bookResult.author = request.POST["author"]
	bookResult.title = request.POST["title"]
	bookResult.image = request.POST["image"]
	bookResult.imageSmall = request.POST["imageSmall"]
	bookResult.imageLarge = request.POST["imageLarge"]
	bookResult.numberOfPages = int(request.POST["numberOfPages"])
	
	book = fetchCreateByISBN(request.POST["isbn"], bookResult, False)
	
	createReaderBookIfNecessary(reader, book, 'unread')
	
	return redirectToBook(book)

def createReaderBookIfNecessary(reader, book, state):
	readerBook = ReaderBook.byReaderAndBook(reader, book)
	
	if not readerBook:
		readerBook = ReaderBook(parent=reader)
		readerBook.reader = reader
		readerBook.book = book
	
	readerBook.state = state
	readerBook.put()

def fetchCreateByISBN(isbn, dataSource, needInvoke):
	book = Book.byISBN(isbn)
	
	if needInvoke: dataSource = dataSource(isbn)
	
	if not book:
		book = Book()
		
		book.title = dataSource.title
		book.author = dataSource.author
		book.isbn = dataSource.isbn
		book.image = dataSource.image
		book.imageSmall = dataSource.imageSmall
		book.imageLarge = dataSource.imageLarge
		book.amazonUrl = dataSource.detailUrl
		book.numberOfPages = dataSource.numberOfPages
		
		book.put()
		
		book.tags = dataSource.genre
	
	return book

def markAsFinished(request, identifier):
	book = Book().get(db.Key(identifier))
	readerBook = ReaderBook.byReaderAndBook(Reader.byCurrentUser(), book)
	readerBook.state = 'finished'
	readerBook.put()
	
	return redirectToBook(book)
	
def markAsInProgress(request, identifier):
	book = Book().get(db.Key(identifier))
	readerBook = ReaderBook.byReaderAndBook(Reader.byCurrentUser(), book)
	readerBook.state = 'inprogress'
	readerBook.put()
	
	return redirectToBook(book)
	
def markAsTodo(request, identifier):
	book = Book().get(db.Key(identifier))
	readerBook = ReaderBook.byReaderAndBook(Reader.byCurrentUser(), book)
	readerBook.state = 'unread'
	readerBook.put()
	
	return redirectToBook(book)

def ajaxAddBook(request):
	reader = Reader.byCurrentUser()
	if not reader:
		return HttpResponse("Login or create account to add books")
	
	book = fetchCreateByISBN(request.POST["isbn"], invokeAmazonSearchByIsbn, True)
	
	createReaderBookIfNecessary(reader, book, request.POST["state"])
	
	return HttpResponse("success")
	
def rate(request, value, identifier):
	val = int(value)
	if val < 1  or val > 5:
		raise Exception('invalid value')
	
	readerBook = getCurrentUserBook(identifier)
	readerBook.rating = val
	readerBook.put()
	
	return HttpResponse("success")

def unrate(request, identifier):
	readerBook = getCurrentUserBook(identifier)
	readerBook.rating = None
	readerBook.put()
	
	return HttpResponse("success")
	
def saveNotes(request, identifier):
	readerBook = getCurrentUserBook(identifier)
	readerBook.notes = cgi.escape(request.POST["notes"])
	readerBook.put()
	
	return HttpResponse("success")

def saveTags(request, identifier):
	readerBook = getCurrentUserBook(identifier)
	readerBook.tags = cgi.escape(request.POST["tags"])
	readerBook.put()
	
	return HttpResponse("success")
	
def getCurrentUserBook(identifier):
	return ReaderBook.byReaderAndBook(Reader.byCurrentUser(), db.Key(identifier))
	
def render(template_values):
	return render_to_response('book.html', template_values)
	
def redirectToBook(book):
	return HttpResponseRedirect('/book/view/' + book.identifier())