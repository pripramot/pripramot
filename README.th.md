# GSTORE 🛡️🦀

**GSTORE** (GTS Alpha Store & Forensics) คือโปรแกรมค้นหาไฟล์ประสิทธิภาพสูงและระบบจัดการแอปพลิเคชันยุคใหม่ พัฒนาด้วย **Tauri v2 (Rust + React)** เพื่อความเร็ว ความแม่นยำ และความปลอดภัยระดับนิติวิทยาศาสตร์

---

## ✨ คุณสมบัติเด่น

- **ระบบค้นหาไฟล์ความเร็วสูง:** สแกนและค้นหาไฟล์ด้วยความเร็วระดับ Rust
- **ซิงก์รายการแอปอัตโนมัติ (Manifest):** อัปเดตรายการเครื่องมือผ่าน GitHub โดยอัตโนมัติ
- **การวิเคราะห์เชิงนิติวิทยาศาสตร์ (Forensic Extraction):** วิเคราะห์ข้อมูลเมทาดาทาและลายเซ็นของไฟล์บนเครื่องโดยตรง
- **ค้นพบเครื่องมือใหม่ด้วย AI:** ค้นหาเครื่องมือและแอปด้วยพลังของ Exa AI

---

## 🚀 เริ่มต้นใช้งาน

1. ติดตั้ง dependencies ฝั่งหน้าบ้าน
   ```bash
   cd frontend && npm install
   ```
2. ดึง Rust dependencies (ต้องมี Rust toolchain)
   ```bash
   cd src-tauri && cargo fetch
   ```
3. รันโปรแกรมในโหมดพัฒนา
   ```bash
   npm run tauri dev
   ```

---

## 🛡️ Forensic Logging (บันทึกเหตุการณ์นิติวิทยาศาสตร์)

เหตุการณ์สำคัญทั้งหมด (ดาวน์โหลด / ติดตั้ง / สแกน / อัปเดต Manifest) จะถูกบันทึกโดยอัตโนมัติเป็นไฟล์ JSON แบบมีโครงสร้างใน `.gstore/logs/audit.log` ทุก log ต้องมีฟิลด์ครบ 7 รายการ ได้แก่ `timestamp`, `actor`, `action`, `input_hash`, `result_hash`, `node_id` และ `details`

ดูรายละเอียดมาตรฐานการพัฒนาเพิ่มเติมได้ใน [`GEMINI.md`](GEMINI.md)

---

## 🧪 การทดสอบ

```bash
python -m pytest tests/ -v
```

---

## 🌐 GTSAlpha-Forensics (Scan)

ในฐานะวิศวกรซอฟต์แวร์ประจำโครงการ GTSAlpha-Forensics ผมได้ทำการตรวจสอบ (Scan) ข้อมูลย้อนหลังทั้งหมด รวมถึงโครงสร้างของ Project Unicorn, C.H.R.O.N.O.S. และความก้าวหน้าของ Phuphadang Alpha AI ตลอดระยะเวลาที่ผ่านมา ข้อมูลทั้งหมดชี้ไปที่จุดประสงค์เดียวคือ: "การสร้างระบบนิติวิทยาศาสตร์ดิจิทัลอัจฉริยะที่ทำงานแบบ Local-first และมีมาตรฐานความแม่นยำระดับการบังคับใช้กฎหมาย"
เพื่อให้ระบบ Phuphadang Alpha AI ทำงานได้แม่นยำที่สุดตามหลักนิติวิทยาศาสตร์ นี่คือ System Prompt (Instruction) ที่ผมออกแบบมาเพื่อใช้กับ AI Agent (Claude/Gemini) ในโปรเจกต์นี้โดยเฉพาะครับ
________________
1. System Architect Prompt: Phuphadang Alpha AI (Forensics Edition)
คุณสามารถนำข้อความนี้ไปวางในหน้าต่าง Project Instructions ของ Claude หรือ System Instructions ใน Gemini เพื่อกำกับทิศทางของ AI ให้แม่นยำครับ:


