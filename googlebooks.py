import logging

import urllib
from google.appengine.api import urlfetch

import json

NO_IMAGE_URL = "/static/images/nopicture.jpg"

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
		
		if "items" in response:
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

		if "authors" in item:
			result.author = ", ".join(item["authors"])
		else:
			result.author = None

		result.title = item["title"]

		if "imageLinks" in item:
			result.image = item["imageLinks"]["thumbnail"]
			result.imageSmall = item["imageLinks"]["smallThumbnail"]
			result.imageLarge = item["imageLinks"]["thumbnail"]
		else:
			result.image = NO_IMAGE_URL
			result.imageSmall = NO_IMAGE_URL
			result.imageLarge = NO_IMAGE_URL

		if "categories" in item:
			result.genre = ",".join(item["categories"])
		else:
			result.genre = ""

		if "pageCount" in item:
			result.numberOfPages = item["pageCount"]
		else:
			result.numberOfPages = None
		
		return  result