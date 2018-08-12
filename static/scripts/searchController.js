function SearchController()
{
}

SearchController.prototype.addBook = function(isbn, state) {
	var url = '/book/ajaxAddBook';
	
	$.post(url, {"isbn":isbn, "state":state}, function(data, statusText){searchController.successAddBook(data, statusText, isbn);});
	
	var statusLabel = $("#addStatus" + isbn)
	statusLabel.text("adding... please wait");
}

SearchController.prototype.successAddBook = function(data, statusText, isbn) {
	var statusLabel = $("#addStatus" + isbn)
	
	if (statusText == "success") {
		statusLabel.text("done.")
	} else {
		statusLabel.text("Failed to add, try again (" + statusText + ")");
	}
}
