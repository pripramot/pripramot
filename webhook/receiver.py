import hashlib
import hmac
import json
import os
import uuid

from fastapi import FastAPI, HTTPException, Request, Header

from src.gstore.logging_config import configure_json_logging

app = FastAPI()
logger = configure_json_logging("gstore-webhook")


def _get_webhook_secret() -> str:
    return os.environ.get("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload_body: bytes, signature_header: str | None) -> bool:
    """Verify the HMAC-SHA256 signature from GitHub webhook."""
    secret = _get_webhook_secret()
    if not secret:
        return False
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(
        secret.encode("utf-8"),
        payload_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature_header)


@app.post("/webhook")
async def webhook_receiver(
    request: Request,
    x_github_event: str | None = Header(None),
    x_hub_signature_256: str | None = Header(None),
):
    body = await request.body()

    # Verify HMAC signature (mandatory per security policy)
    if not verify_signature(body, x_hub_signature_256):
        logger.warning(
            "webhook_signature_invalid",
            extra={"event": x_github_event},
        )
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    trace_id = str(uuid.uuid4())
    logger.info("webhook_received", extra={
        "trace_id": trace_id,
        "event": x_github_event,
        "payload_keys": list(payload.keys()),
    })
    return {"status": "ok", "trace_id": trace_id}
