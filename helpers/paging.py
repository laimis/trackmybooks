def preparePagingTemplateForBookcase(template_values, reader, state, page):
	totalByState = reader.getTotalByState(state)
	template_values["currentPage"] = page
	template_values["currentStateTotal"] = totalByState
	template_values["showPaging"] = True
	template_values["isAtFirstPage"] = page == 1
	template_values["maxPages"] = totalByState / 12
	if totalByState % 12: template_values["maxPages"] = template_values["maxPages"] + 1
	
	template_values["nextPage"] = page + 1
	
	if page > 1: 
		template_values["prevPage"] = page - 1
	else:
		template_values["prevPage"] = 1
	
	if page < template_values["maxPages"]:
		template_values["nextPage"] = page + 1
	else:
		template_values["nextPage"] = page
			
	if state:
		template_values["currentStateForPaging"] = state + "/"
	else:
		template_values["currentStateForPaging"] = ""

def preparePagingTemplateForSearch(template_values, page, total):
	total = int(total)
	template_values["currentPage"] = page
	template_values["total"] = total
	template_values["showPaging"] = total > 10
	template_values["isAtFirstPage"] = page == 1
	template_values["maxPages"] = total / 10
	if total % 10: template_values["maxPages"] = template_values["maxPages"] + 1
	
	template_values["nextPage"] = page + 1
	
	if page > 1: 
		template_values["prevPage"] = page - 1
	else:
		template_values["prevPage"] = 1
	
	if page < template_values["maxPages"]:
		template_values["nextPage"] = page + 1
	else:
		template_values["nextPage"] = page