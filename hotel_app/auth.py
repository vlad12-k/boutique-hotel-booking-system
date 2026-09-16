import secrets
from datetime import datetime, timezone

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from hotel_app.extensions import db, limiter, login_manager
from hotel_app.models import SecurityAuditEvent, StaffAccount
from hotel_app.security import (
    MAXIMUM_PASSWORD_LENGTH,
    is_safe_local_url,
    is_valid_email,
    login_rate_limit_key,
    normalise_email,
)


_DUMMY_PASSWORD_HASH = generate_password_hash(
    secrets.token_urlsafe(32),
    method="scrypt",
)

auth = Blueprint("auth", __name__)


def record_security_event(
    event_type: str,
    outcome: str,
    staff_account_id: int | None = None,
) -> None:
    db.session.add(
        SecurityAuditEvent(
            staff_account_id=staff_account_id,
            event_type=event_type,
            outcome=outcome,
        )
    )


def login_limit() -> str:
    return current_app.config["LOGIN_RATE_LIMIT"]


def login_ip_limit() -> str:
    return current_app.config["LOGIN_IP_RATE_LIMIT"]


@login_manager.user_loader
def load_user(user_id: str):
    try:
        account_id = int(user_id)
    except (TypeError, ValueError):
        return None
    return db.session.get(StaffAccount, account_id)


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit(login_ip_limit, methods=["POST"])
@limiter.limit(
    login_limit,
    methods=["POST"],
    key_func=login_rate_limit_key,
)
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    requested_next = request.values.get("next")
    safe_next = requested_next if is_safe_local_url(requested_next) else None

    if request.method == "POST":
        email = normalise_email(request.form.get("email", ""))
        password = request.form.get("password", "")
        account = None

        if is_valid_email(email):
            account = StaffAccount.query.filter_by(email=email).one_or_none()

        if len(password) > MAXIMUM_PASSWORD_LENGTH:
            check_password_hash(_DUMMY_PASSWORD_HASH, "invalid-password")
            password_valid = False
        else:
            password_hash = account.password_hash if account else _DUMMY_PASSWORD_HASH
            password_valid = check_password_hash(password_hash, password)

        if account is None or not password_valid or not account.is_active:
            record_security_event(
                "login_failed",
                "denied",
                account.id if account else None,
            )
            db.session.commit()
            flash("Invalid email or password.", "danger")
            return render_template("login.html", next_url=safe_next), 401

        session.clear()
        login_user(account, remember=False, fresh=True)
        session.permanent = True
        account.last_login_at = datetime.now(timezone.utc)
        record_security_event("login_succeeded", "success", account.id)
        db.session.commit()

        return redirect(safe_next or url_for("dashboard"))

    return render_template("login.html", next_url=safe_next)


@auth.post("/logout")
@login_required
def logout():
    account_id = current_user.id
    logout_user()
    session.clear()
    record_security_event("logout", "success", account_id)
    db.session.commit()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
