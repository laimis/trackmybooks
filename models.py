import datetime

from google.appengine.ext import db
from google.appengine.api import users

from taggable import Taggable

from tasks import dispatcher

class Entity(db.Model):

	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)
	def identifier(self):
		return str(self.key())

class Book(Taggable, Entity):

	def __init__(self, parent=None, key_name=None, app=None, **entity_values):
		Entity.__init__(self, parent, key_name, app, **entity_values)
		Taggable.__init__(self)
		
	title = db.StringProperty()
	author = db.StringProperty()
	isbn = db.StringProperty()
	image = db.StringProperty()
	imageLarge = db.StringProperty()
	imageSmall = db.StringProperty()
	amazonUrl = db.StringProperty()
	numberOfPages = db.IntegerProperty()
	
	def __str__(self):
		return "Book: " + self.title
	
	@staticmethod
	def byISBN(isbn):
		return Book.all().filter('isbn', isbn).get()

class Reader(Entity):

	name = db.StringProperty()
	username = db.StringProperty()
	email = db.EmailProperty()
	passwordHash = db.StringProperty()
	salt = db.StringProperty()
	
	toReadCount = db.IntegerProperty(default=0)
	finishedCount = db.IntegerProperty(default=0)
	inProgressCount = db.IntegerProperty(default=0)
	
	def getTotalByState(self, state):
		if state == 'unread':
			return self.toReadCount
		elif state == 'finished':
			return self.finishedCount
		elif state == 'inprogress':
			return self.inProgressCount
		else:
			return self.getTotal()
	
	def getTotal(self):
		return self.toReadCount + self.finishedCount + self.inProgressCount
	
	totalCount = property(getTotal)
	
	def __str__(self):
		return self.name + self.username + self.email
	
	@staticmethod
	def byCurrentUser():
		user = users.get_current_user()
		
		if not user:
			return None
		
		return Reader().all().filter('email', user.email()).get()
	
	@staticmethod
	def byUsername(username):
		return Reader().all().filter('username', username).get()

		
CONSTANT = 12

class ReaderBook(Taggable, Entity):
	
	rating = db.RatingProperty()
	reader = db.ReferenceProperty(Reader, collection_name='books')
	book = db.ReferenceProperty(Book, collection_name='readers')
	stateInternal = db.StringProperty(choices=('unread', 'inprogress', 'finished', 'noticed'))
	notes = db.TextProperty()
	inProgressDate = db.DateTimeProperty()
	finishedDate = db.DateTimeProperty()
	
	def __init__(self, parent=None, key_name=None, app=None, **entity_values):
		Entity.__init__(self, parent, key_name, app, **entity_values)
		Taggable.__init__(self)
	
	@staticmethod
	def finishedBooks(reader, fromDate = None):
		if not reader: return None
		
		return ReaderBook.all().ancestor(reader).filter('finishedDate >', fromDate).filter('stateInternal', 'finished').order('-finishedDate').fetch(1000)
		
	@staticmethod
	def byReaderAndBook(reader, book):
		if not reader: return None
		if not book: return None
		
		return ReaderBook.all().ancestor(reader).filter('book', book).get()
		
	@staticmethod
	def byReaderAndState(reader, state, page):
		
		query = ReaderBook.all().ancestor(reader)
		
		if state:
			query.filter('stateInternal =', state)
		
		query.order('-created')
		
		return query.fetch(CONSTANT, page * CONSTANT)
	
	@staticmethod
	def byReaderUnrated(reader, page):
		query = ReaderBook.all().ancestor(reader)
		
		query.filter("rating =", None)
		
		query.order('-created')
		
		return query.fetch(CONSTANT, page * CONSTANT)
	
	def getState(self):
		return self.stateInternal
	
	def setState(self, newState):
		oldState = self.stateInternal
		self.changeStateCounter(-1)
		self.stateInternal = newState
		self.changeStateCounter(+1)
	
		if newState == "unread" and not oldState:
			self.bookSetAsUnread()
		elif newState == "inprogress":
			self.bookSetAsInProgress()
		elif newState == "finished":
			self.bookSetAsFinished()
			
	def bookSetAsUnread(self):
		dispatcher.dispatchBookAdded(self.book, self.reader)
		
	def bookSetAsInProgress(self):
		if self.inProgressDate is None:
			self.inProgressDate = datetime.datetime.utcnow()
			
		dispatcher.dispatchBookInprogress(self.book, self.reader)
	
	def bookSetAsFinished(self):
		if self.finishedDate is None:
			self.finishedDate = datetime.datetime.utcnow()
		
		dispatcher.dispatchBookFinished(self.book, self.reader)
	
	def changeStateCounter(self, op):
		if self.state == 'finished':
			self.reader.finishedCount = self.reader.finishedCount + op
		elif self.state == 'inprogress':
			self.reader.inProgressCount = self.reader.inProgressCount + op
		elif self.state == 'unread':
			self.reader.toReadCount = self.reader.toReadCount + op
			
	def put(self):
		self.reader.put()
		
		super(Entity, self).put()
	
	def delete(self):
		self.state = ''
		self.reader.put()
		
		super(Entity, self).delete()
	
	state = property(getState, setState)


class Timeline(db.Model):

	reader = db.ReferenceProperty(Reader)

	
class TimelineMonth(db.Model):
	
	month = db.DateProperty()
	count = db.IntegerProperty()
	timeline = db.ReferenceProperty(Timeline)
	

BOOK_LIST_UNREAD = 'booklist:unread'
BOOK_LIST_FINISHED = 'booklist:finished'
BOOK_LIST_PROGRESS = 'booklist:inprogress'

	
class BookList(Entity):
	
	name = db.StringProperty()
	list = db.StringListProperty()

	@staticmethod
	def getUnread():
		booklist = BookList.get_by_key_name(BOOK_LIST_UNREAD)
		if booklist is None : BookList.createUnread([])
		return booklist
	
	@staticmethod
	def createUnread(list):
		BookList.createList(BOOK_LIST_UNREAD, list)
	
	@staticmethod
	def getFinished():
		booklist = BookList.get_by_key_name(BOOK_LIST_FINISHED)
		if booklist is None : BookList.createFinished([])
		return booklist
		
	@staticmethod
	def createFinished(list):
		BookList.createList(BOOK_LIST_FINISHED, list)
		
	@staticmethod
	def getInProgress():
		booklist = BookList.get_by_key_name(BOOK_LIST_PROGRESS)
		if booklist is None : BookList.createInProgress([])
		return booklist
		
	@staticmethod
	def createInProgress(list):
		BookList.createList(BOOK_LIST_PROGRESS, list)
		
	@staticmethod
	def createList(key, list):
		booklist = BookList(key_name=key)
		booklist.list = list
		booklist.put()