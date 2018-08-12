import logging

import urllib
from google.appengine.api import urlfetch

import json

class SearchResults:
	pass

class SearchResult:
	def __init__(self):
		self.isbn = ""
		self.detailUrl = ""
		self.author = ""
		self.title = ""
		self.image = ""

class GoogleBooks:
	
	def __init__(self):
		self.key = ""

	def search(self, q, page=1):
		
		escapedQ = urllib.quote(q)
		
		url = "https://www.googleapis.com/books/v1/volumes?q={0}&country=US".format(escapedQ)

		fetchResult = urlfetch.fetch(url)

		if fetchResult.status_code != 200:
			logging.error("fetch result returned: " + fetchResult.content)
			return

		response = json.loads(fetchResult.content)

		results = SearchResults()
			
		results.TotalResults = response["totalItems"]
			
		results.items = []
			
		for item in response["items"]:
			
			result = self.createResult(item["volumeInfo"])
			results.items.append(result)
			
		return results
		
	def getBookByIsbn(self, isbn):
		
		results = self.search("isbn:" + isbn)
		
		if len(results.items) == 0:
			return None
			
		return results.items[0]

	def createResult(self, item):
		
		result = SearchResult()

		for i in item["industryIdentifiers"]:
			if i["type"] == "ISBN_10":
				result.isbn = i["identifier"]
				break
		
		result.detailUrl = item["infoLink"]
		result.author = ", ".join(item["authors"])
		result.title = item["title"]
		result.image = item["imageLinks"]["thumbnail"]
		result.imageSmall = item["imageLinks"]["smallThumbnail"]
		result.imageLarge = item["imageLinks"]["thumbnail"]

		if "categories" in item:
			result.genre = ",".join(item["categories"])
		else:
			result.genre = None

		result.numberOfPages = item["pageCount"]
		
		return  result