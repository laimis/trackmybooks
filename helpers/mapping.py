import urllib
from datetime import datetime

def toReaderBookTemplate(book, readerBook):
	template_values = {
		"title" : book.title,
		"detailUrl" : book.amazonUrl,
		"isbn" : book.isbn,
		"author" : book.author,
		"image" : book.image,
		"imageSmall" : book.imageSmall,
		"imageLarge" : book.imageLarge,
		"numberOfPages" : book.numberOfPages,
		"identifier" : book.identifier(),
		"bookSearchTerm" : urllib.quote_plus(book.title),
		"bookTags_string" : book.tags_string()
	}
	
	if readerBook:
		template_values["state"] = readerBook.state
		template_values["rating"] = readerBook.rating
		template_values["notes"] = readerBook.notes
		template_values["hasReader"] = True
		template_values["inProgressDate"] = readerBook.inProgressDate
		template_values["finishedDate"] = readerBook.finishedDate
		template_values["addedDate"] = readerBook.created
		template_values["mostRecentDate"] = max([readerBook.inProgressDate or datetime.min, readerBook.finishedDate or datetime.min, readerBook.created or datetime.min])
		template_values["tags_string"] = readerBook.tags_string()
	return template_values