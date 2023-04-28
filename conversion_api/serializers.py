from rest_framework import serializers
from .models import ConversionResponse


class ConversionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionResponse
        fields = ["amount", "message", "is_success"]
