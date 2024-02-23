# Introduction
This project involve using the Wikipedia API to access content from a specific Wikipedia page and then applying OpenAI's GPT-3.5 Turbo for summarization and paraphrasing.

Homepage: http://43.205.140.181/wiki/page/

APIs:
-----------
Documentation: http://43.205.140.181/wiki/api/schema/swagger-ui/

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
- Python = 3.11 
- wikipedia-api = 0.6.0 
- djangorestframework = 3.14.0 
- Django = 4.2.10 
- openai = 1.12.0 
- drf-spectacular = 0.27.1
  
Installation
------------
Add .env file and put the following:
- OPENAI_API_KEY is used to call OPENAI API.
- DJANGO_SECRET_KEY is a secret used by Django.

```
OPENAI_API_KEY="XXXXXXXXXXXXXXXXX"
DJANGO_SECRET_KEY="django-insecure-XXXXXXXXXX"
```

Build docker image using 

    $ docker compose -f docker-compose-prod.yml build

Run docker container using

    $  docker compose -f docker-compose-prod.yml up -d

Possible future enhancements
----------------------------
1. User can be allowed to input prompt for both summarising and paraphrasing. For e.g. User can select funny, sad etc. paraphrasing options.  