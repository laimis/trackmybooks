function BookController()
{
}

BookController.prototype.toggleNotes = function() {
	var n = $("#notes");
	var s = $("#saveLink");
	
	n.toggle();
	s.toggle();
	
	if (n.css("display") != "none") {
		n.focus();
	}
}

BookController.prototype.saveNotes = function(identifier) {
	
	var url = '/book/saveNotes/' + identifier;
	
	var statusLabel = $("#statusLabel");
	
	statusLabel.hide();
	
	$.post(url, {notes:$("#notes").val()}, this.successSaveNotes );
	
	statusLabel.show();
	statusLabel.text("saving...");
}

BookController.prototype.successSaveNotes = function(data, statusText) {
	var statusLabel = $("#statusLabel");
	
	if (statusText == "success") {
		statusLabel.show();
		statusLabel.text("(saved)");
		statusLabel.fadeOut(2000);
	} else {
		statusLabel.text("Failed to save, try again (" + statusText + ")");
	}
}

BookController.prototype.saveTags = function(identifier) {
	
	var url = '/book/saveTags/' + identifier;
	
	var statusLabel = $("#statusLabel")
	
	statusLabel.hide();
	
	var tagsValue = $("#tags").val()
	$.post(url, {tags:tagsValue}, this.successSaveTags);
	
	statusLabel.show();
	statusLabel.text("saving...");
}

BookController.prototype.successSaveTags = function(data, statusText) {
	var label = $("#statusLabel");
	
	if (statusText == "success") {
		label.show();
		label.text("(saved)");
		label.fadeOut(2000);
	} else {
		label.text("Failed to save, try again (" + statusText + ")");
	}
}