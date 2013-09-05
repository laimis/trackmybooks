import logging

import urllib
from google.appengine.api import urlfetch

from xml.dom import minidom
from sets import Set

import hmac, base64, hashlib
import datetime

class SearchResults:
	pass

class SearchResult:
	def __init__(self):
		self.isbn = ""
		self.detailUrl = ""
		self.author = ""
		self.title = ""
		self.image = ""

class AmazonInterface:
	
	def __init__(self):
		self.secretKey = "HMWW6RQ4i03mD6oRpBr3gX1aCNAgrzmfZWj3ltug"
		self.awsAccessKey = "14XY5XMAJ7BFFMAX9Z02"
		self.responseGroup = urllib.quote("Small,Images,BrowseNodes,ItemAttributes")
	
	def searchXml(self, keyword, page):
		
		keyword = urllib.quote(keyword)
		page = str(page)
		ts = getTimestamp()
		
		dict = {"ItemPage" : page, "Keywords" : keyword, "Operation" : "ItemSearch", "SearchIndex" : "Books", "Timestamp" : ts}
		
		url = self.createUrl(dict)
		
		return urlfetch.fetch(url)

	def searchByPrice(self, keyword, price):
		
		result = self.searchXml(keyword, 1, price)
		
		return self.xmlToResults(result)
		
		
	def search(self, keyword, page):
		
		result = self.searchXml(keyword, page)
		
		return self.xmlToResults(result)
	
	def xmlToResults(self, resultsXml):
		
		# try:
			
			# return result.content
			
			xmldoc = minidom.parseString(resultsXml.content)
					
			results = SearchResults()
			
			results.TotalResults = getText(xmldoc.getElementsByTagName('TotalResults'))
			
			results.items = []
			
			for item in xmldoc.getElementsByTagName('Item'):
				
				result = self.createResult(item)
				results.items.append(result)
				
			return results
		# except:
			# logging.error("Failed in search, url: " + url)
			# raise

	
	def getBookByIsbnXml(self, isbn):
		
		ts = getTimestamp()
		
		dict = {"ItemId" : isbn, "Operation" : "ItemLookup", "Timestamp" : ts}
		
		url = self.createUrl(dict)
		
		# try:
		return urlfetch.fetch(url)
		
		
	def getBookByIsbn(self, isbn):
		
		result = self.getBookByIsbnXml(isbn)
		
		xmldoc = minidom.parseString(result.content)
				
		items = xmldoc.getElementsByTagName('Item')
		
		if len(items) == 0:
			return None
			
		return self.createResult(items[0])
				
		# except:
			# logging.error("Failed in bookByIsbn, url: " + url)
			# return "error1"
	
	
	def createUrl(self, dict):
		
		# global params
		dict["AWSAccessKeyId"] = self.awsAccessKey
		dict["ResponseGroup"] = self.responseGroup
		dict["Service"] = "AWSECommerceService"
		dict["AssociateTag"] = "trmybo-20"
		
		paramsList = []
		
		map(lambda k: paramsList.append(k + "=" + dict[k]), sorted(dict.keys()))
		
		return "http://ecs.amazonaws.com/onca/xml?" + "&".join(paramsList) + "&Signature=" + self.createSignatureString(paramsList)
		
		
	def createSignatureString(self, paramsList):
	
		stringToSign = "GET\necs.amazonaws.com\n/onca/xml\n" + "&".join(paramsList)
		
		return generateSignature(self.secretKey, stringToSign)
	
	
	def createResult(self, item):
		
		result = SearchResult()
		result.isbn = getText(item.getElementsByTagName('ASIN'))
		result.detailUrl = getText(item.getElementsByTagName('DetailPageURL'))
		result.author = getText(item.getElementsByTagName('Author'))
		result.title = getText(item.getElementsByTagName('Title'))
		result.image = extractImage(item, "MediumImage")
		result.imageSmall = extractImage(item, "SmallImage")
		result.imageLarge = extractImage(item, "LargeImage")
		result.genre = getGenre(item)
		result.numberOfPages = extractNumberOfPages(item)
		
		return  result

def extractNumberOfPages(item):

	itemAttributes = item.getElementsByTagName("ItemAttributes")
	pagesText = getText(itemAttributes[0].getElementsByTagName("NumberOfPages"))
	
	if pagesText:
		return int(pagesText)
	
	return None
	
def getGenre(item):
	
	browseNodes = item.getElementsByTagName("BrowseNode")
	
	prevNode = None
	booksList = []
	subjectsList = []
	for node in browseNodes:
		name = getText(node.getElementsByTagName("Name"))
		if name == "Subjects" and prevNode:
			subjectsList.append(getText(prevNode.getElementsByTagName("Name")))
		if name == "Books" and prevNode:
			booksList.append(getText(prevNode.getElementsByTagName("Name")))
		prevNode = node
	
	if subjectsList: return ",".join(list(Set(subjectsList)))
	if booksList : return ",".join(list(Set(booksList)))
	
	return "NotFound"
	
def extractImage(item, imageType):
	imageTag = item.getElementsByTagName(imageType)
			
	if imageTag:
		return getText(item.getElementsByTagName(imageType)[0].getElementsByTagName('URL'))
	else:
		return None

def getText(nodelist):
	if len(nodelist) == 0:
		return ""
	nodelist = nodelist[0].childNodes
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc = rc + node.data
	return rc
	
def generateSignature(secretKey, stringToSign):
	digest = hmac.new(secretKey, stringToSign, hashlib.sha256).digest()
		
	return urllib.pathname2url(base64.b64encode(digest, None))

def getTimestamp():
	return urllib.quote(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))