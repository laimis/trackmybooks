from google.appengine.ext.webapp import template

from django.http import HttpResponse	
from django.template.loader import get_template
from django.template import Context

from googlebooks import GoogleBooks

from models import Reader
from helpers import paging

def find(request, keyword = "", page = 1):
	
	page = int(page)
	
	if "keywords" in request.GET:
		keyword = request.GET["keywords"]
	
	results = []
	
	if keyword:
		results = GoogleBooks().search(keyword, page)
		
		template_values = {
			'totalResults': results.TotalResults,
			'results': results.items,
			'keywords' : keyword
		}
		
		paging.preparePagingTemplateForSearch(template_values, page, results.TotalResults)
		
	else:
		template_values = {}
		
	if Reader.byCurrentUser():
		template_values["isLoggedIn"] = True
	
	# load template
	t = get_template('searchresults.html')
	html = t.render(Context(template_values))
	
	return HttpResponse(html)