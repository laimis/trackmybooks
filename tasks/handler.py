from google.appengine.ext import db
import webapp2

from models import BookList

def recordEvent(bookList, value):
	lst = bookList.list
	lst.insert(0, value)
		
	if len(lst) > 10:
		lst = lst[0:10]
	
	bookList.put()
	return ""

class BookAddedHandler(webapp2.RequestHandler):
	def post(self):
		bookList = BookList.getUnread()
		return recordEvent( bookList, self.request.get('book') )

class BookAddedToReader(webapp2.RequestHandler):
	def post(self):
		
		reader = Reader.get(self.request.get('reader'))
		book = Reader.get(self.request.get('book'))
		
		timeline = reader.timelines.all().filter('month', currentmonth)
		if timeline is None:
			timeline = Timeline(reader, currentmonth)
			reader.AddTimeline(timeline)
			
		timeline.AddBook(book)
		
class BookFinishedHandler(webapp2.RequestHandler):
	def post(self):
		bookList = BookList.getFinished()
		return recordEvent( bookList, self.request.get('book') )

class BookInprogressHandler(webapp2.RequestHandler):
	def post(self):
		bookList = BookList.getInProgress()
		return recordEvent( bookList, self.request.get('book') )

jobApp = webapp2.WSGIApplication([
    ('/tasks/bookadded', BookAddedHandler),
	('/tasks/bookfinished', BookFinishedHandler),
	('/tasks/bookinprogress', BookInprogressHandler),
  ])