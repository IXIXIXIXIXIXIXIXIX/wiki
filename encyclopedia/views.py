from django.shortcuts import render

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, page_title):

	page = util.get_entry(page_title)
	
	if page:
		return render(request, "encyclopedia/display.html", {
			"page_title": page_title, "contents": markdown2.markdown(page)
		})
	else:
		return render(request, "encyclopedia/not_found.html", {
			"page_title": page_title	
		})

def search(request, page_title):
	
	page = util.get_entry(page_title)

	if page:
		return render(request, "encyclopedia/display.html", {
			"page_title": page_title, "contents": markdown2.markdown(page)
		})
	else:
		# find entries where search string is a substring and pass list of these to template
		full_list = util.list_entries()
		near_misses = []

		for entry in full_list:
			if entry.find(page_title) != -1:
				near_misses.append(entry)

		return render(request, "encyclpedia/results.html", {
			"near_misses": near_misses, "page_title": page_title
		})
