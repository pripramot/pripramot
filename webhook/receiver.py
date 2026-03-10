from fastapi import FastAPI, Request, Header
import uuid
from src.gstore.logging_config import configure_json_logging

app = FastAPI()
logger = configure_json_logging("gstore-webhook")

@app.post("/webhook")
async def webhook_receiver(request: Request, x_github_event: str | None = Header(None)):
    payload = await request.json()
    trace_id = str(uuid.uuid4())
    logger.info("webhook_received", extra={
        "trace_id": trace_id,
        "event": x_github_event,
        "payload_keys": list(payload.keys())
    })
    # TODO: validate manifest, enqueue processing
    return {"status": "ok", "trace_id": trace_id}
