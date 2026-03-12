REQUIRED_MANIFEST_FIELDS = {"project", "coding_style", "testing"}
REQUIRED_CODING_STYLE_FIELDS = {"line_length", "formatter", "linter"}


def validate(manifest: dict) -> bool:
    """Validate a GSTORE project manifest.

    Checks that the manifest contains the required top-level fields, the correct
    project identifier, and that nested sections include their mandatory keys.
    """
    if not isinstance(manifest, dict):
        return False
    if manifest.get("project") != "GSTORE":
        return False
    if not REQUIRED_MANIFEST_FIELDS.issubset(manifest.keys()):
        return False

    coding_style = manifest.get("coding_style")
    if not isinstance(coding_style, dict):
        return False
    if not REQUIRED_CODING_STYLE_FIELDS.issubset(coding_style.keys()):
        return False

    testing = manifest.get("testing")
    if not isinstance(testing, dict):
        return False
    if "unit_test_framework" not in testing:
        return False

    return True
