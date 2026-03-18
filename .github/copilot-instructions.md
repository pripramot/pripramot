# คำแนะนำ GitHub Copilot Workspace — GSTORE

## ภาพรวมโปรเจกต์

GSTORE คือแอปเดสก์ท็อป Tauri v2 (Rust backend + React frontend) พร้อม Python FastAPI webhook service เป็นระบบค้นหาไฟล์และ App Store ระดับนิติวิทยาศาสตร์

---

## อ้างอิงเทคโนโลยีหลัก

| ไฟล์ / ไดเรกทอรี | ภาษา | วัตถุประสงค์ |
|-----------------|----------|---------|
| `frontend/src/App.jsx` | React 18 / JSX | UI — ธีมมืดแบบ Glassmorphism |
| `src-tauri/src/lib.rs` | Rust | คำสั่ง Tauri: `search_files`, `log_forensic_event` |
| `webhook/receiver.py` | Python 3.11+ | รับ GitHub webhook (ตรวจสอบด้วย HMAC-SHA256) |
| `src/gstore/manifest_validator.py` | Python | ตรวจสอบ `gstore-manifest.json` |
| `src/gstore/logging_config.py` | Python | JSON structured logger |
| `tests/` | Python pytest | เทสต์ทั้งหมด |

---

## รูปแบบโค้ดที่ต้องปฏิบัติตาม

### Python — ต้องใช้ type hints และ Google docstrings เสมอ
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

### Python — webhook ต้องตรวจสอบ HMAC ก่อนอ่าน payload เสมอ
```python
body = await request.body()
_verify_github_signature(body, x_hub_signature_256)  # 403 if bad
payload = await request.json()
```

### Rust — คำสั่ง Tauri ต้อง return `Result<T, String>`
```rust
#[tauri::command]
async fn my_command(input: String) -> Result<MyStruct, String> {
    do_work(&input).map_err(|e| e.to_string())
}
```

### Rust — บันทึกทุก critical action ผ่าน `log_forensic_event`
```rust
// หลังจาก SEARCH, INSTALL, SCAN หรืออัปเดต manifest ทุกครั้ง:
invoke('log_forensic_event', { actor: 'user', action: 'INSTALL', details: format!("installed {}", app_id) })
```

### React — เรียก Rust ผ่าน invoke และบันทึก log หลังเสมอ
```jsx
import { invoke } from '@tauri-apps/api/core';

const results = await invoke('search_files', { query, path });
await invoke('log_forensic_event', { actor: 'user', action: 'SEARCH', details: `query: ${query}` });
```

### React — รูปแบบ UI Glassmorphism
```jsx
// Cards
<div className="bg-[#1c1c1c]/40 backdrop-blur-md border border-white/5 rounded-2xl p-5">

// ส่วนที่มี animation
<motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>

// Sidebar items (active state)
<button className="bg-white/10 text-white font-medium rounded-md">
```

---

## โครงสร้าง Forensic Log — ฟิลด์บังคับ

ทุก log entry ที่เขียนลง `.gstore/logs/audit.log` ต้องมีฟิลด์ครบ 7 รายการ:

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

## สไตล์โค้ด Python

- **Formatter**: `black` — ความยาวบรรทัดสูงสุด **100**
- **Linter**: `flake8`
- **Type hints**: บังคับทุก function signature
- **Union types**: ใช้ `str | None` (ไม่ใช่ `Optional[str]`)
- **Imports**: stdlib → third-party → local (คั่นด้วยบรรทัดว่าง)

---

## สไตล์โค้ด Rust

- ประเภท error: `thiserror` สำหรับนิยาม, `anyhow` สำหรับ propagation
- Async runtime: ใช้ `tokio` เท่านั้น — ห้ามใช้ `std::thread::spawn` สำหรับงาน I/O
- ทุก `#[tauri::command]` function ต้องมี `///` doc comment

---

## การทดสอบ

รัน: `python -m pytest tests/ -v`

- กฎ manifest validation ใหม่ → เพิ่มเทสต์ใน `tests/test_manifest_validator.py`
- พฤติกรรม webhook ใหม่ → เพิ่มเทสต์ใน `tests/test_webhook_receiver.py`
- ใช้ `monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "secret")` สำหรับเทสต์ webhook

---

## สิ่งที่ห้ามทำโดยเด็ดขาด

- ❌ ห้ามส่งเนื้อหาไฟล์ไปยัง URL ภายนอกใดๆ
- ❌ ห้ามข้าม `_verify_github_signature()` ใน webhook routes
- ❌ ห้ามสร้าง `ForensicLog` / log entry โดยขาดฟิลด์ใดฟิลด์หนึ่งจาก 7 ฟิลด์บังคับ
- ❌ ห้าม commit secrets หรือ API keys
- ❌ ห้ามใช้ type `any` ใน TypeScript (เมื่อ migrate ไปใช้ TSX)
