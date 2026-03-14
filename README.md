# GSTORE 🛡️🦀

**GSTORE** (GTS Alpha Store & Forensics) คือโปรแกรมค้นหาไฟล์ประสิทธิภาพสูงและระบบจัดการแอปพลิเคชันยุคใหม่
สร้างขึ้นด้วยเทคโนโลยี **Tauri v2 (Rust + React)** เพื่อความเร็ว แรง และเบาที่สุด

## ✨ Key Features
- **High-speed Search Engine:** สแกนและค้นหาไฟล์ด้วยความเร็วระดับ Rust
- **Auto-Sync Manifest:** ระบบ Store ที่อัปเดตรายการแอปผ่าน GitHub อัตโนมัติ
- **Forensic Extraction:** วิเคราะห์ Metadata และ Signatures ของไฟล์โดยตรง (แงะ!)
- **AI-Powered Discovery:** ค้นหาเครื่องมือใหม่ๆ ด้วยพลังของ Exa AI

---

## 🏛️ สถาปัตยกรรมโครงการ (Project Architecture)

```
pripramot/
├── frontend/               # React 18 + Vite + Tailwind CSS (Glassmorphism UI)
│   └── src/
│       ├── App.jsx         # Main app: Sidebar, Store, Search, Logs, Settings tabs
│       ├── main.jsx        # React entry point
│       └── index.css       # Tailwind base styles
│
├── src-tauri/              # Tauri v2 Rust backend
│   ├── Cargo.toml          # Rust dependencies (tokio, serde, walkdir, sha2, …)
│   └── src/
│       ├── main.rs         # Binary entry point → calls gstore::run()
│       └── lib.rs          # Tauri commands: search_files, log_forensic_event
│
├── src/gstore/             # Python utility modules
│   ├── __init__.py
│   ├── manifest_validator.py   # Validates gstore-manifest.json structure
│   └── logging_config.py       # Structured JSON logger (python-json-logger)
│
├── webhook/
│   └── receiver.py         # FastAPI webhook receiver with HMAC-SHA256 verification
│
├── tests/
│   ├── test_manifest_validator.py  # pytest: manifest validation rules
│   └── test_webhook_receiver.py    # pytest: webhook HMAC + response tests
│
├── gstore-manifest.json    # App catalog (id, name, version, checksum, …)
├── manifest.json           # Project-level config (coding style, logging policy)
├── requirements.txt        # Python dependencies
└── GEMINI.md               # Engineering & Forensic Standards (source of truth)
```

### ชั้นสถาปัตยกรรม (Layers)

| ชั้น | เทคโนโลยี | หน้าที่ |
|------|-----------|---------|
| **UI Layer** | React 18, Tailwind CSS, Framer Motion | แสดงผล Store, Search, Audit Logs |
| **IPC Bridge** | Tauri v2 `invoke()` | ส่งคำสั่งจาก JS → Rust |
| **Core Engine** | Rust (tokio, walkdir, sha2) | ค้นหาไฟล์, บันทึก Forensic Log |
| **Webhook Service** | Python FastAPI | รับ GitHub Webhook พร้อม HMAC verification |
| **Validation** | Python (manifest_validator) | ตรวจสอบโครงสร้าง manifest |
| **Logging** | JSON (audit.log) | Immutable trace ทุก action |

---

## 🔒 Forensic Log Format

ทุก event ที่บันทึกใน `.gstore/logs/audit.log` มีโครงสร้างตาม GEMINI.md:

```json
{
  "timestamp": "2026-03-14T12:00:00+07:00",
  "actor":      "user",
  "action":     "SEARCH",
  "input_hash": "<sha256 of action:details>",
  "result_hash":"<sha256 of input_hash:actor:node_id>",
  "node_id":    "<sha256 of hostname>",
  "details":    "User searched: malware.exe"
}
```

---

## 🚀 Getting Started

```bash
# 1. Python backend (webhook + validator)
pip install -r requirements.txt
uvicorn webhook.receiver:app --reload

# 2. Frontend + Tauri desktop app
cd frontend && npm install
npm run tauri dev        # ต้องมี Rust & Tauri CLI
```

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## 🛡️ Security Requirements (GEMINI.md)

1. **Forensic Logging** – ทุก critical action ต้องบันทึกเป็น JSON ที่ `.gstore/logs/`
2. **Immutable Trace** – ทุก log entry ต้องมี `timestamp`, `actor`, `action`, `input_hash`, `result_hash`, `node_id`
3. **Local-First Analysis** – ห้ามส่ง binary data ไปยัง 3rd-party APIs
4. **HMAC Signature Verification** – webhook ทุก request ต้องตรวจ `X-Hub-Signature-256`
5. **Sandboxed Worker** – งานหนักต้องรันใน Tokio thread หรือ subprocess แยก

---

## 🗺️ แนวทางการพัฒนาต่อ (Development Roadmap)

### 🔧 งานที่ยังขาด (Open TODOs)
- [ ] **Manifest auto-sync**: webhook receiver ยังไม่ enqueue manifest update หลังตรวจสอบ HMAC
- [ ] **Forensic file extractor**: ยังไม่มี Rust module สำหรับแยก PE/ELF metadata (`goblin`, `pe-parse` มีใน Cargo.toml แล้ว)
- [ ] **Audit Logs UI tab**: frontend มี tab "Audit Logs" แต่ยังไม่แสดงข้อมูลจริง
- [ ] **Settings UI tab**: ยังเป็น placeholder
- [ ] **Installed Apps tab**: ข้อมูล hardcoded ยังไม่ดึงจาก manifest จริง
- [ ] **Node ID**: ควรใช้ UUID เครื่องที่ stable แทน sha256(hostname)
- [ ] **Search path**: hardcoded `C:\Users\usEr` ใน App.jsx ควรให้ user เลือก path เอง

### 📈 การปรับปรุงที่แนะนำ
- เพิ่ม Zustand store สำหรับ global state (ยังใช้แค่ useState)
- ย้าย frontend จาก JSX → TSX เพื่อ type safety
- เพิ่ม test สำหรับ Rust commands (`cargo test`)
- เพิ่ม CI step สำหรับ `cargo build --release`

---
*Developed by Jarntam & Nangnoy* 🙄🚀ⅨⅫ⫺⫺

