from django.urls import path

from wiki.views import get_wiki_page

urlpatterns = [
    path("page/", get_wiki_page, name="get_wiki_page"),
]