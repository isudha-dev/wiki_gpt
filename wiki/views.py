import wikipediaapi

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wiki.constants import SUCCESS, ERROR, DATA


@api_view(["GET"])
def get_wiki_page(request):
    search_text = request.GET.get("title")
    if not search_text:
        response = {SUCCESS: False, ERROR: "Invalid page title"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    wiki_wiki = wikipediaapi.Wikipedia('Wiki summary', 'en')
    page_py = wiki_wiki.page(search_text)
    if not page_py.exists():
        response = {SUCCESS: False, ERROR: "Could not find wiki page with the given search text."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    section_titles = []
    for section in page_py.sections:
        section_titles.append(section.title)

    response = {
        SUCCESS: True,
        DATA: {
            "title": page_py.title,
            "full_url": page_py.fullurl,
            "sections": section_titles
        }
    }
    return Response(response, status=status.HTTP_200_OK, content_type="application/json")
