from django.urls import path

from wiki.views import get_wiki_sections, summarise, paraphrase, index
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("", index, name="index"),
    path("page/", get_wiki_sections, name="get_wiki_sections"),
    path("page/section/summarise/", summarise, name="summarise"),
    path("page/section/paraphrase/", paraphrase, name="paraphrase"),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
