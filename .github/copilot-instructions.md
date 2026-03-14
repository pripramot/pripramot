# GitHub Copilot Workspace Instructions — GSTORE

## Project Overview
GSTORE is a Tauri v2 desktop app (Rust backend + React frontend) with a Python FastAPI webhook service.
It is a forensic-grade file search engine and app store.

---

## Tech Stack Quick Reference

| File / Directory | Language | Purpose |
|-----------------|----------|---------|
| `frontend/src/App.jsx` | React 18 / JSX | UI — Glassmorphism dark theme |
| `src-tauri/src/lib.rs` | Rust | `search_files`, `log_forensic_event` Tauri commands |
| `webhook/receiver.py` | Python 3.11+ | GitHub webhook receiver (HMAC-SHA256 verified) |
| `src/gstore/manifest_validator.py` | Python | Validates `gstore-manifest.json` |
| `src/gstore/logging_config.py` | Python | JSON structured logger |
| `tests/` | Python pytest | All tests |

---

## Coding Patterns to Follow

### Python — always use type hints and Google docstrings
```python
def validate(manifest: dict) -> bool:
    """Return True when manifest passes all GSTORE validation rules.

    Args:
        manifest: Parsed dict from gstore-manifest.json.

    Returns:
        True if valid, False otherwise.
    """
    ...
```

### Python — webhook always verifies HMAC before reading payload
```python
body = await request.body()
_verify_github_signature(body, x_hub_signature_256)  # 403 if bad
payload = await request.json()
```

### Rust — Tauri commands return `Result<T, String>`
```rust
#[tauri::command]
async fn my_command(input: String) -> Result<MyStruct, String> {
    do_work(&input).map_err(|e| e.to_string())
}
```

### Rust — log every critical action via `log_forensic_event`
```rust
// After any SEARCH, INSTALL, SCAN, or manifest update:
invoke('log_forensic_event', { actor: 'user', action: 'INSTALL', details: format!("installed {}", app_id) })
```

### React — call Rust using invoke, always log after
```jsx
import { invoke } from '@tauri-apps/api/core';

const results = await invoke('search_files', { query, path });
await invoke('log_forensic_event', { actor: 'user', action: 'SEARCH', details: `query: ${query}` });
```

### React — Glassmorphism UI pattern
```jsx
// Cards
<div className="bg-[#1c1c1c]/40 backdrop-blur-md border border-white/5 rounded-2xl p-5">

// Animated sections
<motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>

// Sidebar items (active state)
<button className="bg-white/10 text-white font-medium rounded-md">
```

---

## Forensic Log — Required Shape

Every audit log entry written to `.gstore/logs/audit.log` MUST have these 7 fields:

```json
{
  "timestamp":   "ISO-8601 string",
  "actor":       "user | webhook | system",
  "action":      "SEARCH | INSTALL | SCAN | MANIFEST_UPDATE",
  "input_hash":  "sha256 hex string",
  "result_hash": "sha256 hex string",
  "node_id":     "sha256 hex string",
  "details":     "plain text description"
}
```

---

## Python Code Style

- **Formatter**: `black` — max line length **100**
- **Linter**: `flake8`
- **Type hints**: required on every function signature
- **Union types**: use `str | None` (not `Optional[str]`)
- **Imports**: stdlib → third-party → local (blank line between groups)

---

## Rust Code Style

- Error types: `thiserror` for definitions, `anyhow` for propagation
- Async runtime: `tokio` only — no `std::thread::spawn` for I/O
- Every `#[tauri::command]` function needs a `///` doc comment

---

## Testing

Run: `python -m pytest tests/ -v`

- New manifest validation rules → add test in `tests/test_manifest_validator.py`
- New webhook behaviour → add test in `tests/test_webhook_receiver.py`
- Use `monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "secret")` for webhook tests

---

## Absolute Don'ts

- ❌ Do NOT send file content to any external URL
- ❌ Do NOT skip `_verify_github_signature()` in webhook routes
- ❌ Do NOT create a `ForensicLog` / log entry without all 7 required fields
- ❌ Do NOT commit secrets or API keys
- ❌ Do NOT use `any` type in TypeScript (when migrating to TSX)
