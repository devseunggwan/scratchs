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

Python projects use **uv** for dependency management (preferred):

```bash
# Initialize new project
uv init

# Add dependencies
uv add <package>
uv add --dev <dev-package>

# Install dependencies (creates .venv automatically)
uv sync

# Install with optional dependencies
uv sync --all-extras

# Run scripts
uv run python <script.py>

# Run with specific Python version
uv run --python 3.12 python <script.py>
```

Legacy projects may use pip + requirements.txt:
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Code Formatting (Ruff)

**Ruff** is the standard for Python linting and formatting:

```bash
# Format code
ruff format .

# Lint and auto-fix
ruff check --fix .

# Check without fixing
ruff check .
```

Standard `pyproject.toml` configuration:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

Configured hooks:
- **gitleaks**: Secret scanning
- **ruff**: Linting and formatting

## Git Commit Convention

This repository follows **Conventional Commits** specification.

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks, dependencies |

### Examples

```bash
# New feature
feat(google/bigquery): add Python connector for ETL pipelines

# Bug fix
fix(airflow): correct DAG scheduling interval

# Documentation
docs(README): update installation instructions

# Refactoring
refactor(trino): simplify connection handling

# Multiple lines with body
feat(dagster): add dbt integration

Add support for running dbt models as Dagster assets.
Includes automatic dependency detection and materialization.
```

### Scope Guidelines

- Use directory/project name: `google/bigquery`, `airflow`, `dagster`
- Use feature name for cross-cutting changes: `auth`, `config`
- Omit scope for repository-wide changes

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

# Initialize with uv (recommended)
uv init
uv add <dependencies>

# Or with pip (legacy)
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

```

## Architecture Notes

- **Date-based organization**: Data processing work follows YYYY/YYYYMM/YYYYMMDD structure for temporal tracking
- **Platform isolation**: Each platform exploration is self-contained in `platforms/<platform-name>/`
- **Experimentation focus**: This is a scratch repository - code prioritizes exploration over production readiness
- **Polyglot approach**: Primarily Python, with some Rust, SQL, and TypeScript experiments
