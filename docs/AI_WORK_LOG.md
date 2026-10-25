# AI Engineering Work Log

## Purpose

This log records how AI assistance was used during implementation, review, debugging, testing, and documentation. It distinguishes AI suggestions from accepted engineering decisions and records how changes were validated.

## Engineering Activity Log

| Activity | AI assistance / question | Engineering decision | Validation evidence | Status |
|---|---|---|---|---|
| API implementation review | Review the API implementation for correctness, validation, and error handling. | Retain the FastAPI endpoint structure and verify expected status codes and errors. | Automated API tests and demonstration script. | Validated in recorded test run |
| Database connection management | Review SQLite connection lifecycle and cleanup. | Use controlled connection management and ensure connections are closed. | Automated test suite; persistence behavior was also tested. | Changes implemented; tests passed |
| Database error handling | Review how database integrity errors are handled. | Handle expected unique-code conflicts without hiding unrelated integrity errors. | `test_non_unique_integrity_error_is_not_swallowed`. | Passed |
| Requirement analysis | Review how greenfield, brownfield, and ambiguous requirements can be represented as structured engineering tasks. | Keep the current analyzer deterministic and document its limitations. | Three requirement-analysis tests and API demonstration. | Passed |
| API documentation | Review endpoint contracts, request examples, responses, and errors. | Align documentation with implemented API behavior. | Compare examples against the running application and tests. | Final review required |
| Architecture documentation | Explain components, data flow, and design trade-offs. | Document the current architecture without claiming unimplemented infrastructure. | Compare documentation with the source code. | Final review required |
| Validation and risk documentation | Identify verified tests, known limitations, and remaining risks. | Separate demonstrated behavior from production-readiness assumptions. | Test results, demo output, and source review. | Final review required |

## Validation Record
**Last validation date:** 25 October 2026

### Automated tests

**Command**

```powershell
python -m pytest -v
```

**Latest recorded result:** 11 passed, 0 failed.

The run also reported a Starlette deprecation warning involving the installed HTTP client. The warning did not cause the tests to fail.

### API demonstration

**Command**

```powershell
python scripts/run_api_demo.py
```

**Latest recorded result:** All API demonstration checks passed.

Verified operations included the health check, URL creation, redirection, analytics, and greenfield, brownfield, and ambiguous requirement analysis.

### Evidence Location

Evidence files are stored in the project's `evidence/` directory.

- Automated test evidence: `evidence/pytest-results.txt`
- API demonstration evidence: `evidence/api-demo-results.txt`
- Persistence-across-restart evidence: `evidence/persistence-check.txt` — records the short code, original URL, click count, and creation timestamp observed before and after the restart.

## Evidence to Attach or Record

For each significant engineering activity, record:

- Date of the activity.
- Actual prompt or question used, where available.
- AI suggestion or generated output.
- Accepted, modified, or rejected decision.
- Files changed.
- Test command and result.
- Relevant API response, screenshot, or test output.

Do not reconstruct an exact historical prompt from memory. If the original wording is unavailable, record a concise description of the activity instead.

## Engineering Review Principles

- AI-generated code and recommendations are not accepted without review.
- Test results are recorded only after the tests have actually been run.
- Unimplemented functionality is documented as a limitation or future improvement.
- Any discrepancy between the implementation and documentation must be resolved before submission.
- The engineer remains responsible for correctness, security, and final acceptance.