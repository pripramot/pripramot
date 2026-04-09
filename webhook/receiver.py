import hashlib
import hmac
import os
import uuid

from fastapi import FastAPI, Header, HTTPException, Request

from src.gstore.logging_config import configure_json_logging

app = FastAPI()
logger = configure_json_logging("gstore-webhook")


def _verify_github_signature(body: bytes, signature_header: str | None) -> None:
    """ตรวจสอบลายเซ็น HMAC-SHA256 จาก GitHub Webhook

    Args:
        body: Raw request body bytes.
        signature_header: Value of the X-Hub-Signature-256 header.

    Raises:
        HTTPException: 403 if the signature is missing or invalid.
    """
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(status_code=403, detail="Webhook secret not configured")
    if not signature_header or not signature_header.startswith("sha256="):
        raise HTTPException(status_code=403, detail="Missing or malformed signature")
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(status_code=403, detail="Invalid signature")


@app.post("/webhook")
async def webhook_receiver(
    request: Request,
    x_github_event: str | None = Header(None),
    x_hub_signature_256: str | None = Header(None),
) -> dict:
    """รับและตรวจสอบ GitHub webhook payload

    Args:
        request: FastAPI request object.
        x_github_event: GitHub event type header.
        x_hub_signature_256: HMAC-SHA256 signature header from GitHub.

    Returns:
        JSON response with status and trace_id.
    """
    body = await request.body()
    _verify_github_signature(body, x_hub_signature_256)
    payload = await request.json()
    trace_id = str(uuid.uuid4())
    logger.info(
        "webhook_received",
        extra={
            "trace_id": trace_id,
            "event": x_github_event,
            "payload_keys": list(payload.keys()),
        },
    )
    # TODO: validate manifest, enqueue processing
    return {"status": "ok", "trace_id": trace_id}
