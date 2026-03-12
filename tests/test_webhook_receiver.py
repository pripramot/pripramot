import hashlib
import hmac
import json
import os

import pytest
from fastapi.testclient import TestClient

from webhook.receiver import app


def _sign(payload: bytes, secret: str = "test-secret-key") -> str:
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


@pytest.fixture(autouse=True)
def _set_webhook_secret(monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "test-secret-key")


@pytest.fixture()
def client():
    return TestClient(app)


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
    client = TestClient(app)

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
