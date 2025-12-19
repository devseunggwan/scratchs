# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a scratch/experimentation repository for data engineering, data processing, platform exploration, and API integration work. Projects are organized chronologically and by platform/technology.

## Repository Structure

```
.
├── api/                    # API integrations (blockchain, e-commerce, naver, etc.)
├── data-processing/        # Data processing experiments organized by YYYY/YYYYMM/YYYYMMDD
├── infrastructure/         # Infrastructure as code (Docker, Terraform)
├── languages/             # Language-specific examples (Python, Rust)
├── machine-learning/      # ML/LLM experiments (HuggingFace, LangChain, Prophet)
└── platforms/             # Platform explorations (Airflow, Dagster, dbt, Snowflake, Trino, etc.)
```

## Development Environment

### Python Projects

Most Python projects use one of these dependency management approaches:

1. **Poetry** (preferred for structured projects):
   ```bash
   # Install dependencies
   poetry install

   # Activate virtual environment
   poetry shell

   # Run scripts
   poetry run python <script.py>
   ```

2. **pip + requirements.txt** (for quick experiments):
   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux

   # Install dependencies
   pip install -r requirements.txt
   ```

### Code Quality Tools

Pre-commit hooks are configured with:
- **gitleaks**: Secret scanning
- **ruff**: Python linting and formatting (replaces black, isort, flake8)

```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Ruff commands (if needed manually)
ruff check --fix .           # Lint and auto-fix
ruff format .                # Format code
```

## Platform-Specific Notes

### Apache Airflow

Located in `platforms/apache-airflow/`:
- DAG files in `dags/` directory
- Use Airflow REST API via `platforms/apache-airflow/rest-api/` for programmatic interactions
- Jupyter notebooks (`scratch.ipynb`) for API exploration

### Dagster

Located in `platforms/dagster/`:
- Multiple projects: `dagster-dbt/`, `dagster_university/`, `quickstart/`
- Run Dagster dev server: `dagster dev`
- Assets defined in `assets/` directory
- Integration with dbt projects

### dbt

Located in `platforms/dbt/`:
- `dbt_snowflake/`: dbt project for Snowflake
- `dbt_airflow/`: dbt with Airflow orchestration

Standard dbt commands:
```bash
dbt deps              # Install dependencies from packages.yml
dbt run               # Run models
dbt test              # Run tests
dbt debug             # Test connection
```

### Trino

Located in `platforms/trino/`:
- Python connector examples in `trino-operation-wtih-python-and-sql/`
- Jupyter notebooks for query exploration

### Snowflake

Located in `platforms/snowflake/`:
- Quickstart guides and tutorials
- Snowpark Python examples
- Streamlit apps for Snowflake integration

## Data Processing Workflow

Projects in `data-processing/` are organized by date (YYYY/YYYYMM/YYYYMMDD):
- Each subdirectory is a self-contained experiment
- Typically includes:
  - `pyproject.toml` or `requirements.txt` for dependencies
  - `src/` or root-level Python scripts
  - Jupyter notebooks (`*.ipynb`) for exploration
  - `.env` for environment-specific configuration (gitignored)

## Common Patterns

### Project Initialization

When creating a new dated experiment:
```bash
# Create directory structure
mkdir -p data-processing/2025/202512/20251219
cd data-processing/2025/202512/20251219

# Initialize with Poetry
poetry init --no-interaction
poetry add <dependencies>

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install <dependencies>
pip freeze > requirements.txt
```

### Environment Variables

- Use `.env` files for credentials and configuration (never commit)
- Reference `.env.example` files where available
- Common variables: AWS credentials, Snowflake credentials, API keys

### Jupyter Notebooks

- Used extensively for exploration and prototyping
- Naming: typically `scratch.ipynb` for experiments
- Checkpoints (`.ipynb_checkpoints/`) are gitignored

## Data File Handling

The following data file formats are gitignored (see `.gitignore`):
- Tabular: `*.csv`, `*.tsv`, `*.parquet`, `*.xlsx`, `*.xls`, `*.avro`
- Serialized: `*.pkl`, `*.pickle`, `*.h5`, `*.hdf5`, `*.npz`
- Media: `*.mp3`, `*.wav`, `*.mp4`, etc.
- Database: `*.db`

## Testing

Test structure varies by project:
- Unit tests typically in `tests/` directory
- Use pytest for Python testing:
  ```bash
  pytest                  # Run all tests
  pytest tests/test_*.py  # Run specific test file
  pytest -v              # Verbose output
  ```

## Airflow MCP Integration

This repository has Airflow MCP (Model Context Protocol) integration available via the `mcp__airflow-mcp__*` tools. Use these for:
- Listing and managing DAGs
- Triggering DAG runs
- Querying task instances
- Managing connections and variables
- Accessing datasets and event logs

Example workflows:
```bash
# List all DAGs
mcp__airflow-mcp__fetch_dags

# Get DAG details
mcp__airflow-mcp__get_dag(dag_id="example_dag")

# Trigger a DAG run
mcp__airflow-mcp__post_dag_run(dag_id="example_dag")

# List connections
mcp__airflow-mcp__list_connections
```

## Architecture Notes

- **Date-based organization**: Data processing work follows YYYY/YYYYMM/YYYYMMDD structure for temporal tracking
- **Platform isolation**: Each platform exploration is self-contained in `platforms/<platform-name>/`
- **Experimentation focus**: This is a scratch repository - code prioritizes exploration over production readiness
- **Polyglot approach**: Primarily Python, with some Rust, SQL, and TypeScript experiments
