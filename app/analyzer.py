from app.schemas import RequirementAnalysisResponse

def classify_requirement(requirement: str, requested_type: str | None = None) -> str:
    if requested_type:
        return requested_type
    text = requirement.lower()
    if any(word in text for word in ("existing", "refactor", "bug", "enhance", "currently", "modify")):
        return "brownfield"
    if any(word in text for word in ("scalable", "build", "create", "develop", "new service", "implement")):
        return "greenfield"
    return "ambiguous"

def analyze_requirement(requirement: str, requested_type: str | None = None):
    scenario = classify_requirement(requirement, requested_type)
    ambiguities = [
        "Expected traffic and peak requests per second are not specified.",
        "Availability, recovery objectives, and deployment environment are not specified.",
        "Authentication, authorization, and rate-limit requirements are not specified."
    ]
    assumptions = [
        "Use Python with FastAPI for REST endpoints.",
        "Use SQLite for a local, reproducible prototype; production should use a managed database.",
        "Accept absolute HTTP/HTTPS URLs only.",
        "Record aggregate click counts without storing visitor IP addresses."
    ]
    if scenario == "brownfield":
        problem = "Safely change an existing system while preserving current behavior and adding regression coverage."
        tasks = [
            {"id": 1, "task": "Inspect existing behavior, interfaces, and tests", "depends_on": [], "ai_assistance": "Summarize code and propose regression cases; engineer verifies against source."},
            {"id": 2, "task": "Define backward-compatible change and acceptance criteria", "depends_on": [1], "ai_assistance": "Draft change plan and identify compatibility risks."},
            {"id": 3, "task": "Implement the smallest modular code change", "depends_on": [2], "ai_assistance": "Suggest implementation/refactoring; engineer reviews every change."},
            {"id": 4, "task": "Run regression, unit, and integration tests", "depends_on": [3], "ai_assistance": "Suggest missing edge cases and diagnose failures."},
            {"id": 5, "task": "Update documentation and release notes", "depends_on": [4], "ai_assistance": "Draft docs based on verified behavior."}
        ]
    elif scenario == "ambiguous":
        problem = "Turn an underspecified request into a testable engineering problem by documenting unknowns and obtaining decisions before implementation."
        tasks = [
            {"id": 1, "task": "Extract stated goals, actors, constraints, and acceptance criteria", "depends_on": [], "ai_assistance": "Structure the request; engineer confirms interpretation."},
            {"id": 2, "task": "List ambiguities and ask prioritized clarification questions", "depends_on": [1], "ai_assistance": "Generate questions about scale, security, data, and failure behavior."},
            {"id": 3, "task": "Record provisional assumptions and decision owners", "depends_on": [2], "ai_assistance": "Draft assumptions; stakeholder approves them."},
            {"id": 4, "task": "Create a small testable design and implementation plan", "depends_on": [3], "ai_assistance": "Compare options and identify trade-offs."},
            {"id": 5, "task": "Validate against agreed acceptance criteria", "depends_on": [4], "ai_assistance": "Suggest test cases; engineer verifies expected outcomes."}
        ]
    else:
        problem = "Implement the requested capability as a modular service with documented APIs, persistent data, automated tests, and operational safeguards."
        tasks = [
            {"id": 1, "task": "Clarify requirements and acceptance criteria", "depends_on": [], "ai_assistance": "Draft assumptions and questions; engineer confirms scope."},
            {"id": 2, "task": "Design API schemas and persistence model", "depends_on": [1], "ai_assistance": "Propose endpoint contracts and schema; engineer reviews compatibility."},
            {"id": 3, "task": "Implement service logic and persistence", "depends_on": [2], "ai_assistance": "Generate small code units; engineer checks correctness and security."},
            {"id": 4, "task": "Create unit and API integration tests", "depends_on": [2, 3], "ai_assistance": "Suggest boundary and negative cases; engineer verifies assertions."},
            {"id": 5, "task": "Run tests, review risks, and document setup", "depends_on": [4], "ai_assistance": "Help interpret failures and draft docs; engineer validates evidence."}
        ]
    risks = [
        {"risk": "AI-generated code may be incorrect or incomplete", "mitigation": "Review diffs, run automated tests, and manually inspect edge cases."},
        {"risk": "Prototype database may not meet production throughput or availability", "mitigation": "Use PostgreSQL or a managed database after load and operational requirements are defined."},
        {"risk": "Abuse through malicious or excessive URL creation", "mitigation": "Add authentication, rate limits, abuse detection, and operational monitoring before public production use."}
    ]
    checks = [
        "Validate request schemas and reject malformed or unsupported URLs.",
        "Test success, not-found, conflict, and error responses.",
        "Verify persistence survives application restart.",
        "Verify redirect destination and click analytics behavior.",
        "Review security, privacy, logging, and performance assumptions."
    ]
    ai = [
        {"stage": "Requirement analysis", "prompt_example": "Convert this requirement into goals, assumptions, ambiguities, and acceptance criteria. Do not invent unstated constraints."},
        {"stage": "Implementation", "prompt_example": "Propose a small, modular FastAPI implementation. Explain edge cases and security concerns."},
        {"stage": "Testing", "prompt_example": "Generate positive, negative, boundary, and regression tests. State what each test proves."},
        {"stage": "Review", "prompt_example": "Review this change for correctness, security, performance, and missing tests. Separate facts from assumptions."}
    ]
    return RequirementAnalysisResponse(
        requirement=requirement,
        scenario_type=scenario,
        engineering_problem=problem,
        assumptions=assumptions,
        ambiguities=ambiguities,
        tasks=tasks,
        validation_checks=checks,
        risks=risks,
        ai_assistance=ai,
        note="This analyzer uses deterministic rules, not a live LLM. AI prompt examples document how an engineer can use ChatGPT/Copilot during implementation; generated output must be reviewed and tested."
    )
