from rest_framework import serializers
from .models import FishSpecies, Fish

class FishSpeciesSerializer(serializers.ModelSerializer):
    """
    Serializer untuk informasi jenis ikan.
    
    Digunakan untuk menampilkan informasi jenis ikan secara lengkap.
    """
    class Meta:
        model = FishSpecies
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )

class FishSpeciesCreateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk membuat jenis ikan baru.
    
    Digunakan saat membuat jenis ikan baru dengan validasi nama yang unik.
    """
    class Meta:
        model = FishSpecies
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )
        
    def validate_name(self, value):
        """
        Validasi nama jenis ikan.
        
        Memastikan nama jenis ikan bersifat unik dalam sistem (tidak case sensitive).
        """
        if FishSpecies.objects.filter(name__iexact=value).exists():  # type: ignore
            raise serializers.ValidationError("A fish species with this name already exists.")
        return value

class FishSpeciesUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk memperbarui informasi jenis ikan.
    
    Digunakan saat memperbarui informasi jenis ikan.
    """
    class Meta:
        model = FishSpecies
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )

class FishSerializer(serializers.ModelSerializer):
    """
    Serializer untuk informasi ikan.
    
    Digunakan untuk menampilkan informasi ikan secara lengkap dengan nama jenis ikan.
    """
    species_name = serializers.CharField(
        source='species.name', 
        read_only=True,
        help_text="Nama jenis ikan"
    )
    
    class Meta:
        model = Fish
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )

class FishCreateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk membuat ikan baru.
    
    Digunakan saat membuat ikan baru dengan informasi jenis ikan.
    """
    class Meta:
        model = Fish
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )

class FishUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk memperbarui informasi ikan.
    
    Digunakan saat memperbarui informasi ikan.
    """
    class Meta:
        model = Fish
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )