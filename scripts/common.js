function submitRating(value, identifier)
{ 
	if (value)
		url = '/book/rate/' + value + '/' + identifier
	else
		url = '/book/unrate/' + identifier
		
	$.post(url);
}