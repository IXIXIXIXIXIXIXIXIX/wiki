from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("wiki/<str:page_title>", views.display, name="display"),
	path("search", views.search, name="search"),
	path("add", views.add, name="add"),
	path("edit/<str:page_title>", views.edit, name="edit")
]
