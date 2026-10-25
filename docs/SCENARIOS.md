# Example Scenarios

This document demonstrates how an engineer can use AI assistance to break down software requirements, identify uncertainties, plan implementation, and validate results.

The requirement-analysis endpoint produces structured output for greenfield, brownfield, and ambiguous scenarios using deterministic rules. The AI prompts below are examples of how an engineer could use ChatGPT or GitHub Copilot during development; they do not indicate that the prototype invokes a live LLM.

## 1. Greenfield Scenario

**Input requirement**

"Build a scalable URL shortener service with APIs, persistence, and analytics."

### Task breakdown

1. Clarify expected traffic, availability, security, and recovery requirements.
2. Define API contracts and the data model.
3. Implement URL creation and short-code generation.
4. Implement redirects and click analytics.
5. Add automated tests for success, validation failures, and unknown codes.
6. Document setup instructions, assumptions, and engineering risks.

### Task Dependencies

| Task | Depends on | Reason |
|---|---|---|
| Clarify requirements and acceptance criteria | None | Establish the scope and measurable outcomes. |
| Define API contracts and data model | Requirements clarification | The interfaces and data model depend on agreed requirements. |
| Implement URL creation and persistence | API contracts and data model | Implementation follows the agreed interface and schema. |
| Implement redirects and analytics | Data model and URL persistence | Redirects and click tracking depend on stored URL mappings. |
| Add automated tests | API contracts and implementation | Tests verify the expected behavior and error cases. |
| Document setup, assumptions, and risks | Verified implementation and test results | Documentation should reflect actual behavior and known limitations. |

### AI assistance

Example prompt:

"Break this requirement into implementation tasks, API contracts, data-model suggestions, acceptance criteria, and negative test cases. Clearly identify assumptions and do not invent unstated requirements."

An engineer reviews the proposed design, checks the implementation against the requirements, and validates the generated suggestions.

### Validation

- Run `python -m pytest -v`.
- Create a short URL and verify the HTTP 201 response.
- Follow the redirect with automatic redirects disabled and verify HTTP 302 and the destination.
- Query analytics and verify the click count.
- Restart the application and confirm that the URL mapping persists.
- Review documented security and scalability limitations.

### Prototype evidence

The current prototype implements URL creation, redirects, persistent storage, click analytics, and automated tests. The recorded local verification run reported 11 passing tests, and the API demo passed all checks.

Persistence across an application restart was subsequently checked using a dedicated URL. The same short code, original URL, creation timestamp, and click count were returned before and after the restart. Evidence is recorded in `evidence/persistence-check.txt`.

Production scalability has not been established through load testing.

## 2. Brownfield Scenario

**Input requirement**

"Add a `created_by` field to the existing URL shortener API without breaking existing clients."

### Task breakdown

1. Inspect the existing routes, schemas, database schema, and automated tests.
2. Clarify whether `created_by` is mandatory, optional, or derived from an authenticated user.
3. Define a backward-compatible API and database change.
4. Implement the smallest suitable code and schema changes.
5. Add regression tests for existing clients and tests for the new field.
6. Update the API contract and release documentation.

### AI assistance

Example prompt:

"Review the existing URL shortener implementation and propose the smallest backward-compatible change to add a `created_by` field. Identify schema migration concerns, API compatibility risks, and regression tests. Do not assume authentication or a user identity source exists unless the code confirms it."

The engineer verifies the proposed changes against the actual source code and reviews every modification before acceptance.

### Validation

- Confirm that existing URL creation and redirect flows still work.
- Confirm that existing clients can continue using the previous request format if backward compatibility requires it.
- Test the new field's validation and persistence behavior.
- Test existing analytics and unknown-code behavior for regressions.
- Run the complete automated test suite.
- Update documentation to match the implemented contract.

### Prototype evidence

This is a proposed brownfield change scenario. The current prototype does not implement a `created_by` field. The scenario describes how an engineer would approach the change; it is not evidence that the feature has already been implemented or tested.

No backward-compatibility or regression results for the `created_by` change are claimed because that change has not been implemented in the current prototype.

## 3. Ambiguous Scenario

**Input requirement**

"Make our service better for customers."

### Clarification questions

- Which customer problem are we trying to solve?
- Which user journeys or business processes are affected?
- What measurable outcome defines success?
- What response-time and availability targets are required?
- What security, privacy, and data-retention constraints apply?
- What traffic volume and peak workload should the service support?
- Who will approve the acceptance criteria?

### Task breakdown

1. Extract the facts and goals explicitly stated in the request.
2. Identify missing information and conflicting assumptions.
3. Generate prioritized clarification questions.
4. Obtain stakeholder decisions and record approved assumptions.
5. Define measurable acceptance criteria.
6. Propose a design and implementation plan only after the requirements are sufficiently clear.
7. Validate the implementation against the agreed criteria.

### AI assistance

Example prompt:

"Analyze this ambiguous software requirement. Separate known facts from assumptions, list the highest-priority clarification questions, and suggest possible interpretations with their trade-offs. Do not silently select an interpretation or present assumptions as confirmed requirements."

AI can help organize questions and explore options, but stakeholders and engineers remain responsible for the decisions.

### Validation

- Obtain stakeholder-approved acceptance criteria before implementation.
- Ensure each acceptance criterion has a corresponding verification method.
- Record unresolved questions and assumptions.
- Test the implementation against the agreed criteria.
- Revisit the design if requirements change.
- Maintain a traceability record linking each approved requirement to its implementation task, acceptance criterion, and verification result.

### Prototype evidence

The current requirement-analysis endpoint accepts ambiguous requirements and returns structured tasks, assumptions, ambiguities, validation checks, and risks. Its output is generated by deterministic rules and does not automatically obtain stakeholder approval or implement the proposed tasks.

## 4. Cross-Scenario Engineering Principles

Across all three scenarios:

- **Requirement clarity:** Separate stated facts, assumptions, and unknowns.
- **Engineer ownership:** Keep humans accountable for design decisions and final acceptance.
- **AI-assisted development:** Use AI suggestions as drafts that require review and validation.
- **Test-driven validation:** Verify positive, negative, boundary, and regression cases as appropriate.
- **Traceability:** Connect requirements to tasks, acceptance criteria, tests, and documented outcomes.
- **Honest reporting:** Distinguish implemented and tested capabilities from proposed changes and future improvements.

The goal is to demonstrate a repeatable engineering workflow in which AI can support analysis and development while the engineer remains responsible for correctness, security, and quality.
