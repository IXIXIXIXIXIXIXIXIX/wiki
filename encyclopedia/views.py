from django.shortcuts import render
from django import forms
from . import util

import markdown2

class NewEntryForm(forms.Form):
	page_title = forms.CharField(label="New Page Title")
	page_content = forms.Charfield(label="Entry", widget=forms.Textarea)

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

def search(request):
	
	if request.method == "POST":
		page_title = request.POST.get("q")
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

			return render(request, "encyclopedia/results.html", {
				"near_misses": near_misses, "page_title": page_title
			})
	else:
		# Program flow should never usually reach this point.
    	return render(request, "encyclopedia/index.html", {
			"entries": util.list_entries()
		})

def add(request):

	if request.method == "POST":

	else:
		return render(request, "add.html"
