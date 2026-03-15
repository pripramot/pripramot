import json
import pathlib

from src.gstore.manifest_validator import validate

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_ENTRY = {
    "id": "gstore-scanner",
    "name": "GSTORE Native Scanner",
    "description": "The high-speed file discovery engine.",
    "version": "0.1.0",
    "category": "Forensics",
    "icon_url": "https://example.com/icon.png",
    "download_url": "https://example.com/scanner.exe",
    "checksum": "sha256:abc123",
    "is_verified": True,
}


def _valid_manifest(**overrides) -> dict:
    """สร้าง manifest ที่ valid พร้อม override fields ได้"""
    base = {
        "version": "1.0.0",
        "last_updated": "2026-03-10T23:05:00Z",
        "catalog": [dict(_VALID_ENTRY)],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------


def test_manifest_valid_sample():
    assert validate(_valid_manifest()) is True


def test_manifest_multiple_catalog_entries():
    second = dict(_VALID_ENTRY, id="ahq-store", name="AHQ Store")
    assert validate(_valid_manifest(catalog=[dict(_VALID_ENTRY), second])) is True


def test_manifest_real_file():
    """gstore-manifest.json ที่อยู่ใน repo ต้องผ่าน validation"""
    repo_root = pathlib.Path(__file__).parent.parent
    manifest_path = repo_root / "gstore-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert validate(manifest) is True


# ---------------------------------------------------------------------------
# Missing required top-level field tests
# ---------------------------------------------------------------------------


def test_manifest_missing_version():
    m = _valid_manifest()
    del m["version"]
    assert validate(m) is False


def test_manifest_missing_last_updated():
    m = _valid_manifest()
    del m["last_updated"]
    assert validate(m) is False


def test_manifest_missing_catalog():
    m = _valid_manifest()
    del m["catalog"]
    assert validate(m) is False


# ---------------------------------------------------------------------------
# Catalog structure tests
# ---------------------------------------------------------------------------


def test_manifest_empty_catalog():
    assert validate(_valid_manifest(catalog=[])) is False


def test_manifest_catalog_not_a_list():
    assert validate(_valid_manifest(catalog="not-a-list")) is False


def test_manifest_entry_missing_required_field():
    entry = dict(_VALID_ENTRY)
    del entry["checksum"]
    assert validate(_valid_manifest(catalog=[entry])) is False


def test_manifest_entry_is_verified_not_bool():
    entry = dict(_VALID_ENTRY, is_verified="yes")
    assert validate(_valid_manifest(catalog=[entry])) is False


def test_manifest_checksum_wrong_prefix():
    entry = dict(_VALID_ENTRY, checksum="md5:abc123")
    assert validate(_valid_manifest(catalog=[entry])) is False


def test_manifest_checksum_empty_string():
    entry = dict(_VALID_ENTRY, checksum="")
    assert validate(_valid_manifest(catalog=[entry])) is False
