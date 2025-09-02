# Fish Data Import Guide

## Overview

This guide explains how to import fish species and fish data from CSV or Excel files into the Fish Chain Optimization system.

## API Endpoints

### Import Fish Species

- **URL**: `POST /api/fishs/species/import/`
- **Description**: Import fish species data from a CSV or Excel file
- **File Format**: CSV or Excel (.xlsx, .xls)
- **Authentication**: Required (Token Authentication)

### Import Fish

- **URL**: `POST /api/fishs/fish/import/`
- **Description**: Import fish data from a CSV or Excel file
- **File Format**: CSV or Excel (.xlsx, .xls)
- **Authentication**: Required (Token Authentication)

### Download Fish Species Template

- **URL**: `GET /api/fishs/species/template/`
- **Description**: Download CSV template for fish species import
- **Authentication**: Required (Token Authentication)

### Download Fish Template

- **URL**: `GET /api/fishs/fish/template/`
- **Description**: Download CSV template for fish import
- **Authentication**: Required (Token Authentication)

## File Format Requirements

### Fish Species Import

The CSV/Excel file should contain the following columns:

- `name` (required): Unique name of the fish species
- `scientific_name` (optional): Scientific name of the fish species
- `description` (optional): Description of the fish species

**Sample CSV format:**

```csv
name,scientific_name,description
Tuna,Thunnus,Thunnus is a genus of ocean-dwelling ray-finned fish
Salmon,Salmo salar,Salmon is the common name for several species
```

### Fish Import

The CSV/Excel file should contain the following columns:

- `species_name` (required): Name of the existing fish species
- `name` (optional): Name of the individual fish
- `notes` (optional): Additional notes about the fish

**Sample CSV format:**

```csv
species_name,name,notes
Tuna,Bluefin Tuna,Caught in Pacific Ocean
Salmon,Atlantic Salmon,Farmed in Norway
```

## How to Use

### Download Templates

```bash
# Download fish species template
curl -X GET \
  http://localhost:8000/api/fishs/species/template/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -o fish_species_template.csv

# Download fish template
curl -X GET \
  http://localhost:8000/api/fishs/fish/template/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -o fish_template.csv
```

### Import Data

```bash
# Import fish species
curl -X POST \
  http://localhost:8000/api/fishs/species/import/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -F 'file=@fish_species_template.csv'

# Import fish
curl -X POST \
  http://localhost:8000/api/fishs/fish/import/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -F 'file=@fish_template.csv'
```

### Using Python requests

```python
import requests

# Download templates
species_template_url = 'http://localhost:8000/api/fishs/species/template/'
fish_template_url = 'http://localhost:8000/api/fishs/fish/template/'
headers = {'Authorization': 'Token YOUR_AUTH_TOKEN'}

# Download fish species template
response = requests.get(species_template_url, headers=headers)
with open('fish_species_template.csv', 'wb') as f:
    f.write(response.content)

# Download fish template
response = requests.get(fish_template_url, headers=headers)
with open('fish_template.csv', 'wb') as f:
    f.write(response.content)

# Import fish species
url = 'http://localhost:8000/api/fishs/species/import/'
files = {'file': open('fish_species_template.csv', 'rb')}

response = requests.post(url, headers=headers, files=files)
print(response.json())

# Import fish
url = 'http://localhost:8000/api/fishs/fish/import/'
files = {'file': open('fish_template.csv', 'rb')}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

## Response Format

### Success Response

```json
{
  "message": "Successfully processed X fish species",
  "created_count": X,
  "errors": []
}
```

### Partial Success Response

```json
{
  "message": "Successfully processed X fish species",
  "created_count": X,
  "errors": [
    "Row 2: Missing required 'name' field",
    "Row 5: Fish species 'Shark' does not exist"
  ],
  "warning": "Some rows had errors during import"
}
```

### Error Response

```json
{
  "error": "Failed to process file: [error details]"
}
```

## Error Handling

- If a fish species with the same name already exists, it will be updated with the new data
- If a fish species referenced in the fish import does not exist, that row will be skipped with an error
- All operations are atomic - if any error occurs, no changes will be committed to the database
- Rows with missing required fields will be skipped with appropriate error messages

## Best Practices

1. Always download and use the provided template files as a starting point
2. Ensure all required fields are filled in
3. Check that referenced fish species exist before importing fish data
4. Review the response for any errors or warnings after import
5. Make backups of your data before performing large imports
