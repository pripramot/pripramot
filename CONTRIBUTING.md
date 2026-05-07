# Contributing Guidelines / แนวทางการมีส่วนร่วม

> ภาษาไทย · [English below](#english)

---

## 🇹🇭 ภาษาไทย

ขอบคุณที่สนใจมีส่วนร่วมในโปรเจกต์นี้!
โปรเจกต์นี้เป็น **Monorepo** ที่ประกอบด้วย Frontend (JavaScript), Backend (Python), Desktop App (Tauri/Rust) และ Webhook Service

### โครงสร้างโปรเจกต์

```
pripramot/
├── frontend/      # UI (JavaScript / Vite)
├── src/           # Python backend หลัก
├── src-tauri/     # Tauri desktop app (Rust)
├── tests/         # Test suites (Python)
├── webhook/       # Webhook service
├── docs/          # เอกสารประกอบ
└── scripts/       # Build / deploy scripts
```

### ข้อกำหนดก่อน Pull Request

- [ ] อ่านและทำความเข้าใจโครงสร้างโปรเจกต์ก่อน
- [ ] ตรวจสอบว่า Issue หรือ PR ที่คล้ายกันยังไม่มีอยู่แล้ว
- [ ] Fork repo และสร้าง branch ใหม่จาก `main` เสมอ
- [ ] ตั้งชื่อ branch ให้สื่อความหมาย เช่น `feat/add-login`, `fix/webhook-timeout`
- [ ] สร้าง PR **แยกต่างหากสำหรับแต่ละฟีเจอร์หรือแก้บัค**
- [ ] เขียน commit message ให้ชัดเจน ตาม [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` เพิ่มฟีเจอร์ใหม่
  - `fix:` แก้บัค
  - `docs:` เปลี่ยนแปลงเอกสาร
  - `chore:` งาน maintenance
  - `test:` เพิ่ม/แก้ tests
- [ ] ใส่คำอธิบายใน PR ว่าแก้ไขอะไร และทำไม
- [ ] ตรวจสอบให้แน่ใจว่า tests ผ่านก่อนส่ง PR

### การตั้งค่า Development Environment

```bash
# 1. Clone repo
git clone https://github.com/pripramot/pripramot.git
cd pripramot

# 2. Python backend
pip install -r requirements.txt
pre-commit install

# 3. Frontend
cd frontend
npm install

# 4. Tauri (ต้องการ Rust)
cd ../src-tauri
cargo build
```

### การรัน Tests

```bash
# Python tests
pytest tests/

# Frontend tests
cd frontend && npm test
```

### Code Style

- **Python**: ใช้ `flake8` และ `black` (ตั้งค่าใน `.flake8` และ `pyproject.toml`)
- **JavaScript**: ใช้ ESLint / Prettier (ถ้ามีใน frontend)
- **Rust**: ใช้ `cargo fmt` และ `cargo clippy`
- pre-commit hooks จะรันอัตโนมัติเมื่อ commit

### สิ่งที่รับ

- ✅ Bug fixes
- ✅ Feature ใหม่ที่สอดคล้องกับเป้าหมายโปรเจกต์
- ✅ ปรับปรุงเอกสาร
- ✅ เพิ่ม tests
- ✅ ปรับปรุง CI/CD

### สิ่งที่ไม่รับ

- ❌ Code ที่ไม่มี tests (สำหรับฟีเจอร์หลัก)
- ❌ Dependencies ใหม่โดยไม่มีเหตุผล
- ❌ Breaking changes โดยไม่มีการหารือใน Issue ก่อน

---

## English

Thank you for your interest in contributing!
This is a **Monorepo** containing Frontend (JavaScript), Backend (Python), Desktop App (Tauri/Rust), and a Webhook Service.

### Before Submitting a Pull Request

- Search existing issues and PRs to avoid duplicates.
- Fork the repository and create your branch from `main`.
- Use descriptive branch names: `feat/add-login`, `fix/webhook-timeout`.
- Make individual pull requests for each feature or bug fix.
- Write clear commit messages following [Conventional Commits](https://www.conventionalcommits.org/).
- Describe what and why in your PR description.
- Ensure all tests pass before submitting.

### Code Style

- **Python**: `flake8`, `black` (configured in `.flake8` / `pyproject.toml`)
- **JavaScript**: ESLint / Prettier
- **Rust**: `cargo fmt`, `cargo clippy`
- Pre-commit hooks run automatically on commit.

### What We Accept

- ✅ Bug fixes
- ✅ New features aligned with the project goals
- ✅ Documentation improvements
- ✅ Additional tests
- ✅ CI/CD improvements

---

ขอบคุณสำหรับการมีส่วนร่วม! / Thank you for contributing! 🙏
