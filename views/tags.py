from google.appengine.ext import db

from django.shortcuts import render_to_response

from taggable import Tag
from models import Book

def index(request):

	tags = Tag.get_tags_by_frequency()
	template_values = {}
	template_values["tags"] = tags
	
	return render(template_values)

def view(request, tag):
	tag = db.get(db.Key(tag))
	books = db.get(tag.tagged)
	
	template_values = {}
	template_values["tag"] = tag
	template_values["books"] = books
	
	return render(template_values)
	
def render(template_values):
	return render_to_response('tags.html', template_values)