import hashlib
import re
from urllib.parse import urlsplit

from flask import Flask, request
from flask_limiter.util import get_remote_address


MINIMUM_PASSWORD_LENGTH = 14
MAXIMUM_PASSWORD_LENGTH = 128
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalise_email(value: str) -> str:
    return value.strip().casefold()


def is_valid_email(value: str) -> bool:
    return len(value) <= 254 and bool(EMAIL_PATTERN.fullmatch(value))


def validate_new_password(password: str) -> None:
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must contain at least {MINIMUM_PASSWORD_LENGTH} characters."
        )
    if len(password) > MAXIMUM_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must contain no more than {MAXIMUM_PASSWORD_LENGTH} characters."
        )


def is_safe_local_url(candidate: str | None) -> bool:
    if not candidate or "\\" in candidate or "%5c" in candidate.casefold():
        return False

    parsed = urlsplit(candidate)
    return (
        not parsed.scheme
        and not parsed.netloc
        and parsed.path.startswith("/")
        and not parsed.path.startswith("//")
    )


def login_rate_limit_key() -> str:
    email = normalise_email(request.form.get("email", ""))
    email_digest = hashlib.sha256(email.encode("utf-8")).hexdigest()[:16]
    return f"{get_remote_address()}:{email_digest}"


def register_security_headers(app: Flask) -> None:
    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "base-uri 'self'; "
            "connect-src 'self'; "
            "font-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "img-src 'self' data:; "
            "object-src 'none'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' https://cdn.jsdelivr.net"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), geolocation=(), microphone=(), payment=()"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        if request.endpoint != "static":
            response.headers["Cache-Control"] = "no-store"

        if app.config.get("APP_ENV") == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response
