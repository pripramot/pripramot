"""Validation logic for gstore-manifest.json files."""

_REQUIRED_TOP_LEVEL: frozenset[str] = frozenset({"version", "last_updated", "catalog"})
_REQUIRED_ENTRY_FIELDS: frozenset[str] = frozenset(
    {
        "id",
        "name",
        "description",
        "version",
        "category",
        "icon_url",
        "download_url",
        "checksum",
        "is_verified",
    }
)


def validate(manifest: dict) -> bool:
    """Return True when *manifest* passes all GSTORE validation rules.

    Validation rules:
    - Top-level keys ``version``, ``last_updated``, and ``catalog`` must be present.
    - ``catalog`` must be a non-empty list.
    - Every entry in ``catalog`` must contain all required fields.
    - ``is_verified`` must be a boolean.
    - ``checksum`` must start with ``sha256:``.

    Args:
        manifest: Parsed dict from gstore-manifest.json.

    Returns:
        True if valid, False otherwise.
    """
    if not _REQUIRED_TOP_LEVEL.issubset(manifest.keys()):
        return False

    catalog = manifest["catalog"]
    if not isinstance(catalog, list) or len(catalog) == 0:
        return False

    for entry in catalog:
        if not isinstance(entry, dict):
            return False
        if not _REQUIRED_ENTRY_FIELDS.issubset(entry.keys()):
            return False
        if not isinstance(entry["is_verified"], bool):
            return False
        checksum = entry.get("checksum", "")
        if not isinstance(checksum, str) or not checksum.startswith("sha256:"):
            return False

    return True
