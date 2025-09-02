from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import pandas as pd
import io
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import FishSpecies, Fish
from .serializers import (
    FishSpeciesSerializer, FishSpeciesCreateSerializer, FishSpeciesUpdateSerializer,
    FishSerializer, FishCreateSerializer, FishUpdateSerializer
)

# Fish Species Views
@extend_schema(
    summary="Daftar dan Buat Jenis Ikan",
    description="""
    Endpoint ini digunakan untuk mendapatkan daftar semua jenis ikan atau membuat jenis ikan baru.
    
    Metode GET:
    - Mengembalikan daftar semua jenis ikan dalam sistem
    
    Metode POST:
    - Membuat jenis ikan baru dengan data yang diberikan
    
    Parameter yang diperlukan untuk membuat jenis ikan:
    - name: Nama jenis ikan (unik)
    
    Parameter opsional:
    - scientific_name: Nama ilmiah jenis ikan
    - description: Deskripsi jenis ikan
    """,
    request=FishSpeciesCreateSerializer,
    responses={
        200: FishSpeciesSerializer(many=True),
        201: FishSpeciesSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    }
)
class FishSpeciesListCreateView(generics.ListCreateAPIView):
    queryset = FishSpecies.objects.all()  # type: ignore
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method == 'POST':
            return FishSpeciesCreateSerializer
        return FishSpeciesSerializer

@extend_schema(
    summary="Detail, Update, dan Hapus Jenis Ikan",
    description="""
    Endpoint ini digunakan untuk mendapatkan detail jenis ikan, memperbarui data jenis ikan, atau menghapus jenis ikan.
    
    Metode GET:
    - Mengembalikan detail jenis ikan berdasarkan ID
    
    Metode PUT/PATCH:
    - Memperbarui data jenis ikan berdasarkan ID
    
    Metode DELETE:
    - Menghapus jenis ikan berdasarkan ID
    """,
    request=FishSpeciesUpdateSerializer,
    responses={
        200: FishSpeciesSerializer,
        204: None,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        404: {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'}
            }
        }
    }
)
class FishSpeciesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FishSpecies.objects.all()  # type: ignore
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method in ['PUT', 'PATCH']:
            return FishSpeciesUpdateSerializer
        return FishSpeciesSerializer

# Fish Views
@extend_schema(
    summary="Daftar dan Buat Ikan",
    description="""
    Endpoint ini digunakan untuk mendapatkan daftar semua ikan atau membuat ikan baru.
    
    Metode GET:
    - Mengembalikan daftar semua ikan dalam sistem dengan informasi jenis ikan
    
    Metode POST:
    - Membuat ikan baru dengan data yang diberikan
    
    Parameter yang diperlukan untuk membuat ikan:
    - species: ID jenis ikan
    - species_name: Nama jenis ikan (alternatif untuk species ID)
    
    Parameter opsional:
    - name: Nama ikan
    - notes: Catatan tambahan tentang ikan
    """,
    request=FishCreateSerializer,
    responses={
        200: FishSerializer(many=True),
        201: FishSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    }
)
class FishListCreateView(generics.ListCreateAPIView):
    queryset = Fish.objects.select_related('species').all()  # type: ignore
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method == 'POST':
            return FishCreateSerializer
        return FishSerializer

@extend_schema(
    summary="Detail, Update, dan Hapus Ikan",
    description="""
    Endpoint ini digunakan untuk mendapatkan detail ikan, memperbarui data ikan, atau menghapus ikan.
    
    Metode GET:
    - Mengembalikan detail ikan berdasarkan ID
    
    Metode PUT/PATCH:
    - Memperbarui data ikan berdasarkan ID
    
    Metode DELETE:
    - Menghapus ikan berdasarkan ID
    """,
    request=FishUpdateSerializer,
    responses={
        200: FishSerializer,
        204: None,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        },
        404: {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'}
            }
        }
    }
)
class FishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fish.objects.select_related('species').all()  # type: ignore
    serializer_class = FishSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method in ['PUT', 'PATCH']:
            return FishUpdateSerializer
        return FishSerializer

