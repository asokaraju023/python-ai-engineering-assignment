# AI-Assisted Software Engineering Prototype (Python)

## 1. Purpose

This runnable prototype demonstrates engineer-led AI-assisted software engineering. It includes:

- A Python/FastAPI URL shortener with persistent storage and click analytics.

- A requirement analysis endpoint that returns structured tasks, assumptions, ambiguities, validation checks, risks, and AI-assistance opportunities.

- Automated API tests.

- API contract, architecture, scenario, setup, and validation documentation.

**\*\*Important:\*\*** The requirement analyzer currently uses deterministic rules, not a live LLM. The AI prompt examples document how ChatGPT or GitHub Copilot can assist during development. This version is not an autonomous AI coding agent.

## 2. Requirements

- Python 3.10 or later

- pip

## 3. Project Structure

```text

app/

  main.py          # FastAPI endpoints and application setup

  database.py      # SQLite connection and schema initialization

  schemas.py       # Request and response validation

  analyzer.py      # Deterministic requirement analysis

tests/

  test_api.py      # Automated API tests

scripts/

  run_api_demo.py  # End-to-end API demonstration

samples/

  create_url.json

  greenfield.json

  brownfield.json

  ambiguous.json

docs/

  API_CONTRACT.md

```

## 4. Run Locally (Windows PowerShell)

Open PowerShell in the project root directory and run:

```powershell

py -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

uvicorn app.main:app --reload

```

Open the interactive Swagger UI:

http\://127.0.0.1:8000/docs

The OpenAPI specification is available at:

http\://127.0.0.1:8000/openapi.json

If PowerShell blocks virtual-environment activation, run the commands using `.\.venv\Scripts\python.exe` directly after creating the environment.

## 5. API Examples

### 5.1 Health Check

**\*\*Endpoint:\*\*** `GET /health`

Expected response: HTTP 200.

```json

{

  "status": "healthy"

}

```

This endpoint confirms that the application is responding. It does not perform a comprehensive database readiness check.

### 5.2 Create a Short URL

**\*\*Endpoint:\*\*** `POST /api/urls`

Request:

```json

{

  "url": "https\://example.com/products/123"

}

```

Expected response: HTTP 201, containing:

- `shortCode`

- `originalUrl`

- `shortUrl`

- `createdAtUtc`

The service generates a random short code and stores the mapping in SQLite.

### 5.3 Redirect to the Original URL

**\*\*Endpoint:\*\*** `GET /r/{shortCode}`

Example:

`GET /r/FGhNmeS`

Expected behavior:

- Returns HTTP 302 for an existing short code.

- Redirects the client to the original URL.

- Increments the click counter and updates the last-accessed timestamp.

- Returns HTTP 404 if the short code does not exist.

Use a client with automatic redirects disabled when demonstrating the HTTP 302 response.

### 5.4 Retrieve Click Analytics

**\*\*Endpoint:\*\*** `GET /api/urls/{shortCode}/analytics`

Returns the stored URL information, aggregate click count, creation timestamp, and last-accessed timestamp.

Expected response: HTTP 200 for an existing short code, or HTTP 404 for an unknown code.

### 5.5 Analyze a Requirement

**\*\*Endpoint:\*\*** `POST /api/requirements/analyze`

Example request:

```json

{

  "requirement": "Build a scalable URL shortener service with APIs, persistence, and analytics.",

  "scenario_type": "greenfield"

}

```

The `scenario_type` field is optional. Supported values are:

- `greenfield` — plan a new implementation.

- `brownfield` — plan a change to an existing system.

- `ambiguous` — identify missing information and clarify requirements.

The response includes a structured engineering problem, assumptions, ambiguities, tasks and dependencies, validation checks, risks, and AI-assistance examples.

**\*\*Implementation note:\*\*** This endpoint currently uses deterministic rules. It does not invoke a live LLM or autonomously generate and execute code.

## 6. Run Automated Tests

Run the following command from the project root:

```powershell

python -m pytest -v

```

The automated tests cover:

- Application health.

- URL creation and persistence.

- Invalid URL and unsupported scheme validation.

- Database integrity-error handling.

- Redirect behavior and click analytics.

- Unknown short-code and analytics requests.

- Greenfield, brownfield, and ambiguous requirement analysis.

## 7. Run the API Demo

Start the application in one PowerShell terminal:

```powershell

uvicorn app.main:app --reload

```

Open a second PowerShell terminal, activate the same virtual environment, and run:

```powershell

.\.venv\Scripts\Activate.ps1

python scripts/run_api_demo.py

```

The demo checks the health endpoint, creates a short URL, verifies the redirect response, checks analytics, and exercises all three requirement-analysis scenarios.

## 8. Verification Results

The latest local verification run completed successfully:

- **\*\*Automated tests:\*\*** 11 passed.

- **\*\*API demo:\*\*** All checks passed.

- **\*\*URL creation:\*\*** HTTP 201 verified.

- **\*\*Redirect:\*\*** HTTP 302 and destination verified.

