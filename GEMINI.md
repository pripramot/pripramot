# GSTORE: Engineering & Forensic Standards

## 🎯 Vision
A high-performance file search engine and modern app store for forensics and power users. Built with Tauri v2 (Rust + React).

## 🛡️ Security & Integrity (Mandatory)
1. **Forensic Logging:** All critical actions (Downloads, Installs, Scans, Manifest Updates) MUST be logged in `.gstore/logs/` in structured JSON format.
2. **Immutable Trace:** Every log entry must include: `timestamp`, `actor`, `action`, `input_hash`, `result_hash`, and `node_id`.
3. **Local-First Analysis:** File metadata extraction (แงะ) must happen LOCALLY. No binary data should be sent to 3rd party APIs.
4. **Signature Verification:** All manifest updates via GitHub Webhook MUST verify the HMAC signature.
5. **Sandboxed Worker:** Heavy file analysis tasks MUST run in isolated background threads (Tokio) or separate processes.

## 💻 Coding Style
- **Rust Backend:** Use `tokio` for async tasks. Prefer `thiserror` and `anyhow` for robust error handling.
- **Frontend:** React + TypeScript + Tailwind CSS. Follow the "Modern Glassmorphism" aesthetic.
- **State Management:** Use `Zustand` on the frontend and `Tauri State` on the backend.
- **Testing:** 100% test coverage for `manifest validator` and `file extractor core`.

## 📁 Directory Structure
- `src-tauri/`: Rust logic, commands, and forensic modules.
- `src/`: React frontend (UI/UX).
- `.gstore/`: Local database, cache, and immutable logs.

---
*Created by: Nangnoy (Gemini CLI) for Jarntam (Forensic Master)*
