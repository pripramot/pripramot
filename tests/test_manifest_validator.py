from src.gstore.manifest_validator import validate


# --- Valid manifests ---


def test_manifest_valid_sample():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest", "coverage_threshold": 80},
    }
    assert validate(sample) is True


def test_manifest_valid_with_extra_fields():
    sample = {
        "project": "GSTORE",
        "coding_style": {
            "line_length": 100,
            "formatter": "black",
            "linter": "flake8",
            "extra": True,
        },
        "testing": {"unit_test_framework": "pytest"},
        "forensic_logging": {"format": "json"},
    }
    assert validate(sample) is True


# --- Invalid manifests ---


def test_manifest_wrong_project_name():
    sample = {
        "project": "OTHER",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_missing_project():
    sample = {
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_missing_coding_style():
    sample = {
        "project": "GSTORE",
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_missing_testing():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
    }
    assert validate(sample) is False


def test_manifest_coding_style_missing_formatter():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_coding_style_missing_linter():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black"},
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_coding_style_missing_line_length():
    sample = {
        "project": "GSTORE",
        "coding_style": {"formatter": "black", "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_testing_missing_framework():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": {"coverage_threshold": 80},
    }
    assert validate(sample) is False


def test_manifest_empty_dict():
    assert validate({}) is False


def test_manifest_none_input():
    assert validate(None) is False


def test_manifest_string_input():
    assert validate("not a dict") is False


def test_manifest_coding_style_not_dict():
    sample = {
        "project": "GSTORE",
        "coding_style": "invalid",
        "testing": {"unit_test_framework": "pytest"},
    }
    assert validate(sample) is False


def test_manifest_testing_not_dict():
    sample = {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": "invalid",
    }
    assert validate(sample) is False
