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
from .models import Ship
from .serializers import ShipSerializer, ShipCreateSerializer, ShipUpdateSerializer

@extend_schema(
    summary="Daftar dan Buat Kapal",
    description="""
    Endpoint ini digunakan untuk mendapatkan daftar semua kapal atau membuat kapal baru.
    
    Metode GET:
    - Mengembalikan daftar semua kapal dalam sistem
    
    Metode POST:
    - Membuat kapal baru dengan data yang diberikan
    
    Parameter yang diperlukan untuk membuat kapal:
    - name: Nama kapal
    - reg_number: Nomor registrasi kapal (unik)
    
    Parameter opsional:
    - length: Panjang kapal dalam meter
    - width: Lebar kapal dalam meter
    - gross_tonnage: Gross tonnage kapal
    - year_built: Tahun pembuatan kapal
    - home_port: Pelabuhan asal kapal
    - active: Status aktif kapal (true/false)
    """,
    request=ShipCreateSerializer,
    responses={
        200: ShipSerializer(many=True),
        201: ShipSerializer,
        400: {
            'type': 'object',
            'properties': {
                'field_name': {'type': 'array', 'items': {'type': 'string'}}
            }
        }
    }
)
class ShipListCreateView(generics.ListCreateAPIView):
    queryset = Ship.objects.all()  # type: ignore
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method == 'POST':
            return ShipCreateSerializer
        return ShipSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    summary="Detail, Update, dan Hapus Kapal",
    description="""
    Endpoint ini digunakan untuk mendapatkan detail kapal, memperbarui data kapal, atau menghapus kapal.
    
    Metode GET:
    - Mengembalikan detail kapal berdasarkan ID
    
    Metode PUT/PATCH:
    - Memperbarui data kapal berdasarkan ID
    - Parameter reg_number tidak dapat diubah
    
    Metode DELETE:
    - Menghapus kapal berdasarkan ID
    """,
    request=ShipUpdateSerializer,
    responses={
        200: ShipSerializer,
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
class ShipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ship.objects.all()  # type: ignore
    serializer_class = ShipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):  # type: ignore
        if self.request.method in ['PUT', 'PATCH']:
            return ShipUpdateSerializer
        return ShipSerializer

# Template Download View
@extend_schema(
    summary="Unduh Template CSV Kapal",
    description="""
    Endpoint ini digunakan untuk mengunduh template CSV yang dapat digunakan untuk mengimpor data kapal.
    Template ini berisi contoh format dan data yang sesuai untuk proses impor massal.
    
    File yang diunduh:
    - ship_template.csv: Template CSV dengan kolom yang diperlukan dan opsional
    """,
    responses={
        (200, 'text/csv'): OpenApiTypes.BINARY
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_ship_template(request):
    """Download CSV template for ship import"""
    # Create a DataFrame with template data
    template_data = {
        'name': ['MV Oceanic', 'MV Mariner', 'MV Navigator'],
        'reg_number': ['SHIP001', 'SHIP002', 'SHIP003'],
        'length': [45.5, 38.0, 52.3],
        'width': [8.2, 7.5, 9.1],
        'gross_tonnage': [1200.5, 850.0, 1800.0],
        'year_built': [2010, 2015, 2008],
        'home_port': ['Port of Jakarta', 'Port of Surabaya', 'Port of Makassar'],
        'active': [True, True, True]
    }
    
    df = pd.DataFrame(template_data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ship_template.csv"'
    
    # Write DataFrame to response
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    response.write(csv_buffer.getvalue())
    
    return response

@extend_schema(
    summary="Impor Data Kapal dari File",
    description="""
    Endpoint ini digunakan untuk mengimpor data kapal dari file CSV atau Excel.
    Endpoint ini mendukung impor massal dengan fitur update otomatis untuk kapal yang sudah ada.
    
    Format file yang didukung:
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    
    Kolom yang diperlukan:
    - name: Nama kapal
    - reg_number: Nomor registrasi kapal (unik)
    
    Kolom opsional:
    - length: Panjang kapal dalam meter
    - width: Lebar kapal dalam meter
    - gross_tonnage: Gross tonnage kapal
    - year_built: Tahun pembuatan kapal
    - home_port: Pelabuhan asal kapal
    - active: Status aktif kapal (true/false)
    
    Fitur:
    - Jika kapal dengan reg_number yang sama sudah ada, data akan diperbarui
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
                'updated_count': {'type': 'integer'},
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
                'updated_count': {'type': 'integer'},
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
class ShipImportView(APIView):
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
            updated_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Extract data from row
                    name = row.get('name') or row.get('Name') or row.get('nama_kapal') or row.get('Nama Kapal')
                    reg_number = row.get('reg_number') or row.get('Reg Number') or row.get('nomor_registrasi') or row.get('Nomor Registrasi')
                    length = row.get('length') or row.get('Length') or row.get('panjang')
                    width = row.get('width') or row.get('Width') or row.get('lebar')
                    gross_tonnage = row.get('gross_tonnage') or row.get('Gross Tonnage') or row.get('gross_tonase')
                    year_built = row.get('year_built') or row.get('Year Built') or row.get('tahun_dibuat')
                    home_port = row.get('home_port') or row.get('Home Port') or row.get('pelabuhan_asal') or row.get('Pelabuhan Asal')
                    active = row.get('active', True)  # Default to True if not specified
                    
                    # Validate required fields
                    if not name:
                        errors.append(f"Row {int(index) + 1}: Missing required 'name' field")  # type: ignore
                        continue
                        
                    if not reg_number:
                        errors.append(f"Row {int(index) + 1}: Missing required 'reg_number' field")  # type: ignore
                        continue
                    
                    # Convert data types if needed
                    if length is not None:
                        try:
                            length = float(length)
                        except (ValueError, TypeError):
                            length = None
                            
                    if width is not None:
                        try:
                            width = float(width)
                        except (ValueError, TypeError):
                            width = None
                            
                    if gross_tonnage is not None:
                        try:
                            gross_tonnage = float(gross_tonnage)
                        except (ValueError, TypeError):
                            gross_tonnage = None
                            
                    if year_built is not None:
                        try:
                            year_built = int(year_built)
                        except (ValueError, TypeError):
                            year_built = None
                    
                    # Create or update Ship
                    ship, created = Ship.objects.get_or_create(  # type: ignore
                        reg_number=reg_number,
                        defaults={
                            'name': name,
                            'length': length,
                            'width': width,
                            'gross_tonnage': gross_tonnage,
                            'year_built': year_built,
                            'home_port': home_port,
                            'active': active
                        }
                    )
                    
                    # If ship already exists, update it
                    if not created:
                        ship.name = name
                        ship.length = length
                        ship.width = width
                        ship.gross_tonnage = gross_tonnage
                        ship.year_built = year_built
                        ship.home_port = home_port
                        ship.active = active
                        ship.save()
                        updated_count += 1
                    else:
                        created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {int(index) + 1}: {str(e)}")  # type: ignore
            
            # Prepare response
            response_data = {
                'message': f'Successfully processed {created_count} ships ({updated_count} updated)',
                'created_count': created_count,
                'updated_count': updated_count,
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