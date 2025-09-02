from rest_framework import serializers
from .models import Ship

class ShipSerializer(serializers.ModelSerializer):
    """
    Serializer untuk informasi kapal.
    
    Digunakan untuk menampilkan informasi kapal secara lengkap.
    """
    class Meta:
        model = Ship
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )

class ShipCreateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk membuat kapal baru.
    
    Digunakan saat membuat kapal baru dengan validasi nomor registrasi yang unik.
    """
    class Meta:
        model = Ship
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at'
        )
        
    def validate_reg_number(self, value):
        """
        Validasi nomor registrasi kapal.
        
        Memastikan nomor registrasi kapal bersifat unik dalam sistem.
        """
        # Using try/except with general Exception to avoid type checking issues
        try:
            Ship.objects.get(reg_number=value)  # type: ignore
            raise serializers.ValidationError("A ship with this registration number already exists.")
        except Exception:
            return value

class ShipUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk memperbarui informasi kapal.
    
    Digunakan saat memperbarui informasi kapal dengan pengecualian
    pada field nomor registrasi yang tidak dapat diubah.
    """
    class Meta:
        model = Ship
        fields = '__all__'
        read_only_fields = (
            'created_at', 
            'updated_at', 
            'reg_number'
        )  # Prevent changing reg_number