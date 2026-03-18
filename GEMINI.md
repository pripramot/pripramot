# GSTORE: มาตรฐานวิศวกรรมและนิติวิทยาศาสตร์ (Engineering & Forensic Standards)

## 🎯 วิสัยทัศน์

ระบบค้นหาไฟล์ประสิทธิภาพสูงและ App Store ยุคใหม่สำหรับงานนิติวิทยาศาสตร์และ Power User พัฒนาด้วย Tauri v2 (Rust + React)

## 🛡️ ความปลอดภัยและความน่าเชื่อถือ (บังคับ)

1. **Forensic Logging:** เหตุการณ์สำคัญทั้งหมด (ดาวน์โหลด / ติดตั้ง / สแกน / อัปเดต Manifest) ต้องถูกบันทึกเป็น JSON แบบมีโครงสร้างใน `.gstore/logs/`
2. **Immutable Trace:** ทุก log ต้องมีฟิลด์ครบ ได้แก่ `timestamp`, `actor`, `action`, `input_hash`, `result_hash` และ `node_id`
3. **Local-First Analysis:** การดึงเมทาดาทาของไฟล์ (แงะ) ต้องประมวลผลบนเครื่องเท่านั้น ห้ามส่งข้อมูลไบนารีออกไปยัง API ภายนอก
4. **Signature Verification:** การอัปเดต Manifest ผ่าน GitHub Webhook ทุกครั้งต้องตรวจสอบลายเซ็น HMAC
5. **Sandboxed Worker:** งานวิเคราะห์ไฟล์ที่หนักต้องรันใน background thread แยกต่างหาก (Tokio) หรือ process แยก

## 💻 แนวทางการเขียนโค้ด

- **Rust:** ใช้ `tokio` สำหรับงาน async ใช้ `thiserror` และ `anyhow` สำหรับจัดการ error
- **Frontend:** React + TypeScript + Tailwind CSS ตามแนวทาง "Modern Glassmorphism"
- **State Management:** ใช้ `Zustand` ฝั่ง frontend และ Tauri State ฝั่ง backend
- **Testing:** ตั้งเป้า test coverage สูง โดยเฉพาะ `manifest validator` และแกนหลัก `file extractor`

## 📁 โครงสร้างไดเรกทอรี

- `src-tauri/`: โค้ด Rust, คำสั่ง Tauri และโมดูลนิติวิทยาศาสตร์
- `src/`: สคริปต์ Python (manifest validator, logging)
- `frontend/`: React UI/UX
- `.gstore/`: ฐานข้อมูลโลคอล, cache และ log ที่ตรวจสอบย้อนหลังได้

---

*สร้างโดย: Nangnoy (Gemini CLI) สำหรับ Jarntam (Forensic Master)*
