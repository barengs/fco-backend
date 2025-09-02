# Ship Data Import Guide

## Overview

This guide explains how to import ship data from CSV or Excel files into the Fish Chain Optimization system.

## API Endpoints

### Import Ships

- **URL**: `POST /api/ships/import/`
- **Description**: Import ship data from a CSV or Excel file
- **File Format**: CSV or Excel (.xlsx, .xls)
- **Authentication**: Required (Token Authentication)

### Download Ship Template

- **URL**: `GET /api/ships/template/`
- **Description**: Download CSV template for ship import
- **Authentication**: Required (Token Authentication)

## File Format Requirements

The CSV/Excel file should contain the following columns:

- `name` (required): Name of the ship
- `reg_number` (required): Unique registration number of the ship
- `length` (optional): Length of the ship in meters
- `width` (optional): Width of the ship in meters
- `gross_tonnage` (optional): Gross tonnage of the ship
- `year_built` (optional): Year the ship was built
- `home_port` (optional): Home port of the ship
- `active` (optional): Whether the ship is active (True/False, defaults to True)

**Sample CSV format:**

```csv
name,reg_number,length,width,gross_tonnage,year_built,home_port,active
MV Oceanic,SHIP001,45.5,8.2,1200.5,2010,"Port of Jakarta",True
MV Mariner,SHIP002,38.0,7.5,850.0,2015,"Port of Surabaya",True
```

## How to Use

### Download Template

```bash
# Download ship template
curl -X GET \
  http://localhost:8000/api/ships/template/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -o ship_template.csv
```

### Import Data

```bash
curl -X POST \
  http://localhost:8000/api/ships/import/ \
  -H 'Authorization: Token YOUR_AUTH_TOKEN' \
  -F 'file=@ship_template.csv'
```

### Using Python requests

```python
import requests

# Download template
template_url = 'http://localhost:8000/api/ships/template/'
headers = {'Authorization': 'Token YOUR_AUTH_TOKEN'}

response = requests.get(template_url, headers=headers)
with open('ship_template.csv', 'wb') as f:
    f.write(response.content)

# Import ships
url = 'http://localhost:8000/api/ships/import/'
files = {'file': open('ship_template.csv', 'rb')}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

## Response Format

### Success Response

```json
{
  "message": "Successfully processed X ships (Y updated)",
  "created_count": X,
  "updated_count": Y,
  "errors": []
}
```

### Partial Success Response

```json
{
  "message": "Successfully processed X ships (Y updated)",
  "created_count": X,
  "updated_count": Y,
  "errors": [
    "Row 2: Missing required 'name' field"
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

- If a ship with the same registration number already exists, it will be updated with the new data
- All operations are atomic - if any error occurs, no changes will be committed to the database
- Rows with missing required fields will be skipped with appropriate error messages

## Best Practices

1. Always download and use the provided template file as a starting point
2. Ensure all required fields (name, reg_number) are filled in
3. Review the response for any errors or warnings after import
4. Make backups of your data before performing large imports
