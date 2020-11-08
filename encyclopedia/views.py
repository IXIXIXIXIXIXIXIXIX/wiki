from django.shortcuts import render, redirect
from django import forms
from . import util

import random
import markdown2

class NewEntryForm(forms.Form):
	page_title = forms.CharField(label="New Page Title")
	page_content = forms.CharField(label="Entry Content", widget=forms.Textarea)

class EditEntryForm(forms.Form):
	page_content = forms.CharField(label="Edit Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, page_title):

	# Find requested page
	page = util.get_entry(page_title)
	
	# If page exists, render it; if not, render error page
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
		
		# Get user input from form
		page_title = request.POST.get("q")
		page = util.get_entry(page_title)

		# Check if page exists and if so, render it
		if page:
			return render(request, "encyclopedia/display.html", {
				"page_title": page_title, "contents": markdown2.markdown(page)
			})
		else:
			# Find entries where search string is a substring and pass list of these to template
			full_list = util.list_entries()
			near_misses = []

			for entry in full_list:
				if entry.find(page_title) != -1:
					near_misses.append(entry)

			return render(request, "encyclopedia/results.html", {
				"near_misses": near_misses, "page_title": page_title
			})
	else:
		# Program flow should never usually reach this point
		return render(request, "encyclopedia/index.html", {
			"entries": util.list_entries()
		})

def add(request):

	if request.method == "POST":
		
		# Check form is valid and get submitted data if so
		form = NewEntryForm(request.POST)
		if form.is_valid():
			new_title = form.cleaned_data["page_title"]
			
			# Check if proposed page already exists
			page_exists = util.get_entry(new_title)
			if page_exists:
				return render(request, "encyclopedia/page_exists.html", {
					"page_title": new_title
				})

			# Save new entry
			new_content = form.cleaned_data["page_content"]
			util.save_entry(new_title, new_content)

			# Redirect to new page
			return redirect("display", new_title)
	else:
		return render(request, "encyclopedia/add.html", {
			"form": NewEntryForm()
		})

def edit(request, page_edit_title):

	if request.method == "POST":
		
		# Check form is valid and get submitted data if so
		form = EditEntryForm(request.POST)
		if form.is_valid():
			new_content = form.cleaned_data["page_content"]
			

			util.save_entry(page_edit_title, new_content)

			# Redirect to new page
			return redirect("display", page_edit_title)
	else:

		# Find requested page
		page = util.get_entry(page_edit_title)
	
		# If page exists, render edit page, otherwise render error page
		if page:
			edit_form = EditEntryForm(initial={"page_content": page})
			return render(request, "encyclopedia/edit.html", {
				"page_title": page_edit_title, "form": edit_form
			})
		else:
			return render(request, "encyclopedia/not_found.html", {
				"page_title": page_edit_title	
			})

def random_page(request):
	
	# Get a list of all entries then choose one at random
	all_entries  = util.list_entries()
	random_entry = random.choice(all_entries)

	# Redirect to chosen entry
	return redirect("display", random_entry)
