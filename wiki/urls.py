from django.urls import path

from wiki.views import get_wiki_sections, status

urlpatterns = [
    path("page/", get_wiki_sections, name="get_wiki_sections")
]
