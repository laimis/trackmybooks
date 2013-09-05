import urllib2
import urllib
import os

from google.appengine.api import users
from google.appengine.ext import db

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template.loader import get_template
from django.template import Context

from models import Reader
from models import ReaderBook

import re

def update(request):
	return create(request)
	
def create(request):
	
	user = users.get_current_user()
	
	if not user:
		HttpResponseRedirect('/reader/')
	
	username = request.POST["username"]
	
	if not re.match(r"^\w{4,16}$", username):
		return index(request, "Username can contain only letters and digits, 4-16 characters long")
		
	r = Reader.byCurrentUser()
	
	if not r:
		r = Reader()
	
	r.name = request.POST["name"]
	r.username = username
	r.email = user.email()
	r.id = user.user_id()
	
	r.put()
	
	return HttpResponseRedirect('/reader')
	
def delete(request):
	
	r = Reader.byCurrentUser()
	
	if r:
		list = ReaderBook.all(keys_only = True).ancestor(r).fetch(1000)
		db.delete(list)
		r.delete()
	else:
		return HttpResponseRedirect('/')
	
	return HttpResponse(
		render('reader_delete_confirm.html', None)
	)
	
def index(request, error = None):
	
	user = users.get_current_user()
	loginUrl = users.create_login_url('/reader')
	
	if not user:
		return HttpResponseRedirect(loginUrl)
		
	r = Reader.byCurrentUser()
	
	if not r:
		r = Reader()
	
		template_values = {
			"isLoggedIn" : True,
			"isNew" : True,
			"name" : "",
			"username" : user.nickname(),
			"email" : user.email()
		}
	else:
		template_values = {
			"isLoggedIn" : True,
			"isNew" : False,
			"name" : r.name,
			"username" : r.username,
			"email" : r.email
		}
	
	template_values["logoutUrl"] = users.create_logout_url("/")
		
	if error:
		template_values["errorMsg"] = error
	
	html = render('reader.html', template_values)
		
	return HttpResponse(html)

def render(template, template_values):
	t = get_template(template)
	return t.render(Context(template_values))