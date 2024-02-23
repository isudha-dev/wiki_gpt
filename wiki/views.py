import os
import wikipediaapi

from openai import OpenAI
from rest_framework.decorators import api_view
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from wiki.constants import SUCCESS, ERROR, DATA, PAGE_SECTION_CACHE_KEY

page_cache = {}
page_section_summary_cache = {}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
summary_prompt = ("You are a highly skilled AI trained in language comprehension and summarising. I would like you to "
                  "read the following text and summarise it so that anyone can easily understand it. Aim to retain "
                  "the most important points, providing a coherent and readable summary that could help a person "
                  "understand the main points of the discussion without needing to read the entire text. Please avoid "
                  "unnecessary details or tangential points.")
paraphrase_prompt = ("You are a highly skilled AI trained in language comprehension and paraphrasing. I would like you "
                     "to read the following text and paraphrase it so that anyone can easily understand it. Aim to "
                     "retain the most important points, providing a coherent and readable summary that could help a "
                     "person understand the main points of the discussion without needing to read the entire text. "
                     "Please avoid unnecessary details or tangential points and respond in a funny manner.")


def get_wiki_page(page_title):
    if not page_cache.get(page_title):
        wiki_wiki = wikipediaapi.Wikipedia('Wiki summary', 'en')
        wiki_page = wiki_wiki.page(page_title)
        if not wiki_page.exists():
            return

        page_cache[wiki_page.title] = wiki_page
        return wiki_page

    return page_cache[page_title]


def get_wiki_page_section_summary(wiki_page, section_title, section_text):
    cache_key = PAGE_SECTION_CACHE_KEY.format(wiki_page.title, section_title)
    if not page_section_summary_cache.get(cache_key):
        summary = get_text_completions(summary_prompt, section_text)
        page_section_summary_cache[cache_key] = summary

    return page_section_summary_cache[cache_key]


def get_text_completions(prompt, text):
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return summary_response.choices[0].message.content


def get_summary_paraphase(page_title, section_title, operation):
    wiki_page = get_wiki_page(page_title)
    sections = get_sections(wiki_page)

    section_text = ""
    for section in sections:
        if section["title"] == section_title:
            section_text = section["text"]
            break

    section_summary = get_wiki_page_section_summary(wiki_page, section_title, section_text)

    for section in sections:
        if section["title"] == section_title:
            if operation == "summarise":
                section["summary"] = section_summary
            else:
                section["summary"] = section_summary
                section["paraphrase"] = get_text_completions(paraphrase_prompt, section_summary)

    response = {
        SUCCESS: True,
        DATA: {
            "page_title": wiki_page.title,
            "full_url": wiki_page.fullurl,
            "sections": sections,
            "section_title": section_title,
        }
    }

    return response


def index(request):
    return render(request, "wiki/index.html")


def get_sections(wiki_page):
    sections = []

    for section in wiki_page.sections:
        section_dict = {"title": section.title, "text": section.text}

        if not section.text:
            section_text = ""
            for subsection in section.sections:
                section_text = "{0}\n\n{1}\n\n{2}".format(section_text, subsection.title, subsection.text)

            section_dict["text"] = section_text

        sections.append(section_dict)

    return sections


@extend_schema(
    description="Wikipedia API to get wiki page for searched title and load page sections",
    parameters=[
        OpenApiParameter(name='page_title', description='Page title to search', type=str,
                         default="Python (programming language)"),
    ],
)
@api_view(["GET"])
def get_wiki_sections(request):
    page_title = request.GET.get("page_title")

    if not page_title:
        response = {SUCCESS: False, ERROR: ""}
        return render(request, "wiki/index.html", response)

    wiki_page = get_wiki_page(page_title)
    if not wiki_page:
        response = {
            DATA: {"page_title": page_title},
            SUCCESS: False,
            ERROR: f"Could not find any wiki page with title '{page_title}'"
        }
        return render(request, "wiki/index.html", response)

    response = {
        SUCCESS: True,
        DATA: {
            "page_title": wiki_page.title,
            "full_url": wiki_page.fullurl,
            "sections": get_sections(wiki_page),
        }
    }
    return render(request, "wiki/index.html", response)


@extend_schema(
    description="Summarises selected section",
    parameters=[
        OpenApiParameter(name='page_title', description='Searched page title', type=str,
                         default="Python (programming language)"),
        OpenApiParameter(name='section_title', description='Section to summarise', type=str, default="History"),
    ],
)
@api_view(["GET"])
def summarise(request):
    page_title = request.GET.get("page_title")
    section_title = request.GET.get("section_title")

    summary = get_summary_paraphase(page_title, section_title, "summarise")
    return render(request, "wiki/index.html", summary)


@extend_schema(
    description="Paraphrases selected summary",
    parameters=[
        OpenApiParameter(name='page_title', description='Searched page title', type=str,
                         default="Python (programming language)"),
        OpenApiParameter(name='section_title', description='Section to summarise', type=str, default="History"),
    ],
)
@api_view(["GET"])
def paraphrase(request):
    page_title = request.GET.get("page_title")
    section_title = request.GET.get("section_title")

    summary_paraphrase = get_summary_paraphase(page_title, section_title, "paraphrase")
    return render(request, "wiki/index.html", summary_paraphrase)
