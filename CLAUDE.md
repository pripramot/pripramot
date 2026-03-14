# CLAUDE.md — GSTORE Instructions for Claude Code

> Claude reads this file automatically when you open this repository.
> Follow every rule here before writing a single line of code.

---

## Project Identity

**GSTORE** is a Tauri v2 desktop application for high-speed file search and forensic analysis.

| Component | Language | Entry point |
|-----------|----------|-------------|
| Desktop UI | React 18 / JSX | `frontend/src/App.jsx` |
| Core engine | Rust (Tokio) | `src-tauri/src/lib.rs` |
| Webhook service | Python (FastAPI) | `webhook/receiver.py` |
| Manifest validator | Python | `src/gstore/manifest_validator.py` |
| Tests | Python (pytest) | `tests/` |

---

## Commands — Run These, Nothing Else

```bash
# Run all tests (do this before AND after any code change)
python -m pytest tests/ -v

# Install / refresh Python dependencies
pip install -r requirements.txt

# Format Python code (required before committing)
black src/ webhook/ tests/

# Lint Python code
flake8 src/ webhook/ tests/

# Start webhook server locally
uvicorn webhook.receiver:app --reload --port 8000

# Start the full desktop app (needs Rust toolchain + Node.js)
cd frontend && npm install
npm run tauri dev
```

---

## Security Rules — Absolute, Non-Negotiable

### Rule 1 — Every ForensicLog entry needs all 7 fields

When writing a new log entry (Python or Rust), it MUST contain:

```python
# Python side (logging_config.py LoggerAdapter)
logger.info("event_name", extra={
    "trace_id":    str(uuid.uuid4()),   # maps to input_hash concept
    "actor":       "user | webhook | system",
    "action":      "SEARCH | INSTALL | SCAN | WEBHOOK",
    "event":       "human-readable description",
})
```

```rust
// Rust side (lib.rs log_forensic_event)
// Always pass: actor, action, details
// Hashes (input_hash, result_hash, node_id) are computed inside the function
invoke('log_forensic_event', { actor: 'user', action: 'SEARCH', details: '...' })
```

### Rule 2 — Webhook MUST verify HMAC before processing

In `webhook/receiver.py`, `_verify_github_signature()` MUST be called on every request.
Do NOT add any route that skips this check.

```python
# ✅ Correct
body = await request.body()
_verify_github_signature(body, x_hub_signature_256)  # raises 403 if bad
payload = await request.json()

# ❌ Wrong — never skip verification
payload = await request.json()
# (proceeding without checking signature)
```

### Rule 3 — Local-first file analysis

Never send file content or binary data to an external URL.
`requests.post()` or `httpx.post()` to non-localhost is forbidden for file data.

### Rule 4 — Heavy work goes in background threads

Rust: use `tokio::spawn()` for anything that scans directories.
Python: use `asyncio` or `BackgroundTasks` for long-running operations.

---

## Python Coding Style

```python
# ✅ All functions need type hints
def validate(manifest: dict) -> bool: ...

# ✅ Google-style docstrings
def validate(manifest: dict) -> bool:
    """Return True when manifest is valid.

    Args:
        manifest: Parsed JSON dict from gstore-manifest.json.

    Returns:
        True if all required fields are present and correct.
    """

# ✅ Line length max 100 characters (black enforces this)

# ✅ Use | for union types (Python 3.10+)
def fn(x: str | None) -> str | None: ...
```

---

## Rust Coding Style

```rust
// ✅ Every public function needs a doc comment
/// Search for files whose names contain `query` under `path`.
#[tauri::command]
async fn search_files(query: String, path: String) -> Result<Vec<FileResult>, String> {
    // ...
}

// ✅ Use thiserror for custom errors
#[derive(Debug, thiserror::Error)]
enum GstoreError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

// ✅ Use anyhow for propagating errors in non-command functions
fn internal_helper() -> anyhow::Result<()> { ... }

// ✅ Tauri commands return Result<T, String> (String = error message to JS)
```

---

## React / JSX Style

```jsx
// ✅ Glassmorphism aesthetic — always dark bg + blur
<div className="bg-[#1c1c1c]/40 backdrop-blur-md border border-white/5 rounded-2xl">

// ✅ Use framer-motion for animations
<motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>

// ✅ Icons from lucide-react only
import { Search, ShieldCheck, Terminal } from 'lucide-react';

// ✅ Calling Rust from JS
import { invoke } from '@tauri-apps/api/core';
const results = await invoke('search_files', { query, path });

// ✅ Always log after a user action
await invoke('log_forensic_event', { actor: 'user', action: 'SEARCH', details: `searched: ${query}` });
```

---

## How Claude Should Approach Tasks in This Repo

1. **Read first** — check the relevant file before changing it
2. **Test first** — run `python -m pytest tests/ -v` before starting any change
3. **Smallest change** — fix only what the task asks; don't refactor unrelated code
4. **Test after** — every change must pass `python -m pytest tests/ -v`
5. **Security check** — after any change to webhook/receiver.py or lib.rs, confirm Rules 1–4 still hold
6. **No secrets** — never commit `GITHUB_WEBHOOK_SECRET` or any credential

---

## Architecture Mental Model (Simple Version)

```
User clicks button
  ↓
App.jsx (React)   — sends message via invoke()
  ↓
lib.rs (Rust)     — does the real work (fast file scan)
  ↓
audit.log         — EVERY action gets recorded here
```

GitHub pushes manifest update:
```
GitHub → POST /webhook
  ↓
receiver.py       — checks HMAC signature first
  ↓
(queue processing) — validate manifest, update catalog
```

---

*"Code like every action is being recorded — because it is."*
