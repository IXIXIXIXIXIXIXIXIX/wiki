from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("wiki/<str:page_title>", views.display, name="display"),
	path("edit/<str:page_edit_title>", views.edit, name="edit"),
	path("search", views.search, name="search"),
	path("add", views.add, name="add"),
	path("random", views.random_page, name="random_page")
]

