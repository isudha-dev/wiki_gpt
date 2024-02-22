import wikipediaapi

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wiki.constants import SUCCESS, ERROR, DATA


page_cache = {}


def get_wiki_page(page_title):
    if not page_cache.get(page_title):
        wiki_wiki = wikipediaapi.Wikipedia('Wiki summary', 'en')
        wiki_page = wiki_wiki.page(page_title)
        if not wiki_page.exists():
            return

        page_cache[wiki_page.title] = wiki_page
        return wiki_page

    return page_cache[page_title]


@api_view(["GET"])
def get_wiki_sections(request):
    page_title = request.GET.get("page_title")
    if not page_title:
        response = {SUCCESS: False, ERROR: "Invalid page title."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    wiki_page = get_wiki_page(page_title)
    if not wiki_page:
        response = {SUCCESS: False, ERROR: "This page does not exists."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    section_titles = []
    for section in wiki_page.sections:
        section_titles.append(section.title)

    response = {
        SUCCESS: True,
        DATA: {
            "page_title": wiki_page.title,
            "full_url": wiki_page.fullurl,
            "sections": section_titles
        }
    }
    return Response(response, status=status.HTTP_200_OK, content_type="application/json")
