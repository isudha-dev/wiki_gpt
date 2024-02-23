# Introduction
This project involve using the Wikipedia API to access content from a specific Wikipedia page and then applying OpenAI's GPT-3.5 Turbo for summarization and paraphrasing.


APIs:
-----------
1. For getting wiki page sections.
```http
GET /wiki/page/?page_title=Python(ProgrammingLanguage)
```
| Parameter | Type | Description                                   |
| :--- | :--- |:----------------------------------------------|
| `page_title` | `string` | **Required**. Page title you want to search on wiki |

2. For getting summary of selected section.
```http
GET /wiki/page/?page_title=Python(ProgrammingLanguage)&section_title=History
```
| Parameter       | Type | Description                                         |
|:----------------| :--- |:----------------------------------------------------|
| `page_title`    | `string` | **Required**. Page title you want to search on wiki |
| `section_title` | `string` | **Required**. Section title you want to summarize   |

3. For getting paraphrase of selected summary. User can paraphase a summary multiple times to see different responses.
```http
GET /wiki/page/?page_title=Python(ProgrammingLanguage)&section_title=History
```
| Parameter       | Type | Description                                                              |
|:----------------| :--- |:-------------------------------------------------------------------------|
| `page_title`    | `string` | **Required**. Page title you want to search on wiki                      |
| `section_title` | `string` | **Required**. Section title for which you want to paraphrase its summary |


Requirements
------------
- Python = 3.9 
- wikipedia-api = 0.6.0 
- djangorestframework = 3.14.0 
- Django = 4.2.10 
- openai = 1.12.0 
- drf-spectacular = 0.27.1
  
Installation
------------
Install using 

    $ pip install -r requirements.txt

or

    $ python3 -m pip install -r requirements.txt

Possible future enhancements
----------------------------
1. User can be allowed to input prompt for both summarising and paraphrasing. For e.g. User can select funny, sad etc. paraphrasing options.  