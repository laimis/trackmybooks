import logging

class ExceptionHandler:

	def process_exception(self, request, exception):
		logging.error(exception)