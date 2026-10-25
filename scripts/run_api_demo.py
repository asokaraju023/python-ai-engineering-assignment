import json
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = PROJECT_ROOT / "samples"


def load_json(filename: str) -> dict:
    """Load a JSON request body from the samples directory."""
    path = SAMPLES_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_response(name: str, response: httpx.Response,
                   expected_status: int) -> dict | None:
    """Print the result and validate the HTTP status."""
    print(f"\n--- {name} ---")
    print(f"Status: {response.status_code}")

    try:
        body = response.json()
        print(json.dumps(body, indent=2))
    except ValueError:
        body = None
        print(response.text)

    if response.status_code != expected_status:
        raise RuntimeError(
            f"{name}: expected HTTP {expected_status}, "
            f"received {response.status_code}"
        )

    print("Result: PASS")
    return body


def main() -> None:
    with httpx.Client(
        base_url=BASE_URL,
        timeout=10.0,
        follow_redirects=False,
    ) as client:
        # 1. Check service health.
        response = client.get("/health")
        check_response("Health check", response, 200)

        # 2. Create a short URL from the saved JSON file.
        create_request = load_json("create_url.json")
        response = client.post("/api/urls", json=create_request)
        created = check_response("Create URL", response, 201)

        if not isinstance(created, dict) or not created.get("shortCode"):
            raise RuntimeError("Create URL response has no shortCode")

        short_code = created["shortCode"]

        # 3. Request a redirect without following it automatically.
        response = client.get(f"/r/{short_code}")
        if response.status_code != 302:
            raise RuntimeError(
                f"Redirect: expected HTTP 302, "
                f"received {response.status_code}"
            )

        print("\n--- Redirect ---")
        print(f"Status: {response.status_code}")
        print(f"Location: {response.headers.get('location')}")
        print("Result: PASS")

        # 4. Check analytics for the newly created URL.
        response = client.get(
            f"/api/urls/{short_code}/analytics"
        )
        analytics = check_response("Analytics", response, 200)

        if not isinstance(analytics, dict):
            raise RuntimeError("Analytics response is not a JSON object")

        if analytics.get("clickCount") != 1:
            raise RuntimeError(
                "Expected clickCount to be 1 after one redirect"
            )

        # 5. Analyze all three saved requirement scenarios.
        scenarios = [
            ("greenfield.json", "greenfield"),
            ("brownfield.json", "brownfield"),
            ("ambiguous.json", "ambiguous"),
        ]

        for filename, expected_type in scenarios:
            payload = load_json(filename)
            response = client.post(
                "/api/requirements/analyze",
                json=payload,
            )
            result = check_response(
                f"Requirement analysis: {expected_type}",
                response,
                200,
            )

            if not isinstance(result, dict):
                raise RuntimeError(
                    f"{expected_type}: response is not a JSON object"
                )

            if result.get("scenario_type") != expected_type:
                raise RuntimeError(
                    f"{expected_type}: unexpected scenario_type"
                )

            if not result.get("tasks"):
                raise RuntimeError(
                    f"{expected_type}: no tasks returned"
                )

    print("\nAll API demo checks passed.")


if __name__ == "__main__":
    main()