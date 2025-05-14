from .models import Concept
from .serializers import ConceptSerializer
from rest_framework import generics

class ConceptLists(generics.ListAPIView):
    serializer_class = ConceptSerializer
    def get_queryset(self):
        queryset = Concept.objects.all()
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset
class ConceptDetailView(generics.RetrieveAPIView):
    serializer_class = ConceptSerializer
    queryset = Concept.objects.all()