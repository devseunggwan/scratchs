# S3 Tables with PyIceberg

## Overview

This project provides utility classes that help you easily manage S3-based Apache Iceberg catalogs and tables using the PyIceberg library.

## Key Features

- S3-based Iceberg catalog setup and management
- AWS S3 REST API signature support (SigV4)
- Simple catalog wrapper class

## How to Run

1. Install dependencies:
```bash
uv sync
```

2. Use the catalog:
```python
from catalog import S3TableConfig, S3TableCatalog

# Configure S3 table
config = S3TableConfig(
    type="rest",
    warehouse="s3://your-warehouse-bucket/",
    uri="https://your-rest-catalog-endpoint"
)

# Create catalog
catalog = S3TableCatalog("my_catalog", config)

# Use catalog
namespaces = catalog.list_namespaces()
tables = catalog.list_tables("my_database")
table = catalog.load_table("my_database.my_table")
```