# Template Download Views
@extend_schema(
    summary="Unduh Template CSV Jenis Ikan",
    description="""
    Endpoint ini digunakan untuk mengunduh template CSV yang dapat digunakan untuk mengimpor data jenis ikan.
    Template ini berisi contoh format dan data yang sesuai untuk proses impor massal jenis ikan.
    
    File yang diunduh:
    - fish_species_template.csv: Template CSV dengan kolom yang diperlukan dan opsional untuk jenis ikan
    """,
    responses={
        (200, 'text/csv'): OpenApiTypes.BINARY
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_fish_species_template(request):
    """Download CSV template for fish species import"""
    # Create a DataFrame with template data
    template_data = {
        'name': ['Tuna', 'Salmon', 'Cod'],
        'scientific_name': ['Thunnus', 'Salmo salar', 'Gadus morhua'],
        'description': [
            'Large saltwater fish',
            'Farmed fish',
            'North Atlantic fish'
        ]
    }
    
    df = pd.DataFrame(template_data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fish_species_template.csv"'
    
    # Write DataFrame to response
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    response.write(csv_buffer.getvalue())
    
    return response

@extend_schema(
    summary="Unduh Template CSV Ikan",
    description="""
    Endpoint ini digunakan untuk mengunduh template CSV yang dapat digunakan untuk mengimpor data ikan.
    Template ini berisi contoh format dan data yang sesuai untuk proses impor massal ikan.
    
    File yang diunduh:
    - fish_template.csv: Template CSV dengan kolom yang diperlukan dan opsional untuk ikan
    """,
    responses={
        (200, 'text/csv'): OpenApiTypes.BINARY
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_fish_template(request):
    """Download CSV template for fish import"""
    # Create a DataFrame with template data
    template_data = {
        'species_name': ['Tuna', 'Salmon', 'Cod'],
        'name': ['Bluefin Tuna', 'Atlantic Salmon', 'Pacific Cod'],
        'notes': [
            'Caught in Pacific Ocean',
            'Farmed in Norway',
            'Caught in Alaska'
        ]
    }
    
    df = pd.DataFrame(template_data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fish_template.csv"'
    
    # Write DataFrame to response
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    response.write(csv_buffer.getvalue())
    
    return response

# Import Views
@extend_schema(
    summary="Impor Data Jenis Ikan dari File",
    description="""
    Endpoint ini digunakan untuk mengimpor data jenis ikan dari file CSV atau Excel.
    Endpoint ini mendukung impor massal dengan fitur update otomatis untuk jenis ikan yang sudah ada.
    
    Format file yang didukung:
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    
    Kolom yang diperlukan:
    - name: Nama jenis ikan (unik)
    
    Kolom opsional:
    - scientific_name: Nama ilmiah jenis ikan
    - description: Deskripsi jenis ikan
    
    Fitur:
    - Jika jenis ikan dengan nama yang sama sudah ada, data akan diperbarui
    - Transaksi atomik (semua berhasil atau semua gagal)
    - Laporan error per baris
    """,
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary'
                }
            }
        }
    },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'created_count': {'type': 'integer'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        },
        206: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'created_count': {'type': 'integer'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'warning': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    }
)
@method_decorator(csrf_exempt, name='dispatch')
class FishSpeciesImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    @transaction.atomic
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Check file extension
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response(
                    {'error': 'Unsupported file format. Please upload CSV or Excel file.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process the data
            created_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Extract data from row
                    name = row.get('name') or row.get('Name') or row.get('nama')
                    scientific_name = row.get('scientific_name') or row.get('Scientific Name') or row.get('nama_ilmiah')
                    description = row.get('description') or row.get('Description') or row.get('deskripsi')
                    
                    # Validate required fields
                    if not name:
                        errors.append(f"Row {int(index) + 1}: Missing required 'name' field")  # type: ignore
                        continue
                    
                    # Create or update FishSpecies
                    species, created = FishSpecies.objects.get_or_create(  # type: ignore
                        name=name,
                        defaults={
                            'scientific_name': scientific_name,
                            'description': description
                        }
                    )
                    
                    # If species already exists, update it
                    if not created:
                        species.scientific_name = scientific_name
                        species.description = description
                        species.save()
                    
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {int(index) + 1}: {str(e)}")  # type: ignore
            
            # Prepare response
            response_data = {
                'message': f'Successfully processed {created_count} fish species',
                'created_count': created_count,
                'errors': errors
            }
            
            if errors:
                response_data['warning'] = 'Some rows had errors during import'
                return Response(response_data, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': f'Failed to process file: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

@extend_schema(
    summary="Impor Data Ikan dari File",
    description="""
    Endpoint ini digunakan untuk mengimpor data ikan dari file CSV atau Excel.
    
    Format file yang didukung:
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    
    Kolom yang diperlukan:
    - species_name: Nama jenis ikan (harus sudah ada dalam sistem)
    
    Kolom opsional:
    - name: Nama ikan
    - notes: Catatan tambahan tentang ikan
    
    Fitur:
    - Membuat ikan baru berdasarkan data dalam file
    - Transaksi atomik (semua berhasil atau semua gagal)
    - Laporan error per baris
    - Validasi bahwa jenis ikan harus sudah ada dalam sistem
    """,
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary'
                }
            }
        }
    },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'created_count': {'type': 'integer'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        },
        206: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'created_count': {'type': 'integer'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'warning': {'type': 'string'}
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    }
)
@method_decorator(csrf_exempt, name='dispatch')
class FishImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    @transaction.atomic
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Check file extension
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response(
                    {'error': 'Unsupported file format. Please upload CSV or Excel file.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process the data
            created_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Extract data from row
                    species_name = row.get('species_name') or row.get('Species Name') or row.get('jenis_ikan')
                    name = row.get('name') or row.get('Name') or row.get('nama')
                    notes = row.get('notes') or row.get('Notes') or row.get('catatan')
                    
                    # Validate required fields
                    if not species_name:
                        errors.append(f"Row {int(index) + 1}: Missing required 'species_name' field")  # type: ignore
                        continue
                    
                    # Get or create the species
                    try:
                        species = FishSpecies.objects.get(name=species_name)  # type: ignore
                    except Exception:
                        errors.append(f"Row {int(index) + 1}: Fish species '{species_name}' does not exist")  # type: ignore
                        continue
                    
                    # Create Fish
                    Fish.objects.create(  # type: ignore
                        species=species,
                        name=name,
                        notes=notes
                    )
                    
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {int(index) + 1}: {str(e)}")  # type: ignore
            
            # Prepare response
            response_data = {
                'message': f'Successfully imported {created_count} fish',
                'created_count': created_count,
                'errors': errors
            }
            
            if errors:
                response_data['warning'] = 'Some rows had errors during import'
                return Response(response_data, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': f'Failed to process file: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )