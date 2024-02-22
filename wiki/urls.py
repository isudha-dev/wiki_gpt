from django.urls import path

from wiki.views import get_wiki_sections, summarise, paraphrase, index

urlpatterns = [
    path("", index, name="index"),
    path("page/", get_wiki_sections, name="get_wiki_sections"),
    path("page/section/summarise/", summarise, name="summarise"),
    path("page/section/paraphrase/", paraphrase, name="paraphrase"),
]
