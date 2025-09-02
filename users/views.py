from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, ShipOwnerProfileSerializer, CaptainProfileSerializer, AdminProfileSerializer

@extend_schema(
    summary="Registrasi Pengguna Baru",
    description="""
    Endpoint ini digunakan untuk mendaftarkan pengguna baru ke dalam sistem.
    Pengguna dapat mendaftar sebagai pemilik kapal, kapten, atau admin.
    
    Parameter yang diperlukan:
    - username: Nama pengguna unik
    - email: Alamat email pengguna
    - password: Kata sandi (minimal 8 karakter)
    - password_confirm: Konfirmasi kata sandi
    - user_type: Tipe pengguna (ship_owner, captain, admin)
    
    Parameter opsional:
    - phone_number: Nomor telepon pengguna
    - role: Peran pengguna (jika tersedia dalam sistem)
    
    Parameter khusus berdasarkan tipe pengguna:
    - Untuk ship_owner:
      - owner_type: Tipe pemilik (individual/company)
      - company_name: Nama perusahaan (untuk pemilik perusahaan)
      - tax_id: NPWP
    - Untuk captain:
      - license_number: Nomor lisensi nahkoda
      - years_of_experience: Tahun pengalaman
    - Untuk admin:
      - employee_id: ID pegawai
      - department: Departemen
      - position: Jabatan
    """,
    request=UserRegistrationSerializer,
    responses={
        201: {
            'type': 'object',
            'properties': {
                'user': {'$ref': '#/components/schemas/User'},
                'tokens': {
                    'type': 'object',
                    'properties': {
                        'refresh': {'type': 'string'},
                        'access': {'type': 'string'}
                    }
                },
                'message': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Contoh Permintaan - Ship Owner Individual',
            summary='Contoh pendaftaran pemilik kapal individual',
            value={
                'username': 'johndoe',
                'email': 'john@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'user_type': 'ship_owner',
                'owner_type': 'individual',
                'phone_number': '+628123456789'
            }
        ),
        OpenApiExample(
            'Contoh Permintaan - Ship Owner Company',
            summary='Contoh pendaftaran pemilik kapal perusahaan',
            value={
                'username': 'companyowner',
                'email': 'company@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'user_type': 'ship_owner',
                'owner_type': 'company',
                'company_name': 'PT. Sea Transport',
                'tax_id': '123456789012345',
                'phone_number': '+628123456789'
            }
        ),
        OpenApiExample(
            'Contoh Permintaan - Captain',
            summary='Contoh pendaftaran nahkoda',
            value={
                'username': 'captainjack',
                'email': 'jack@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'user_type': 'captain',
                'license_number': 'CAPT001',
                'years_of_experience': 10,
                'phone_number': '+628123456789'
            }
        ),
        OpenApiExample(
            'Contoh Permintaan - Admin',
            summary='Contoh pendaftaran admin',
            value={
                'username': 'adminuser',
                'email': 'admin@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'user_type': 'admin',
                'employee_id': 'EMP001',
                'department': 'Operations',
                'position': 'Manager',
                'phone_number': '+628123456789'
            }
        ),
        OpenApiExample(
            'Contoh Respons Sukses',
            summary='Respons sukses pendaftaran',
            value={
                'user': {
                    'id': 1,
                    'username': 'johndoe',
                    'email': 'john@example.com',
                    'phone_number': '+628123456789',
                    'date_joined': '2023-01-01T00:00:00Z',
                    'role_names': ['ship_owner'],
                    'ship_owner_profile': {
                        'id': 1,
                        'owner_type': 'individual',
                        'company_name': None,
                        'tax_id': None,
                        'address': None,
                        'contact_person': None,
                        'created_at': '2023-01-01T00:00:00Z',
                        'updated_at': '2023-01-01T00:00:00Z'
                    }
                },
                'tokens': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                'message': 'User registered successfully'
            }
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user (ship owner, captain, or admin)
    
    Upon successful registration, this function returns:
    - User profile information (id, username, email, user_type, ship_number, phone_number, date_joined)
    - JWT tokens (access and refresh)
    - Success message
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)  # type: ignore
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Login Pengguna",
    description="""
    Endpoint ini digunakan untuk melakukan autentikasi pengguna.
    Pengguna dapat login menggunakan username dan password.
    
    Parameter yang diperlukan:
    - username: Nama pengguna
    - password: Kata sandi pengguna
    
    Respons akan berisi dua token:
    - access: Token akses untuk permintaan API (berlaku 60 menit)
    - refresh: Token refresh untuk mendapatkan token akses baru (berlaku 7 hari)
    
    Selain token, respons juga mencakup informasi profil pengguna lengkap sesuai dengan tipe pengguna.
    """,
    request=UserLoginSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'user': {'$ref': '#/components/schemas/User'},
                'tokens': {
                    'type': 'object',
                    'properties': {
                        'refresh': {'type': 'string'},
                        'access': {'type': 'string'}
                    }
                },
                'message': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        401: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Contoh Permintaan',
            summary='Contoh login pengguna',
            value={
                'username': 'johndoe',
                'password': 'securepassword123'
            }
        ),
        OpenApiExample(
            'Contoh Respons Sukses - Ship Owner',
            summary='Respons sukses login untuk pemilik kapal',
            value={
                'user': {
                    'id': 1,
                    'username': 'johndoe',
                    'email': 'john@example.com',
                    'phone_number': '+628123456789',
                    'date_joined': '2023-01-01T00:00:00Z',
                    'role_names': ['ship_owner'],
                    'ship_owner_profile': {
                        'id': 1,
                        'owner_type': 'individual',
                        'company_name': None,
                        'tax_id': None,
                        'address': None,
                        'contact_person': None,
                        'created_at': '2023-01-01T00:00:00Z',
                        'updated_at': '2023-01-01T00:00:00Z'
                    }
                },
                'tokens': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                'message': 'Login successful'
            }
        ),
        OpenApiExample(
            'Contoh Respons Sukses - Captain',
            summary='Respons sukses login untuk nahkoda',
            value={
                'user': {
                    'id': 2,
                    'username': 'captainjack',
                    'email': 'jack@example.com',
                    'phone_number': '+628123456789',
                    'date_joined': '2023-01-01T00:00:00Z',
                    'role_names': ['captain'],
                    'captain_profile': {
                        'id': 1,
                        'license_number': 'CAPT001',
                        'years_of_experience': 10,
                        'vessel_type_experience': None,
                        'certification': None,
                        'address': None,
                        'emergency_contact': None,
                        'created_at': '2023-01-01T00:00:00Z',
                        'updated_at': '2023-01-01T00:00:00Z'
                    }
                },
                'tokens': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                'message': 'Login successful'
            }
        ),
        OpenApiExample(
            'Contoh Respons Sukses - Admin',
            summary='Respons sukses login untuk admin',
            value={
                'user': {
                    'id': 3,
                    'username': 'adminuser',
                    'email': 'admin@example.com',
                    'phone_number': '+628123456789',
                    'date_joined': '2023-01-01T00:00:00Z',
                    'role_names': ['admin'],
                    'admin_profile': {
                        'id': 1,
                        'employee_id': 'EMP001',
                        'department': 'Operations',
                        'position': 'Manager',
                        'institution': None,
                        'address': None,
                        'created_at': '2023-01-01T00:00:00Z',
                        'updated_at': '2023-01-01T00:00:00Z'
                    }
                },
                'tokens': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                'message': 'Login successful'
            }
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user with username and password, returns JWT tokens and user profile information.
    
    Upon successful authentication, this function returns:
    - User profile information (id, username, email, user_type, ship_number, phone_number, date_joined)
    - JWT tokens (access and refresh)
    - Success message
    
    The access token should be used in the Authorization header for subsequent requests:
    Authorization: Bearer <access_token>
    
    The refresh token can be used to obtain a new access token when it expires.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        # Type check fix: Access validated_data after is_valid() check
        username = serializer.validated_data['username']  # type: ignore
        password = serializer.validated_data['password']  # type: ignore
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Create JWT tokens
            refresh = RefreshToken.for_user(user)  # type: ignore
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Logout Pengguna",
    description="""
    Endpoint ini digunakan untuk melakukan logout pengguna.
    Token refresh pengguna akan dimasukkan ke daftar hitam (blacklist).
    
    Parameter yang diperlukan:
    - refresh: Token refresh yang akan dimasukkan ke daftar hitam
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'Refresh token yang akan dimasukkan ke daftar hitam'
                }
            },
            'required': ['refresh']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Contoh Permintaan',
            summary='Contoh logout pengguna',
            value={
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting their refresh token
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Error logging out'
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Refresh Token Akses",
    description="""
    Endpoint ini digunakan untuk mendapatkan token akses baru menggunakan token refresh.
    
    Parameter yang diperlukan:
    - refresh: Token refresh yang valid
    
    Respons akan berisi token akses baru yang berlaku selama 60 menit.
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'Refresh token yang valid'
                }
            },
            'required': ['refresh']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {'type': 'string'}
            }
        },
        401: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    },
    examples=[
        OpenApiExample(
            'Contoh Permintaan',
            summary='Contoh refresh token',
            value={
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        ),
        OpenApiExample(
            'Contoh Respons Sukses',
            summary='Respons sukses refresh token',
            value={
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh(request):
    """
    Refresh access token using refresh token
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        
        # Rotate token if enabled
        access_token = token.access_token
        
        return Response({
            'access': str(access_token),
        }, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'error': 'Error refreshing token'
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Profil Pengguna",
    description="""
    Endpoint ini digunakan untuk mendapatkan informasi profil pengguna yang sedang login.
    Hanya pengguna yang telah terautentikasi yang dapat mengakses endpoint ini.
    
    Respons akan mencakup informasi pengguna dasar dan profil spesifik berdasarkan tipe pengguna:
    - Untuk ship_owner: Informasi profil pemilik kapal
    - Untuk captain: Informasi profil nahkoda
    - Untuk admin: Informasi profil admin
    
    Untuk mengakses endpoint ini, sertakan header Authorization dengan format:
    Bearer <access_token>
    """,
    responses={
        200: UserSerializer
    },
    examples=[
        OpenApiExample(
            'Contoh Respons - Ship Owner',
            summary='Respons profil untuk pemilik kapal',
            value={
                'id': 1,
                'username': 'johndoe',
                'email': 'john@example.com',
                'phone_number': '+628123456789',
                'date_joined': '2023-01-01T00:00:00Z',
                'role_names': ['ship_owner'],
                'ship_owner_profile': {
                    'id': 1,
                    'owner_type': 'individual',
                    'company_name': None,
                    'tax_id': None,
                    'address': None,
                    'contact_person': None,
                    'created_at': '2023-01-01T00:00:00Z',
                    'updated_at': '2023-01-01T00:00:00Z'
                }
            }
        ),
        OpenApiExample(
            'Contoh Respons - Captain',
            summary='Respons profil untuk nahkoda',
            value={
                'id': 2,
                'username': 'captainjack',
                'email': 'jack@example.com',
                'phone_number': '+628123456789',
                'date_joined': '2023-01-01T00:00:00Z',
                'role_names': ['captain'],
                'captain_profile': {
                    'id': 1,
                    'license_number': 'CAPT001',
                    'years_of_experience': 10,
                    'vessel_type_experience': None,
                    'certification': None,
                    'address': None,
                    'emergency_contact': None,
                    'created_at': '2023-01-01T00:00:00Z',
                    'updated_at': '2023-01-01T00:00:00Z'
                }
            }
        ),
        OpenApiExample(
            'Contoh Respons - Admin',
            summary='Respons profil untuk admin',
            value={
                'id': 3,
                'username': 'adminuser',
                'email': 'admin@example.com',
                'phone_number': '+628123456789',
                'date_joined': '2023-01-01T00:00:00Z',
                'role_names': ['admin'],
                'admin_profile': {
                    'id': 1,
                    'employee_id': 'EMP001',
                    'department': 'Operations',
                    'position': 'Manager',
                    'institution': None,
                    'address': None,
                    'created_at': '2023-01-01T00:00:00Z',
                    'updated_at': '2023-01-01T00:00:00Z'
                }
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@extend_schema(
    summary="Update Profil Pengguna",
    description="""
    Endpoint ini digunakan untuk memperbarui informasi profil pengguna yang sedang login.
    Pengguna dapat memperbarui informasi seperti email, nomor telepon, dll.
    
    Parameter yang dapat diperbarui:
    - email: Alamat email pengguna
    - first_name: Nama depan pengguna
    - last_name: Nama belakang pengguna
    - phone_number: Nomor telepon pengguna
    
    Untuk memperbarui profil spesifik (ship_owner_profile, captain_profile, admin_profile),
    gunakan endpoint khusus untuk setiap tipe profil.
    
    Untuk mengakses endpoint ini, sertakan header Authorization dengan format:
    Bearer <access_token>
    """,
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update Profil Pemilik Kapal",
    description="""
    Endpoint ini digunakan untuk memperbarui informasi profil pemilik kapal.
    Hanya pengguna dengan tipe ship_owner yang dapat mengakses endpoint ini.
    
    Parameter yang dapat diperbarui:
    - owner_type: Tipe pemilik (individual/company)
    - company_name: Nama perusahaan (untuk pemilik perusahaan)
    - tax_id: NPWP
    - address: Alamat
    - contact_person: Kontak person
    
    Untuk mengakses endpoint ini, sertakan header Authorization dengan format:
    Bearer <access_token>
    """,
    request=ShipOwnerProfileSerializer,
    responses={
        200: ShipOwnerProfileSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        403: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ship_owner_profile(request):
    """
    Update ship owner profile
    """
    # Check if user has ship_owner profile
    if not hasattr(request.user, 'ship_owner_profile'):
        return Response({
            'error': 'User does not have a ship owner profile'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ShipOwnerProfileSerializer(request.user.ship_owner_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update Profil Nahkoda",
    description="""
    Endpoint ini digunakan untuk memperbarui informasi profil nahkoda.
    Hanya pengguna dengan tipe captain yang dapat mengakses endpoint ini.
    
    Parameter yang dapat diperbarui:
    - license_number: Nomor lisensi nahkoda
    - years_of_experience: Tahun pengalaman
    - vessel_type_experience: Pengalaman jenis kapal
    - certification: Sertifikasi
    - address: Alamat
    - emergency_contact: Kontak darurat
    
    Untuk mengakses endpoint ini, sertakan header Authorization dengan format:
    Bearer <access_token>
    """,
    request=CaptainProfileSerializer,
    responses={
        200: CaptainProfileSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        403: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_captain_profile(request):
    """
    Update captain profile
    """
    # Check if user has captain profile
    if not hasattr(request.user, 'captain_profile'):
        return Response({
            'error': 'User does not have a captain profile'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CaptainProfileSerializer(request.user.captain_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update Profil Admin",
    description="""
    Endpoint ini digunakan untuk memperbarui informasi profil admin.
    Hanya pengguna dengan tipe admin yang dapat mengakses endpoint ini.
    
    Parameter yang dapat diperbarui:
    - employee_id: ID pegawai
    - department: Departemen
    - position: Jabatan
    - institution: Institusi
    - address: Alamat
    
    Untuk mengakses endpoint ini, sertakan header Authorization dengan format:
    Bearer <access_token>
    """,
    request=AdminProfileSerializer,
    responses={
        200: AdminProfileSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        403: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_admin_profile(request):
    """
    Update admin profile
    """
    # Check if user has admin profile
    if not hasattr(request.user, 'admin_profile'):
        return Response({
            'error': 'User does not have an admin profile'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = AdminProfileSerializer(request.user.admin_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