- **\*\*Analytics:\*\*** HTTP 200 and click count verified.

- **\*\*Requirement analysis:\*\*** Greenfield, brownfield, and ambiguous scenarios passed.

- **\*\*Database connection cleanup:\*\*** Existing tests and API demo continued to pass after the connection-handling change.

- **Persistence across restart:** Separately verified on 25 October 2026 using a dedicated test URL.
- **Persistence evidence:** `evidence/persistence-check.txt` records that the same short code, original URL, creation timestamp, and click count were returned before and after the restart.

The automated test and API demo results above reflect the previously recorded verification run. The later persistence check provides additional evidence of data persistence across an application restart.

These results demonstrate the tested behavior of the local prototype. They do not establish production-scale performance, availability, or security.

## 9. Data and Database Configuration

The application uses SQLite. By default, the database file is:

`data/urls.db`

The database directory is created automatically when needed.

To use a different database file in Windows PowerShell:

```powershell

$env:URL_SHORTENER_DB = "data/demo.db"

uvicorn app.main:app --reload

```

Set the environment variable before starting the application.

A different database path may point to a new database, so previously stored URLs might not be available when using that path.

Keep database files out of source control.

## 10. API Contract and Architecture

The API contract is documented in:

`docs/API_CONTRACT.md`

The application generates its OpenAPI specification at `/openapi.json`, which is also rendered by Swagger UI.

The main components are:

- **\*\*FastAPI application (`app/main.py`):\*\*** Defines the REST endpoints and coordinates service behavior.

- **\*\*Request and response schemas (`app/schemas.py`):\*\*** Validate incoming requests and structure API responses.

- **\*\*SQLite database (`app/database.py`):\*\*** Creates the database schema and manages database connections.

- **\*\*Requirement analyzer (`app/analyzer.py`):\*\*** Produces structured requirement-analysis output using deterministic rules.

- **\*\*Automated tests (`tests/test_api.py`):\*\*** Verify key API behaviors and error cases.

The URL shortener stores short-code mappings and aggregate analytics in SQLite. The requirement-analysis endpoint is a separate capability within the same application.

## 11. Engineering Notes, Risks, and Limitations

- **\*\*Database scalability:\*\*** SQLite keeps the prototype self-contained. It is not a claim of production-scale throughput or high availability. A production deployment should evaluate PostgreSQL or a managed database against its workload and operational requirements.

- **\*\*Short-code collisions:\*\*** Short codes are randomly generated, and uniqueness is enforced by a database constraint. The application retries a limited number of times if a code collision occurs.

- **\*\*Security and abuse prevention:\*\*** Authentication, authorization, rate limiting, abuse detection, URL expiry, custom aliases, and an administrative delete endpoint are not implemented.

- **\*\*Analytics and privacy:\*\*** Analytics are aggregate only. Visitor IP addresses and device fingerprints are not stored by this implementation.

- **\*\*Transport security:\*\*** A public production deployment should use HTTPS and appropriate security controls.

- **\*\*Monitoring and recovery:\*\*** Production readiness requires suitable monitoring, logging, backups, recovery procedures, and database migration practices.

- **\*\*Performance:\*\*** Load testing and capacity planning are not included in the current verification results.

- **\*\*Redirect behavior:\*\*** HTTP 302 is used because the permanence of the destination URL is unspecified.

- **\*\*Host and proxy handling:\*\*** The generated short URL uses the incoming request's base URL. A reverse proxy should configure trusted forwarded headers correctly, and public deployments should validate how externally visible URLs are constructed.

- **\*\*AI reliability:\*\*** AI-generated code and recommendations can be incorrect or incomplete. Engineers must review proposed changes, validate assumptions, inspect security implications, and run appropriate tests.

- **\*\*Requirement analyzer:\*\*** The analyzer uses deterministic rules rather than a live LLM. Its AI-assistance examples are illustrative prompts, not evidence of live AI execution.

## 12. Suggested Demonstration Sequence

1. Open `/docs` and explain the available endpoints.

2. Call `/health` and show the successful response.

3. Create a short URL using `POST /api/urls`.

4. Call `/r/{shortCode}` with redirects disabled and show the HTTP 302 response.

5. Query analytics and explain the click count and timestamps.

6. Restart the application and verify that the stored URL remains available.

7. Submit greenfield, brownfield, and ambiguous requirements to `/api/requirements/analyze`.

8. Run `python -m pytest -v` and explain what the tests validate.

9. Run `python scripts/run_api_demo.py` and demonstrate the end-to-end checks.

10. Explain the assumptions, engineering decisions, limitations, and production risks.

## 13. Engineering Summary

This project demonstrates a working Python/FastAPI prototype with persistent URL mappings, redirect-based click analytics, structured requirement analysis, automated tests, and a repeatable API demonstration.

AI-assisted engineering is demonstrated through requirement decomposition, implementation review, test design, debugging, and documentation support. The engineer remains responsible for reviewing generated suggestions, making implementation decisions, and validating the results.

The current implementation is a local prototype. Production deployment would require additional security, operational, scalability, and reliability work.
