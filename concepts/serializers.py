from rest_framework import serializers
from .models import Concept


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'