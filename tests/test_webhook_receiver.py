import hashlib
import hmac
import json
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _set_webhook_secret(monkeypatch):
    """Ensure a known webhook secret is set for every test."""
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "test-secret-key")
    # Re-import so the module picks up the new env var.
    import importlib
    import webhook.receiver as mod

    importlib.reload(mod)
    yield mod


@pytest.fixture()
def client(_set_webhook_secret):
    return TestClient(_set_webhook_secret.app)


def _sign(payload: bytes, secret: str = "test-secret-key") -> str:
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


# --- Valid requests ---


def test_webhook_valid_signature(client):
    body = json.dumps({"action": "push"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": _sign(body),
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "trace_id" in data


# --- Invalid requests ---


def test_webhook_missing_signature(client):
    body = json.dumps({"action": "push"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
        },
    )
    assert resp.status_code == 403


def test_webhook_wrong_signature(client):
    body = json.dumps({"action": "push"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=invalidsignature",
        },
    )
    assert resp.status_code == 403


def test_webhook_invalid_json(client):
    body = b"not json"
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": _sign(body),
        },
    )
    assert resp.status_code == 400


def test_webhook_no_secret_configured(monkeypatch):
    """When GITHUB_WEBHOOK_SECRET is empty, all requests should be rejected."""
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "")
    import importlib
    import webhook.receiver as mod

    importlib.reload(mod)
    client = TestClient(mod.app)

    body = json.dumps({"action": "push"}).encode()
    resp = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": _sign(body, ""),
        },
    )
    assert resp.status_code == 403
