# GEMINI.md — GSTORE Agent Instructions

> **อ่านทุกครั้งก่อนแตะโค้ด** — นี่คือคู่มือ AI ประจำโปรเจกต์ GSTORE
> *(Read before every code change — this is the AI agent's rulebook for GSTORE)*

---

## 1. โปรเจกต์นี้คืออะไร? (What is this project?)

**GSTORE** = เครื่องมือค้นหาไฟล์ความเร็วสูง + App Store สำหรับงาน Forensics
- ภาษาที่ใช้: **Rust** (engine), **React/JSX** (UI), **Python** (webhook + validator)
- Framework: **Tauri v2** — ทำให้ Rust คุยกับ React ได้ผ่าน `invoke()`
- คิดแบบง่ายๆ: เหมือน Windows Store แต่ค้นหาไฟล์ได้เร็วมาก และบันทึก log ทุกการกระทำ

---

## 2. คำสั่งที่ใช้บ่อย (Essential Commands)

```bash
# ✅ รัน Python tests (ทำก่อน/หลังแก้โค้ด Python เสมอ)
python -m pytest tests/ -v

# ✅ ติดตั้ง Python dependencies
pip install -r requirements.txt

# ✅ เริ่ม Webhook server (Python FastAPI)
uvicorn webhook.receiver:app --reload

# ✅ เริ่ม Desktop app (ต้องมี Rust + Node.js)
cd frontend && npm install
npm run tauri dev

# ✅ Format Python code
black src/ webhook/ tests/

# ✅ Lint Python code
flake8 src/ webhook/ tests/
```

---

## 3. สถาปัตยกรรม (Architecture — Where Things Live)

```
GSTORE/
├── frontend/src/App.jsx        ← React UI (Glassmorphism style)
│                                 ใช้ invoke('search_files', ...) เรียก Rust
│
├── src-tauri/src/lib.rs        ← Rust commands ที่ frontend เรียกได้:
│                                 • search_files(query, path) → Vec<FileResult>
│                                 • log_forensic_event(actor, action, details)
│
├── webhook/receiver.py         ← FastAPI รับ GitHub Webhook
│                                 ตรวจ HMAC-SHA256 ทุก request
│
├── src/gstore/
│   ├── manifest_validator.py   ← ตรวจสอบ gstore-manifest.json
│   └── logging_config.py       ← JSON structured logger
│
└── tests/
    ├── test_manifest_validator.py
    └── test_webhook_receiver.py
```

**Data flow ง่ายๆ:**
```
User คลิก Search
    → App.jsx invoke('search_files')
        → Rust lib.rs ค้นหาไฟล์
            → ส่งผลกลับ JS
                → invoke('log_forensic_event') บันทึก audit log
```

---

## 4. กฎเหล็ก — ห้ามละเมิด (Hard Rules — Never Break)

### 🔒 กฎที่ 1: Forensic Log ต้องมีครบ 7 ฟิลด์เสมอ
ทุก log entry ใน `.gstore/logs/audit.log` **ต้องมี**:
```json
{
  "timestamp":   "2026-03-14T12:00:00+07:00",
  "actor":       "user",
  "action":      "SEARCH",
  "input_hash":  "sha256(action:details)",
  "result_hash": "sha256(input_hash:actor:node_id)",
  "node_id":     "sha256(hostname)",
  "details":     "User searched: malware.exe"
}
```
❌ ห้ามเพิ่ม log entry ที่ขาดฟิลด์ใดฟิลด์หนึ่ง

### 🔒 กฎที่ 2: Webhook ต้องตรวจ HMAC เสมอ
ใน `webhook/receiver.py` ทุก POST `/webhook` ต้องผ่าน `_verify_github_signature()` ก่อน
❌ ห้าม bypass หรือ comment out การตรวจ signature

### 🔒 กฎที่ 3: Local-First Analysis
การวิเคราะห์ไฟล์ต้องทำในเครื่อง **เท่านั้น**
❌ ห้ามส่ง binary data หรือ file content ไปยัง external API ใดๆ

### 🔒 กฎที่ 4: งานหนักต้องรันใน background thread
ใน Rust ใช้ `tokio::spawn()` สำหรับ file scanning ที่ใช้เวลานาน
❌ ห้าม block the main thread

---

## 5. Coding Style

### Python
| กฎ | ค่า |
|----|-----|
| Line length | 100 ตัวอักษร |
| Formatter | `black` |
| Linter | `flake8` |
| Docstrings | Google style |
| Type hints | **บังคับ** (`-> bool`, `dict`, `str \| None`) |

### Rust
- ใช้ `tokio` สำหรับ async (ไม่ใช้ `std::thread::spawn`)
- Error handling: `thiserror` สำหรับ define errors, `anyhow` สำหรับ propagate
- ทุก public function ต้องมี doc comment (`///`)

### React/JSX
- Style: **Glassmorphism** — dark background, `backdrop-blur`, `border-white/5`
- State: `useState` สำหรับ local state, `zustand` สำหรับ global state
- ห้ามใช้ `any` ใน TypeScript (เมื่อย้ายไป TSX)

---

## 6. การเพิ่ม Feature ใหม่ (How to Add a New Feature)

### เพิ่ม Tauri command ใหม่ (Rust → JS)
1. เขียน function ใน `src-tauri/src/lib.rs` พร้อม `#[tauri::command]`
2. เพิ่มชื่อ command ใน `tauri::generate_handler![..., your_new_command]`
3. เรียกจาก JS ด้วย `invoke('your_new_command', { arg: value })`
4. **อย่าลืม**: ถ้า command ทำ critical action ต้อง call `log_forensic_event` ด้วย

### เพิ่ม Python endpoint ใหม่
1. เพิ่ม route ใน `webhook/receiver.py`
2. ถ้ารับ payload จากภายนอก ต้องตรวจสอบ input ก่อนเสมอ
3. เขียน test ใน `tests/` ทันที

### เพิ่ม manifest field ใหม่
1. อัปเดต `gstore-manifest.json`
2. อัปเดต validation ใน `src/gstore/manifest_validator.py`
3. เพิ่ม test case ใน `tests/test_manifest_validator.py`

---

## 7. งานที่ยังค้างอยู่ (Open TODOs — Pick these up next)

| Priority | งาน | ไฟล์ที่เกี่ยวข้อง |
|----------|-----|-------------------|
| 🔴 High | Webhook enqueue manifest update หลัง HMAC pass | `webhook/receiver.py` |
| 🔴 High | Forensic file extractor (PE/ELF metadata ด้วย `goblin`) | `src-tauri/src/lib.rs` |
| 🟡 Medium | Audit Logs UI tab แสดงข้อมูลจริงจาก audit.log | `frontend/src/App.jsx` |
| 🟡 Medium | Search path ให้ user เลือกเองแทน hardcode | `frontend/src/App.jsx` |
| 🟢 Low | ย้าย frontend จาก JSX → TSX | `frontend/src/` |
| 🟢 Low | Stable node_id ด้วย persistent UUID | `src-tauri/src/lib.rs` |

---

## 8. ก่อน Commit ทุกครั้ง (Pre-Commit Checklist)

```bash
# 1. รัน tests
python -m pytest tests/ -v

# 2. Format + lint
black src/ webhook/ tests/
flake8 src/ webhook/ tests/

# 3. ตรวจว่า log entry ใหม่มีครบ 7 ฟิลด์
# 4. ตรวจว่าไม่มี API call ออกนอก (ไม่มี requests.post ไป external URL)
```

---

*Created for: Jarntam (Forensic Master) — Maintained by: GSTORE Team*
*"เขียนโค้ดให้เหมือนกล้องวงจรปิด — จับทุกอย่าง, ไม่พลาดแม้แต่น้อย"*
