from django.urls import path, include
from .views import ConceptDetailView, ConceptLists

concepturlpatterns = [
    path('concepts/', ConceptLists.as_view(), name='concept-list'),
    path('concepts/<uuid:pk>', ConceptDetailView.as_view(), name='concept-detail')
]