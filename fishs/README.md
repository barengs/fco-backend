# Fish Module Documentation

## Overview

The fish module provides CRUD functionality for managing fish species and individual fish in the Fish Chain Optimization system.

## Models

### FishSpecies

Represents a type of fish species with the following fields:

- `name`: Unique name of the fish species
- `scientific_name`: Scientific name of the fish species (optional)
- `description`: Description of the fish species (optional)
- `created_at`: Timestamp when the species was created
- `updated_at`: Timestamp when the species was last updated

### Fish

Represents an individual fish with the following fields:

- `species`: Foreign key to FishSpecies
- `name`: Name of the individual fish (optional)
- `notes`: Additional notes about the fish (optional)
- `created_at`: Timestamp when the fish was created
- `updated_at`: Timestamp when the fish was last updated

## API Endpoints

### Fish Species

- `GET /api/fishs/species/` - List all fish species
- `POST /api/fishs/species/` - Create a new fish species
- `GET /api/fishs/species/{id}/` - Retrieve a specific fish species
- `PUT /api/fishs/species/{id}/` - Update a specific fish species
- `DELETE /api/fishs/species/{id}/` - Delete a specific fish species

### Fish

- `GET /api/fishs/fish/` - List all fish
- `POST /api/fishs/fish/` - Create a new fish
- `GET /api/fishs/fish/{id}/` - Retrieve a specific fish
- `PUT /api/fishs/fish/{id}/` - Update a specific fish
- `DELETE /api/fishs/fish/{id}/` - Delete a specific fish

## Admin Interface

Both FishSpecies and Fish models are registered in the Django admin interface with appropriate list displays, filters, and search functionality.

## Serializers

Custom serializers are provided for each model with appropriate validation and field handling.

## Tests

Comprehensive tests are implemented for both models and API endpoints, covering:

- Model creation and validation
- String representation
- API authentication
- CRUD operations
