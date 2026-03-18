import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient

from webhook.receiver import app

SECRET = "test-secret"


@pytest.fixture()
def client():
    """สร้าง TestClient ใหม่สำหรับแต่ละ test."""
    return TestClient(app)


def _make_signature(body: bytes, secret: str = SECRET) -> str:
    """สร้าง HMAC-SHA256 signature สำหรับใช้ใน tests."""
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_webhook_valid_signature(client, monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", SECRET)
    payload = json.dumps({"action": "push"}).encode()
    sig = _make_signature(payload)
    response = client.post(
        "/webhook",
        content=payload,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": sig,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "trace_id" in data


def test_webhook_missing_signature(client, monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", SECRET)
    payload = json.dumps({"action": "push"}).encode()
    response = client.post(
        "/webhook",
        content=payload,
        headers={"Content-Type": "application/json", "X-GitHub-Event": "push"},
    )
    assert response.status_code == 403


def test_webhook_invalid_signature(client, monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", SECRET)
    payload = json.dumps({"action": "push"}).encode()
    response = client.post(
        "/webhook",
        content=payload,
        headers={
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=deadbeef",
        },
    )
    assert response.status_code == 403


def test_webhook_no_secret_configured(client, monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "")
    payload = json.dumps({"action": "push"}).encode()
    sig = _make_signature(payload)
    response = client.post(
        "/webhook",
        content=payload,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": sig,
        },
    )
    assert response.status_code == 403
