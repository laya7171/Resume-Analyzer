# Resume Parser

Resume Parser is a FastAPI service that reads a resume PDF, extracts the skills mentioned in it, evaluates the resume with a local language model, and ranks available jobs from a SQLite database.

## Features

- Accepts PDF resume uploads.
- Extracts text from every page with `pypdf`.
- Extracts explicitly mentioned technical and soft skills with an Ollama model.
- Produces a structured resume score from 0 to 100.
- Returns a recommendation, improvement suggestions, and a fit verdict.
- Matches the candidate against jobs stored in SQLite.
- Includes a standalone browser frontend in `app/frontend.html`.

## How It Works

The upload endpoint runs a three-step LangGraph workflow:

1. Extract skills from the extracted resume text.
2. Analyze the resume and generate a score and recommendation.
3. Fetch all jobs from SQLite and rank them by skill match.

The structured model output is validated with Pydantic models in `app/schema/model_output_schema.py`:

- `SkillExtractionOutput` contains a list of skills.
- `AnalysisOutput` contains `overall_score`, `recommendation`, `suggestions`, and `verdict`.
- `MatchJobOutput` contains ranked jobs with a role and match score.

## Project Structure

```text
.
|-- main.py                         # Minimal placeholder entry point
|-- pyproject.toml                  # Project metadata
|-- requirements.txt                # Python dependencies
|-- app/
|   |-- main.py                     # FastAPI application
|   |-- frontend.html               # Browser upload and results UI
|   |-- api/
|   |   |-- home.py                 # GET /
|   |   `-- resume.py               # POST /upload-resume
|   |-- config/core.py               # Application settings
|   |-- database/
|   |   |-- db_connection.py        # SQLite connection helper
|   |   `-- setup_db.py              # Creates the jobs table
|   |-- graph/workflow.py            # LangGraph workflow
|   |-- llm/provider.py              # Ollama model factory
|   |-- schema/                      # API, graph, and model schemas
|   |-- services/parser_service.py   # Parser service module
|   |-- tools/job_fetch.py           # Job database query
|   `-- utils/                       # PDF, skills, analysis, and matching helpers
`-- data/                            # Runtime SQLite data directory
```

## Requirements

- Python 3.10 or newer
- Ollama installed and running locally
- The Ollama model configured in `app/config/core.py` (default: `phi4-mini:latest`)

## Installation

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If your environment does not install these transitive packages automatically, install them directly:

```powershell
pip install pydantic-settings rich
```

Pull the configured Ollama model before making an analysis request:

```powershell
ollama pull phi4-mini:latest
```

The model name can be changed with the `model` setting in `app/config/core.py`.

## Database Setup

Create the SQLite database and its `jobs` table:

```powershell
python -m app.database.setup_db
```

The database is created at `data/resume_project.db`. The setup script creates the table only; add job records separately before using job matching. The table expects these fields:

```text
role
requirements
responsibility
type
```

## Run the API

From the repository root, start the development server:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Check the root endpoint:

```powershell
curl http://127.0.0.1:8000/
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API

### `GET /`

Returns a welcome message:

```json
{
  "message": "Welcome to the Resume Parser API!"
}
```

### `POST /upload-resume`

Upload a resume as multipart form data using the field name `file`. Only PDFs are accepted.

Example:

```powershell
curl -X POST http://127.0.0.1:8000/upload-resume -F "file=@resume.pdf"
```

The response contains the workflow state, including:

```json
{
  "raw_text": "...",
  "skills": ["Python", "FastAPI"],
  "overall_score": 82,
  "recommendation": "...",
  "suggestions": ["..."],
  "verdict": "Strong Fit",
  "matched_jobs": [
    {
      "role": "Backend Developer",
      "match_score": 88
    }
  ]
}
```

If the uploaded file is not a PDF, the API returns `400`. If no text can be extracted, it also returns `400`.

## Frontend

Start the API first, then open `app/frontend.html` in a browser. The page sends uploads to `http://127.0.0.1:8000/upload-resume` and displays the score, feedback, and matched roles.

The FastAPI app enables permissive CORS so the standalone HTML file can call the local API.

## Configuration

Settings are defined in `app/config/core.py`:

```python
app_name = "Resume Parser"
model = "phi4-mini:latest"
database_path = "data/resume_project.db"
```

Update `model` to use another Ollama model or update `database_path` to use another SQLite file. Paths are resolved relative to the directory where the application is started.

## Current Limitations

- The analysis depends on the configured local Ollama model being available.
- Scanned or image-only PDFs may produce little or no extracted text because the parser does not perform OCR.
- Job matching uses every row in the `jobs` table and requires that table to exist.
- The API currently returns the extracted `raw_text` along with the analysis result.
- `app/schema/api_schema.py` defines request and response models, but the upload route currently returns the LangGraph state directly instead of using those models.
