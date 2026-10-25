# AI-Assisted Software Engineering — Engineering Summary

## 1. Objective

The objective of this prototype is to demonstrate how AI-assisted software engineering can help transform software requirements into structured engineering tasks and a working software implementation. The mandatory use case is a scalable URL shortener service with APIs, persistence, and analytics.

The implementation combines a runnable FastAPI application with a requirement-analysis endpoint that produces structured engineering guidance for greenfield, brownfield, and ambiguous requirements.

## 2. Solution Overview

The prototype uses Python, FastAPI, SQLite, and Pydantic-based request validation.

Key capabilities include:

- **URL creation:** Accepts a destination URL and generates a unique short code.
- **Persistence:** Stores shortened URLs and click counts in SQLite.
- **Redirection:** Redirects requests to the original destination using HTTP 302.
- **Analytics:** Provides aggregate click-count information for a short URL.
- **Requirement analysis:** Accepts a software requirement and returns structured assumptions, ambiguities, tasks, dependencies, validation checks, and risks for different requirement scenarios.

The requirement analyzer currently uses deterministic, rule-based logic. It does not call a live large language model (LLM). AI assistance was used during the engineering and review process, rather than being represented as an autonomous AI system inside the application.

## 3. Architecture and Engineering Decisions

The application is organized into separate modules for API handling, database access, request/response schemas, and requirement analysis.

Important design decisions include:

- **FastAPI:** Provides a lightweight HTTP API and interactive API documentation.
- **SQLite:** Keeps the prototype self-contained and allows data persistence across application restarts.
- **Pydantic validation:** Checks incoming request data before processing.
- **Unique short codes:** Uses secure random code generation, database uniqueness constraints, and bounded retry handling.
- **Database connection lifecycle:** Uses controlled connection cleanup to reduce the risk of leaving connections open.
- **Specific error handling:** Handles expected database uniqueness conflicts without swallowing unrelated integrity errors.
- **Deterministic requirement analysis:** Makes the current analysis output repeatable and easier to test.

SQLite is appropriate for this local prototype, but a production-scale deployment would require further evaluation of database concurrency, capacity, availability, and operational requirements.

## 4. AI-Assisted Engineering Activities

AI assistance was used as a development and review aid across the following activities:

- Reviewing implementation choices and identifying potential error-handling issues.
- Refining database connection management and SQLite integrity-error handling.
- Reviewing API contracts, validation behavior, and expected error responses.
- Improving the README and architecture, scenario, validation, and risk documentation.
- Interpreting automated test results and identifying areas requiring further verification.
- Structuring greenfield, brownfield, and ambiguous requirement examples.

AI-generated suggestions were treated as proposals rather than automatically accepted changes. Engineering decisions were reviewed against the existing implementation, and the resulting behavior was checked through automated tests and API demonstrations.

**Important distinction:** The current requirement-analysis endpoint uses deterministic rules. It should not be described as live LLM-generated analysis. The project demonstrates AI-assisted engineering practices; it does not claim autonomous software development.

## 5. Validation and Test Evidence

### Automated Tests

The latest recorded test run was executed using:

```powershell
python -m pytest -v
```

**Result: 11 passed, 0 failed.**

The tests cover:

- Health endpoint behavior.
- URL creation and persistence.
- Invalid URL and unsupported scheme rejection.
- Database integrity-error handling.
- Redirect behavior and click-count updates.
- Unknown short-code and analytics responses.
- Greenfield, brownfield, and ambiguous requirement analysis.

### API Demonstration

The following command completed successfully:

```powershell
python scripts/run_api_demo.py
```

| Operation | Verified result |
|---|---|
| Health check | HTTP 200 |
| Create short URL | HTTP 201 |
| Redirect to original URL | HTTP 302 |
| Retrieve analytics | HTTP 200; click count was 1 |
| Greenfield analysis | HTTP 200 |
| Brownfield analysis | HTTP 200 |
| Ambiguous analysis | HTTP 200 |

### Additional Verification and Warning

Persistence across an application restart was verified in an earlier test session. It should be rerun if fresh evidence is required for the final demonstration.

The latest test run also reported a Starlette deprecation warning involving the installed HTTP client. It did not prevent the tests from passing, but dependency compatibility should be reviewed separately.

These results demonstrate the tested behavior of the local prototype. They do not establish production-scale performance, availability, or scalability.

## 6. Risks and Limitations

The current prototype has the following limitations:

- SQLite is suitable for the prototype but has not been validated for production-scale concurrent workloads.
- Authentication, authorization, rate limiting, and abuse prevention have not been implemented.
- Load testing, production monitoring, backup/recovery testing, and deployment-readiness validation remain outstanding.
- The requirement analyzer uses predefined rules and cannot provide the open-ended reasoning of a live LLM.
- The prototype has not been demonstrated to meet a quantified scalability or performance target.
- The current redirect behavior is HTTP 302; alternative redirect semantics should be selected based on confirmed requirements.

These limitations distinguish verified prototype capabilities from production-readiness claims.

## 7. Next Steps

Before final submission:

1. Rerun the automated tests and API demonstration script.
2. Verify that the README setup instructions work from a clean environment.
3. Review API request/response examples against the actual application behavior.
4. Capture evidence of successful tests and API responses.
5. Maintain an AI engineering work log recording prompts, suggestions, accepted changes, rejected suggestions, and validation evidence.
6. Confirm any additional scalability, security, or deployment expectations with the client before expanding the implementation.

## 8. Engineering Accountability

AI assistance supported implementation review, debugging, testing, and documentation. The final engineering outcome remains subject to human review and validation. Claims in this summary are limited to implemented functionality and recorded test results; proposed improvements and unverified production characteristics are identified as limitations or future work.