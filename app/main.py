import os
import secrets
import sqlite3
import string
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.database import connect, initialize_database
from app.schemas import (
    CreateUrlRequest, CreateUrlResponse, AnalyticsResponse,
    RequirementRequest
)
from app.analyzer import analyze_requirement

DEFAULT_DB = os.getenv("URL_SHORTENER_DB", "data/urls.db")
ALPHABET = string.ascii_letters + string.digits

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def generate_code(length: int = 7) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def create_app(db_path: str = DEFAULT_DB) -> FastAPI:
    initialize_database(db_path)
    app = FastAPI(
        title="AI-Assisted Engineering Prototype",
        version="1.0.0",
        description="Python URL shortener plus a requirement analysis endpoint."
    )
    app.state.db_path = db_path

    @app.get("/health", tags=["Operations"])
    def health():
        return {"status": "healthy"}

    @app.post("/api/urls", response_model=CreateUrlResponse, status_code=201, tags=["URL Shortener"])
    def create_url(payload: CreateUrlRequest, request: Request):
        original_url = str(payload.url)
        created_at = utc_now()
        code = None
        with connect(app.state.db_path) as connection:
            for _ in range(5):
                candidate = generate_code()
                try:
                    connection.execute(
                        "INSERT INTO urls(short_code, original_url, created_at_utc) VALUES (?, ?, ?)",
                        (candidate, original_url, created_at)
                    )
                    code = candidate
                    break
                except sqlite3.IntegrityError as exc:
                    if "UNIQUE constraint failed: urls.short_code" not in str(exc):
                        raise
            if code is None:
                raise HTTPException(status_code=503, detail="Could not allocate a unique short code")
        base_url = str(request.base_url).rstrip("/")
        return CreateUrlResponse(
            shortCode=code,
            originalUrl=original_url,
            shortUrl=f"{base_url}/r/{code}",
            createdAtUtc=created_at
        )

    @app.get("/r/{short_code}", tags=["URL Shortener"], responses={302: {"description": "Redirect to original URL"}})
    def redirect_url(short_code: str):
        now = utc_now()
        with connect(app.state.db_path) as connection:
            row = connection.execute(
                "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
            ).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Short URL not found")
            connection.execute(
                "UPDATE urls SET click_count = click_count + 1, last_accessed_at_utc = ? WHERE short_code = ?",
                (now, short_code)
            )
        return RedirectResponse(url=row["original_url"], status_code=302)

    @app.get("/api/urls/{short_code}/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
    def get_analytics(short_code: str):
        with connect(app.state.db_path) as connection:
            row = connection.execute(
                "SELECT short_code, original_url, click_count, created_at_utc, last_accessed_at_utc "
                "FROM urls WHERE short_code = ?", (short_code,)
            ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        return AnalyticsResponse(
            shortCode=row["short_code"],
            originalUrl=row["original_url"],
            clickCount=row["click_count"],
            createdAtUtc=row["created_at_utc"],
            lastAccessedAtUtc=row["last_accessed_at_utc"]
        )

    @app.post("/api/requirements/analyze", tags=["Requirement Engineering"])
    def analyze(payload: RequirementRequest):
        return analyze_requirement(payload.requirement, payload.scenario_type)

    return app

app = create_app()
