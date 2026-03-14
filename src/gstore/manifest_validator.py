"""Manifest validation for GSTORE.

A valid manifest must:
- Have ``project`` set to ``"GSTORE"``.
- Include a ``forensic_logging`` section with every required field.
- Include a ``testing`` section.
"""

from __future__ import annotations

# Required keys inside the ``forensic_logging`` section (from manifest.json spec).
_REQUIRED_LOG_FIELDS: set[str] = {
    "format",
    "required_fields",
    "retention_days",
    "storage",
    "sensitive_data_policy",
}


def validate(manifest: dict) -> bool:
    """Return ``True`` when *manifest* is a valid GSTORE manifest.

    Validation rules
    ----------------
    1. ``manifest["project"]`` must equal ``"GSTORE"``.
    2. ``manifest["forensic_logging"]`` must be present and contain all
       keys listed in :data:`_REQUIRED_LOG_FIELDS`.
    3. ``manifest["testing"]`` must be present.
    """
    if manifest.get("project") != "GSTORE":
        return False

    log_cfg = manifest.get("forensic_logging")
    if not isinstance(log_cfg, dict):
        return False
    if not _REQUIRED_LOG_FIELDS.issubset(log_cfg.keys()):
        return False

    if "testing" not in manifest:
        return False

    return True
