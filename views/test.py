import os
import cgi 

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from taggable import Tag

def index(request):

	tags = Tag.get_tags_by_frequency()
	
	concated = ""
	
	for t in tags:
		concated += t.tag + str(t.tagged_count) + ", "
		
	return HttpResponse("So many tags! " + concated)