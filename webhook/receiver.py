import hashlib
import hmac
import os
import uuid

from fastapi import FastAPI, Request, Header, HTTPException

from src.gstore.logging_config import configure_json_logging

app = FastAPI()
logger = configure_json_logging("gstore-webhook")


def _verify_github_signature(body: bytes, signature_header: str | None) -> None:
    """Verify the HMAC-SHA256 signature sent by GitHub.

    Raises :class:`fastapi.HTTPException` (403) when the signature is absent
    or does not match the shared secret stored in ``GITHUB_WEBHOOK_SECRET``.
    """
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
    if not secret:
        # If no secret is configured, skip verification (dev / test mode).
        logger.warning("GITHUB_WEBHOOK_SECRET is not set; skipping signature verification")
        return

    if not signature_header or not signature_header.startswith("sha256="):
        raise HTTPException(status_code=403, detail="Missing or malformed X-Hub-Signature-256 header")

    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")


@app.post("/webhook")
async def webhook_receiver(
    request: Request,
    x_github_event: str | None = Header(None),
    x_hub_signature_256: str | None = Header(None),
):
    body = await request.body()
    _verify_github_signature(body, x_hub_signature_256)

    payload = await request.json()
    trace_id = str(uuid.uuid4())
    logger.info("webhook_received", extra={
        "trace_id": trace_id,
        "event": x_github_event,
        "payload_keys": list(payload.keys()) if isinstance(payload, dict) else [],
    })
    # TODO: validate manifest, enqueue processing
    return {"status": "ok", "trace_id": trace_id}
