# Architecture Overview

## 1. System Architecture

The prototype uses Python and FastAPI to expose URL-shortening, redirect, analytics, health-check, and requirement-analysis endpoints.

```text
                    Client / Swagger UI
                            |
                            v
                      FastAPI App
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
     URL Creation       Redirects          Analytics
   POST /api/urls      GET /r/{code}     GET /api/urls/
                                           {code}/analytics
          |                 |                  |
          +-----------------+------------------+
                            |
                            v
                    Database Layer
                    app/database.py
                            |
                            v
                      SQLite Database
                  URL mappings and click data


                    FastAPI App
                         |
                         +---- GET /health
                         |
                         +---- POST /api/requirements/analyze
                                      |
                                      v
                           Deterministic Requirement
                                  Analyzer
                              app/analyzer.py
                                      |
                                      v
                          Structured Engineering Plan
                    Assumptions, tasks, ambiguities,
                     validation checks, and risks
```

The URL-shortening endpoints use SQLite for persistent URL mappings and click analytics. The requirement-analysis endpoint uses deterministic rules to produce a structured engineering plan.

## 2. Main Components

### FastAPI application — `app/main.py`

- Defines the HTTP endpoints.
- Validates requests and structures responses through the application's schemas.
- Coordinates URL creation, redirects, analytics retrieval, and requirement analysis.
- Generates short URLs using the incoming request's base URL.

### Database layer — `app/database.py`

- Initializes the SQLite database schema.
- Creates the database directory when necessary.
- Opens and closes database connections.
- Supports persistent storage of URL mappings and aggregate click analytics.

### Request and response schemas — `app/schemas.py`

- Define the expected request structures.
- Validate incoming URL data.
- Structure API responses.

### Requirement analyzer — `app/analyzer.py`

- Accepts a software requirement and scenario type.
- Produces a structured engineering problem, assumptions, ambiguities, tasks, validation checks, risks, and AI-assistance examples.
- Uses deterministic rules rather than a live LLM.

### Automated tests — `tests/test_api.py`

- Verify core endpoint behavior.
- Check URL validation, redirects, analytics, error responses, and requirement-analysis scenarios.

## 3. Design Decisions

- **FastAPI:** Provides request validation, typed response models, and generated OpenAPI documentation.
- **SQLite:** Keeps the prototype easy to install and run without an external database service.
- **Random short codes:** Uses Python's cryptographically strong `secrets` module to generate codes. A database uniqueness constraint protects against duplicate codes, and collisions are retried a limited number of times.
- **HTTP 302 redirects:** Uses temporary redirects because the permanence of destination URLs has not been specified.
- **Aggregate analytics:** Records click counts and the last-accessed timestamp without storing visitor IP addresses or device fingerprints.
- **Deterministic requirement analysis:** Produces reproducible structured output without requiring an external LLM service.
- **Engineer-led AI assistance:** AI may help draft implementation ideas, tests, documentation, and reviews, but the engineer remains responsible for reviewing and validating changes.

## 4. Production Evolution

The current implementation is a local prototype. The following improvements should be evaluated before production deployment.

1. **Database:** Evaluate PostgreSQL or a managed relational database based on expected traffic, availability, and recovery requirements.
2. **Database operations:** Add schema migrations, appropriate connection management, and environment-specific configuration.
3. **Security and abuse prevention:** Introduce authentication, authorization, rate limits, abuse detection, and URL safety controls appropriate to the service.
4. **Observability:** Add structured logging, metrics, tracing, alerts, and separate health and readiness checks.
5. **Performance validation:** Load-test URL creation, redirects, and analytics updates under representative workloads.
6. **Caching:** Consider Redis for frequently accessed redirects if measurements demonstrate a performance benefit.
7. **High-volume analytics:** Consider a queue or event stream if analytics write contention becomes a bottleneck.
8. **CI/CD quality gates:** Add automated linting, type checks, tests, dependency and security scanning, and build verification.

These are proposed future improvements, not capabilities currently implemented by the prototype.

## 5. AI-Assisted Engineering Workflow

The workflow keeps the engineer accountable for technical decisions and final acceptance.

1. **Requirement analysis:** Identify goals, assumptions, ambiguities, and acceptance criteria.
2. **Design:** Review API contracts, data structures, component boundaries, and risks.
3. **Implementation:** Use AI assistance to explore implementation options and draft small code changes.
4. **Testing:** Develop positive, negative, boundary, and regression tests.
5. **Validation:** Run automated tests, execute the API demonstration, and inspect actual behavior.
6. **Documentation:** Record verified behavior, setup instructions, decisions, and limitations.
7. **Final review:** The engineer evaluates suggestions and accepts only changes supported by evidence.

The requirement analyzer in this prototype is deterministic and does not invoke a live LLM. AI-assisted development activities and prompt examples should not be presented as evidence of autonomous AI execution.