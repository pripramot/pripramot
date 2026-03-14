"""Tests for the GitHub webhook receiver.

Covers:
- Valid payload with correct HMAC signature.
- Valid payload when no secret is configured (dev mode).
- Rejected payload with wrong signature.
- Rejected payload with missing signature header.
"""

import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient

from webhook.receiver import app

client = TestClient(app, raise_server_exceptions=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SECRET = "test-webhook-secret"


def _sign(body: bytes, secret: str = _SECRET) -> str:
    """Return the ``sha256=<hex>`` signature for *body*."""
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def _post(payload: dict, secret: str | None = _SECRET, event: str = "push"):
    body = json.dumps(payload).encode()
    headers = {"X-GitHub-Event": event}
    if secret is not None:
        headers["X-Hub-Signature-256"] = _sign(body, secret)
    return client.post("/webhook", content=body, headers=headers)


# ---------------------------------------------------------------------------
# Happy-path
# ---------------------------------------------------------------------------

def test_webhook_valid_signature(monkeypatch):
    """Correct HMAC signature → 200 OK with trace_id."""
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", _SECRET)
    resp = _post({"ref": "refs/heads/main", "repository": {"name": "gstore"}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "trace_id" in data


def test_webhook_no_secret_configured(monkeypatch):
    """When GITHUB_WEBHOOK_SECRET is unset, any (or no) signature is accepted."""
    monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)
    body = json.dumps({"action": "opened"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "pull_request"},
    )
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Failure cases
# ---------------------------------------------------------------------------

def test_webhook_wrong_signature(monkeypatch):
    """Wrong HMAC signature → 403."""
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", _SECRET)
    body = json.dumps({"ref": "refs/heads/main"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=badhash",
        },
    )
    assert resp.status_code == 403


def test_webhook_missing_signature_header(monkeypatch):
    """Missing signature header when a secret IS configured → 403."""
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", _SECRET)
    body = json.dumps({"ref": "refs/heads/main"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={"X-GitHub-Event": "push"},
    )
    assert resp.status_code == 403
