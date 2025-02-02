# PipeCraft: Flexible ETL Library

PipeCraft is a modern Python ETL library focusing on making data extraction simple and flexible. It provides a powerful set of tools to handle various data sources through an intuitive decorator-based API.

## Features

- Decorator-based configuration for clean and maintainable code
- Support for multiple data sources:
  - Web scraping (with Cloudflare protection handling)
  - REST APIs
  - Files
  - Databases (coming soon)
- Dynamic resource management
- Automatic batch processing
- Customizable output patterns
- Built-in retry mechanisms
- Rate limiting
- Extensible architecture

# Coming Soon

## CLI Tool
A powerful command-line interface to quickly scaffold and configure extractors:
- Generate boilerplate code for new extractors
- Manage configurations and credentials
- Test extractors from the command line
- Monitor extraction jobs

## Additional Data Sources
Expanding support for more data sources:
- S3 and Cloud Storage
- Disk Volumes
- MongoDB, PostgreSQL, MySQL
- Elasticsearch
- Kafka/RabbitMQ streams

## Transform Components
Complete ETL pipeline support:
- Data cleaning and validation
- Schema transformation
- Type conversion
- Aggregations
- Bulk loading
- Incremental updates
- Live Patching

## Load Process
Flexible data loading with multiple destination support:
- Database loaders (PostgreSQL, MySQL, MongoDB)
- File formats (Parquet, CSV, JSON)
- Cloud storage (S3, GCS)
- Data warehouses (BigQuery, Redshift)
- Message queues (Kafka, RabbitMQ)
- APIs and webhooks

## Advanced Features
Enhanced capabilities for production use:
- Distributed processing with Dask/Spark
- Job scheduling
- Progress tracking
- Error recovery
- Resource monitoring
- Performance metrics
- Data lineage tracking

## Pipeline Orchestration
Tools for managing complex data workflows:
- DAG-based pipeline definitions
- Dependency management
- Conditional execution
- Parallel processing
- Pipeline versioning
- Reusable components

## Monitoring & Logging
Comprehensive observability features:
- Structured logging
- Performance metrics
- Alert configuration
- Dashboard integration
- Status reporting

## Schema Management
Robust data validation and schema tools:
- Schema inference
- Validation rules
- Data quality checks
- Schema evolution
- Documentation generation