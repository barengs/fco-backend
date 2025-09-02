from rest_framework import serializers
from .models import FishingArea

class FishingAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for FishingArea model
    """
    class Meta:
        model = FishingArea
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class FishingAreaImportSerializer(serializers.Serializer):
    """
    Serializer for importing FishingArea data from CSV/Excel
    """
    file = serializers.FileField(help_text="File CSV atau Excel yang berisi data wilayah penangkapan")