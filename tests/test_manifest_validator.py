from src.gstore.manifest_validator import validate

# ---------------------------------------------------------------------------
# Happy-path
# ---------------------------------------------------------------------------

def test_manifest_valid_sample():
    """Full, correct manifest is accepted."""
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100},
        "forensic_logging": {
            "format": "json",
            "required_fields": ["timestamp", "level", "service"],
            "retention_days": 90,
            "storage": "centralized-log-bucket",
            "sensitive_data_policy": "mask_or_remove_pii",
        },
        "testing": {"unit_test_framework": "pytest", "coverage_threshold": 80},
    }
    assert validate(sample) is True


# ---------------------------------------------------------------------------
# Failure cases
# ---------------------------------------------------------------------------

def test_manifest_wrong_project_name():
    """Wrong project name must be rejected."""
    sample = {
        "project": "OTHER",
        "forensic_logging": {
            "format": "json",
            "required_fields": [],
            "retention_days": 30,
            "storage": "local",
            "sensitive_data_policy": "none",
        },
        "testing": {},
    }
    assert validate(sample) is False


def test_manifest_missing_project_key():
    """Missing project key must be rejected."""
    assert validate({}) is False


def test_manifest_missing_forensic_logging():
    """Manifest without forensic_logging section must be rejected."""
    assert validate({"project": "GSTORE", "testing": {}}) is False


def test_manifest_forensic_logging_missing_required_field():
    """forensic_logging section with a missing required field must be rejected."""
    sample = {
        "project": "GSTORE",
        "forensic_logging": {
            "format": "json",
            "required_fields": [],
            # retention_days, storage, sensitive_data_policy are missing
        },
        "testing": {},
    }
    assert validate(sample) is False


def test_manifest_missing_testing_section():
    """Manifest without a testing section must be rejected."""
    sample = {
        "project": "GSTORE",
        "forensic_logging": {
            "format": "json",
            "required_fields": [],
            "retention_days": 30,
            "storage": "local",
            "sensitive_data_policy": "none",
        },
    }
    assert validate(sample) is False


def test_manifest_forensic_logging_not_a_dict():
    """forensic_logging must be a dict, not a scalar."""
    assert validate({"project": "GSTORE", "forensic_logging": "json", "testing": {}}) is False
