from django.conf.urls.defaults import *

urlpatterns = patterns(
	'',
	
	(r'^search/(?P<page>\d+)', 'views.search.find'),
	(r'^search/?', 'views.search.find'),
	
	(r'^reader/?$', 'views.reader.index'),
	(r'^reader/create$', 'views.reader.create'),
	(r'^reader/update$', 'views.reader.update'),
	(r'^reader/delete$', 'views.reader.delete'),
	
	(r'^book/isbn/(?P<isbn>\w+)/?$', 'views.readerbook.viewByIsbn'),
	(r'^book/view/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.view'),	
	(r'^book/add$', 'views.readerbook.addToReader'),
	(r'^book/delete/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.delete'),
	(r'^book/markAsFinished/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.markAsFinished'),
	(r'^book/markAsInProgress/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.markAsInProgress'),
	(r'^book/markAsTodo/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.markAsTodo'),
	(r'^book/rate/(?P<value>\d{1,1})/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.rate'),
	(r'^book/unrate/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.unrate'),
	(r'^book/saveNotes/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.saveNotes'),
	(r'^book/saveTags/(?P<identifier>[a-zA-Z0-9\-_]+)/?$', 'views.readerbook.saveTags'),
	(r'^book/ajaxAddBook/?$', 'views.readerbook.ajaxAddBook'),
	
	# bookcase and bookcase paged
	(r'^bookcase/?$', 'views.bookcase.index'),
	(r'^bookcase/(?P<page>\d+)/?$', 'views.bookcase.index'),
	(r'^bookcase/export?$', 'views.bookcase.export'),
	
	(r'^bookcase/(?P<state>(unread|inprogress|finished|unrated))/?$', 'views.bookcase.index'),
	(r'^bookcase/(?P<state>(unread|inprogress|finished|unrated))/(?P<page>\d+)/?$', 'views.bookcase.index'),
	
	
	(r'^public/(?P<username>\w+)/?$', 'views.public.index'),
	(r'^public/(?P<username>\w+)/(?P<page>\d+)/?$', 'views.public.index'),
	(r'^public/(?P<username>\w+)/(?P<state>(unread|inprogress|finished))/?$', 'views.public.index'),
	(r'^public/(?P<username>\w+)/(?P<state>(unread|inprogress|finished))/(?P<page>\d+)/?$', 'views.public.index'),
	
	(r'^tags/?$', 'views.tags.index'),
	(r'^tags/view/(?P<tag>\w+)/?$', 'views.tags.view'),
	
	(r'^calendar/?$', 'views.calendar.index'),
	(r'^layout/?$', 'views.calendar.layout'),
	
	
	(r'^test/?$', 'views.test.index'),
	(r'^testsearch/?$', 'views.test.searchTest'),
	
	(r'^conversions/setGenre$', 'conversions.setgenre.setGenre'),
	(r'^conversions/setImage$', 'conversions.setimage.setImage'),
	(r'^conversions/setPages$', 'conversions.setpages.setPages'),
	(r'^conversions/copyLists$', 'conversions.copylists.copyLists'),
	
	(r'^/?$', 'views.index.index'),
)