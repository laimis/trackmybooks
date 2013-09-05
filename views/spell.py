from google.appengine.api import urlfetch

def checkSpelling(word):
	url = "https://www.google.com/tbproxy/spell?lang=en&hl=en";
	
	header = {
		"MIME-Version" : "1.0",
		"Content-type" : "application/xml",
        "Content-length" : len(xml)
                $header .= "Content-transfer-encoding: text \r\n";
                $header .= "Request-number: 1 \r\n";
                $header .= "Document-type: Request \r\n";
                $header .= "Interface-Version: Test 1.4 \r\n";
                $header .= "Connection: close \r\n\r\n";
	}
	result = urlfetch.fetch(url)
