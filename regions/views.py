import pandas as pd
import io
from typing import Any
from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import FishingArea
from .serializers import FishingAreaSerializer, FishingAreaImportSerializer

@extend_schema(
    summary="Daftar Wilayah Penangkapan",
    description="Mengambil daftar semua wilayah penangkapan ikan",
    responses={200: FishingAreaSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_fishing_areas(request):
    """
    List all fishing areas
    """
    areas = FishingArea.objects.all().order_by('name')  # type: ignore
    serializer = FishingAreaSerializer(areas, many=True)
    return Response(serializer.data)

@extend_schema(
    summary="Detail Wilayah Penangkapan",
    description="Mengambil detail wilayah penangkapan berdasarkan ID",
    responses={200: FishingAreaSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fishing_area(request, area_id):
    """
    Get a specific fishing area by ID
    """
    try:
        area = FishingArea.objects.get(id=area_id)  # type: ignore
        serializer = FishingAreaSerializer(area)
        return Response(serializer.data)
    except FishingArea.DoesNotExist:  # type: ignore
        return Response({'error': 'Fishing area not found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Buat Wilayah Penangkapan Baru",
    description="Membuat wilayah penangkapan ikan baru",
    request=FishingAreaSerializer,
    responses={201: FishingAreaSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_fishing_area(request):
    """
    Create a new fishing area
    """
    serializer = FishingAreaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update Wilayah Penangkapan",
    description="Memperbarui wilayah penangkapan berdasarkan ID",
    request=FishingAreaSerializer,
    responses={200: FishingAreaSerializer}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_fishing_area(request, area_id):
    """
    Update a specific fishing area by ID
    """
    try:
        area = FishingArea.objects.get(id=area_id)  # type: ignore
    except FishingArea.DoesNotExist:  # type: ignore
        return Response({'error': 'Fishing area not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FishingAreaSerializer(area, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Hapus Wilayah Penangkapan",
    description="Menghapus wilayah penangkapan berdasarkan ID",
    responses={204: None}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_fishing_area(request, area_id):
    """
    Delete a specific fishing area by ID
    """
    try:
        area = FishingArea.objects.get(id=area_id)  # type: ignore
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except FishingArea.DoesNotExist:  # type: ignore
        return Response({'error': 'Fishing area not found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Import Data Wilayah Penangkapan",
    description="""
    Mengimpor data wilayah penangkapan dari file CSV atau Excel.
    
    Format file yang diterima:
    - CSV atau Excel (.xlsx)
    - Kolom yang diperlukan: name, code
    - Kolom opsional: description, coordinates
    
    Contoh format CSV:
    name,code,description,coordinates
    "Perairan Utara","N001","Wilayah penangkapan di utara","[[106.823, -6.234], [106.825, -6.232]]"
    "Perairan Selatan","S001","Wilayah penangkapan di selatan","[[106.820, -6.240], [106.822, -6.238]]"
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
        200: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'imported': {'type': 'integer'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_fishing_areas(request):
    """
    Import fishing areas from CSV or Excel file
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # Check file extension
    if not (file.name.endswith('.csv') or file.name.endswith('.xlsx')):
        return Response({'error': 'File must be CSV or Excel format'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read file based on extension
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Required columns
        required_columns = ['name', 'code']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response({'error': f'Missing required columns: {missing_columns}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process data with transaction
        with transaction.atomic():  # type: ignore
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Prepare data
                    data = {
                        'name': row['name'],
                        'code': row['code'],
                        'description': row.get('description', ''),
                        'coordinates': row.get('coordinates', '')
                    }
                    
                    # Check if area with same code already exists
                    area, created = FishingArea.objects.get_or_create(  # type: ignore
                        code=data['code'],
                        defaults=data
                    )
                    
                    if not created:
                        # Update existing area
                        for key, value in data.items():
                            setattr(area, key, value)
                        area.save()
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {int(str(index)) + 1}: {str(e)}")
            
            return Response({
                'message': f'Import completed. {imported_count} records processed.',
                'imported': imported_count,
                'errors': errors
            })
            
    except Exception as e:
        return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Download Template Import Wilayah Penangkapan",
    description="Mengunduh template CSV untuk import data wilayah penangkapan",
    responses={200: OpenApiTypes.BINARY}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_import_template(request):
    """
    Download CSV template for fishing area import
    """
    # Create sample data
    template_data = [
        ['name', 'code', 'description', 'coordinates'],
        ['Perairan Utara', 'N001', 'Wilayah penangkapan di utara', '[[106.823, -6.234], [106.825, -6.232]]'],
        ['Perairan Selatan', 'S001', 'Wilayah penangkapan di selatan', '[[106.820, -6.240], [106.822, -6.238]]'],
        ['Perairan Timur', 'E001', 'Wilayah penangkapan di timur', '[[106.830, -6.230], [106.832, -6.228]]']
    ]
    
    # Create CSV content
    csv_buffer = io.StringIO()
    for row in template_data:
        csv_buffer.write(','.join(['"' + str(cell) + '"' for cell in row]) + '\n')
    
    # Create response
    response = HttpResponse(csv_buffer.getvalue().encode('utf-8'), content_type='text/csv')  # type: ignore
    response['Content-Disposition'] = 'attachment; filename="fishing_area_template.csv"'
    
    return response