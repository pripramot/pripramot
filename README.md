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

## 🌐 GitHub Pages (เว็บไซต์สาธิต)

หน้าสาธิตฝั่งหน้าบ้าน (React) ถูก deploy อัตโนมัติไปยัง **GitHub Pages** ทุกครั้งที่มีการ push ไปยัง branch `main`

- **URL:** [https://pripramot.github.io/pripramot/](https://pripramot.github.io/pripramot/)
- ระบบ CI/CD ใช้ GitHub Actions workflow `.github/workflows/pages.yml`
- ขั้นตอน: build Vite/React → upload artifact → deploy ไปยัง Pages โดยอัตโนมัติ
- ตัวแปร `base: '/pripramot/'` ถูกตั้งใน `frontend/vite.config.js` เพื่อให้ assets และ routing ทำงานถูกต้องบน GitHub Pages สำหรับ project page URL

---

*พัฒนาโดย Jarntam & Nangnoy*
