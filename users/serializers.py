from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from .models import User, ShipOwnerProfile, CaptainProfile, AdminProfile

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Validates username and password for authentication.
    """
    username = serializers.CharField(
        required=True,
        help_text="Nama pengguna"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Kata sandi pengguna"
    )
    
    def validate(self, attrs):
        """
        Validate the login credentials.
        """
        # This method can be extended to add custom validation if needed
        return attrs


class ShipOwnerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for ship owner profile information.
    """
    class Meta:
        model = ShipOwnerProfile
        fields = (
            'id',
            'owner_type',
            'company_name',
            'tax_id',
            'address',
            'contact_person',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )


class CaptainProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for captain profile information.
    """
    class Meta:
        model = CaptainProfile
        fields = (
            'id',
            'license_number',
            'years_of_experience',
            'vessel_type_experience',
            'certification',
            'address',
            'emergency_contact',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )


class AdminProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for admin profile information.
    """
    class Meta:
        model = AdminProfile
        fields = (
            'id',
            'employee_id',
            'department',
            'position',
            'institution',
            'address',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer untuk registrasi pengguna baru.
    
    Digunakan untuk mendaftarkan pengguna baru ke dalam sistem dengan semua
    informasi yang diperlukan.
    """
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        help_text="Kata sandi pengguna (minimal 8 karakter)"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Konfirmasi kata sandi"
    )
    role = serializers.CharField(
        required=False,
        help_text="Peran pengguna (jika tersedia dalam sistem)"
    )
    
    # Ship owner specific fields
    owner_type = serializers.CharField(required=False, help_text="Tipe pemilik (individual/company)")
    company_name = serializers.CharField(required=False, help_text="Nama perusahaan (untuk pemilik perusahaan)")
    tax_id = serializers.CharField(required=False, help_text="NPWP")
    
    # Captain specific fields
    license_number = serializers.CharField(required=False, help_text="Nomor lisensi nahkoda")
    years_of_experience = serializers.IntegerField(required=False, help_text="Tahun pengalaman")
    
    # Admin specific fields
    employee_id = serializers.CharField(required=False, help_text="ID pegawai")
    department = serializers.CharField(required=False, help_text="Departemen")
    position = serializers.CharField(required=False, help_text="Jabatan")
    
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'phone_number', 
            'password', 
            'password_confirm', 
            'role',
            # Ship owner fields
            'owner_type',
            'company_name',
            'tax_id',
            # Captain fields
            'license_number',
            'years_of_experience',
            # Admin fields
            'employee_id',
            'department',
            'position',
        )
        extra_kwargs = {
            'email': {
                'required': True,
                'help_text': "Alamat email pengguna"
            },
            'username': {
                'help_text': "Nama pengguna unik"
            },
            'phone_number': {
                'help_text': "Nomor telepon pengguna"
            }
        }
    
    def validate_role(self, value):
        """
        Validasi peran pengguna.
        
        Memastikan peran yang diberikan ada dalam sistem.
        """
        if value:
            try:
                Group.objects.get(name=value)
            except Exception:
                raise serializers.ValidationError(f"Role '{value}' does not exist.")
        return value
    
    def validate(self, attrs):
        """
        Validasi data pengguna berdasarkan role.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        
        role = attrs.get('role')
        
        # Validate required fields based on role
        if role == 'ship_owner':
            owner_type = attrs.get('owner_type', 'individual')
            if owner_type == 'company' and not attrs.get('company_name'):
                raise serializers.ValidationError("Company name is required for company owners.")
        elif role == 'captain':
            if not attrs.get('license_number'):
                raise serializers.ValidationError("License number is required for captains.")
        elif role == 'admin':
            if not attrs.get('employee_id'):
                raise serializers.ValidationError("Employee ID is required for admin users.")
            
        return attrs
    
    def create(self, validated_data):
        """
        Membuat pengguna baru dengan profil yang sesuai.
        """
        # Remove profile-specific fields
        password_confirm = validated_data.pop('password_confirm')
        role = validated_data.pop('role', None)
        password = validated_data.pop('password')
        
        # Profile-specific fields
        owner_type = validated_data.pop('owner_type', 'individual')
        company_name = validated_data.pop('company_name', None)
        tax_id = validated_data.pop('tax_id', None)
        license_number = validated_data.pop('license_number', None)
        years_of_experience = validated_data.pop('years_of_experience', None)
        employee_id = validated_data.pop('employee_id', None)
        department = validated_data.pop('department', None)
        position = validated_data.pop('position', None)
        
        # Create user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile based on role
        # Using type: ignore to help static analysis tools
        if role == 'ship_owner':
            ShipOwnerProfile.objects.create(  # type: ignore
                user=user,
                owner_type=owner_type,
                company_name=company_name if owner_type == 'company' else None,
                tax_id=tax_id
            )
        elif role == 'captain':
            CaptainProfile.objects.create(  # type: ignore
                user=user,
                license_number=license_number,
                years_of_experience=years_of_experience
            )
        elif role == 'admin':
            AdminProfile.objects.create(  # type: ignore
                user=user,
                employee_id=employee_id,
                department=department,
                position=position
            )
        
        # Assign role if provided
        if role:
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Exception:
                # Role doesn't exist, we could log this or handle it differently
                pass
                
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer untuk informasi pengguna.
    """
    ship_owner_profile = ShipOwnerProfileSerializer(read_only=True)
    captain_profile = CaptainProfileSerializer(read_only=True)
    admin_profile = AdminProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'email', 
            'phone_number', 
            'date_joined',
            'role_names',
            'ship_owner_profile',
            'captain_profile',
            'admin_profile',
        )
        read_only_fields = (
            'id', 
            'date_joined',
            'role_names',
        )