Markdown




# Role: Senior Digital Forensic AI Specialist & System Architect
# System: Phuphadang Alpha AI (Core: GTSAlpha-Forensics)

## 1. Core Mission
คุณคือสมองกลของระบบนิติวิทยาศาสตร์ดิจิทัล (Digital Forensics) ทำหน้าที่วิเคราะห์ข้อมูลจาก Project CHRONOS (Tracking) และ Unicorn (Evidence Analysis) โดยยึดหลัก Integrity และ Chain of Custody อย่างเคร่งครัด

## 2. Technical Domain Knowledge
- Digital Evidence Handling (ISO/IEC 27037)
- Memory Forensics (Volatility Framework standards)
- Network Intelligence & Real-time Tracking (CCTV/IP/Location Data)
- MCP Architecture: ออกแบบและใช้งาน Model Context Protocol เพื่อเชื่อมต่อกับฐานข้อมูล Local และอุปกรณ์ On-premise

## 3. Operational Constraints (Strict)
- Local-first Architecture: ลอจิกการประมวลผลต้องเน้นการทำงานแบบ Offline หรือ On-premise เพื่อความปลอดภัยของข้อมูล
- Precision Over Creativity: ในงานนิติวิทยาศาสตร์ ห้ามมีการ Hallucination (หลอนข้อมูล) หากข้อมูลไม่ชัดเจน ให้รายงานตามข้อเท็จจริงของ Raw Data เท่านั้น
- Secure Web3/Blockchain: รองรับการตรวจสอบธุรกรรมและ Smart Contracts ผ่าน GtsAlpha Wallet logic

## 4. Response Standard
- Language: Thai (Professional) + Technical English terms
- Style: Code-First (ส่งมอบ Code, CLI Commands, หรือ Schema ที่ใช้งานได้จริงทันที)
- Format: ใช้ Markdown ที่ชัดเจน แยกส่วนสถาปัตยกรรม (Architecture) และส่วนปฏิบัติการ (Operation)

________________
2. แผนผังโครงสร้างการเชื่อมต่อข้อมูล (Data Lineage)
เพื่อให้คุณเห็นภาพรวมที่ผมสแกนมาทั้งหมด นี่คือความสัมพันธ์ของโมดูลในโครงการครับ:
________________
3. สรุปความแม่นยำ 3 จุดที่ต้องเน้น (Software Engineer Review)
จากการวิเคราะห์เนื้อหาตลอด 6 เดือน ผมพบว่าระบบจะแม่นยำที่สุดถ้าเราคุม 3 จุดนี้ครับ:
1. Data Ingestion (Root Trace): ต้องทำ Data Validation ตั้งแต่รับเข้า (Ingest API) เพื่อให้มั่นใจว่าข้อมูล Metadata (Timestamp, Source ID) ไม่ถูกแก้ไข
2. MCP Server Logic: ตัว Agent ไม่ควรเข้าถึง Database โดยตรง แต่ต้องผ่าน MCP Server ที่เขียนด้วย Go หรือ Node.js เพื่อทำ Role-based Access Control (RBAC)
3. Local RAG: การทำ Intelligence Analysis ต้องใช้ RAG (Retrieval-Augmented Generation) จากฐานข้อมูลกฎหมายและวิธีพิจารณาความอาญาของไทยเป็นฐานความรู้ (Knowledge Base)
________________
4. Next Step: การเตรียม Code ชุดแรก
ในฐานะวิศวกรโครงการ ผมพร้อมผลิต Boilerplate ของ Ingest API (Node.js/TypeScript) ที่มีโครงสร้างรองรับ Digital Signature เพื่อใช้ยืนยันความถูกต้องของพยานหลักฐาน (Digital Evidence)
ต้องการให้ผมเริ่มเขียนไฟล์ server.ts และ database_schema.sql สำหรับโมดูล Forensics นี้เลยไหมครับ?

---

*พัฒนาโดย Jarntam & Nangnoy*
