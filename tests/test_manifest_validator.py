import pytest

from src.gstore.manifest_validator import validate


@pytest.fixture()
def valid_manifest():
    """Return a minimal valid GSTORE manifest."""
    return {
        "project": "GSTORE",
        "coding_style": {"line_length": 100, "formatter": "black", "linter": "flake8"},
        "testing": {"unit_test_framework": "pytest", "coverage_threshold": 80},
    }


# --- Valid manifests ---


def test_manifest_valid_sample(valid_manifest):
    assert validate(valid_manifest) is True


def test_manifest_valid_with_extra_fields(valid_manifest):
    valid_manifest["forensic_logging"] = {"format": "json"}
    valid_manifest["coding_style"]["extra"] = True
    assert validate(valid_manifest) is True


# --- Invalid manifests ---


def test_manifest_wrong_project_name(valid_manifest):
    valid_manifest["project"] = "OTHER"
    assert validate(valid_manifest) is False


def test_manifest_missing_project(valid_manifest):
    del valid_manifest["project"]
    assert validate(valid_manifest) is False


def test_manifest_missing_coding_style(valid_manifest):
    del valid_manifest["coding_style"]
    assert validate(valid_manifest) is False


def test_manifest_missing_testing(valid_manifest):
    del valid_manifest["testing"]
    assert validate(valid_manifest) is False


def test_manifest_coding_style_missing_formatter(valid_manifest):
    del valid_manifest["coding_style"]["formatter"]
    assert validate(valid_manifest) is False


def test_manifest_coding_style_missing_linter(valid_manifest):
    del valid_manifest["coding_style"]["linter"]
    assert validate(valid_manifest) is False


def test_manifest_coding_style_missing_line_length(valid_manifest):
    del valid_manifest["coding_style"]["line_length"]
    assert validate(valid_manifest) is False


def test_manifest_testing_missing_framework(valid_manifest):
    del valid_manifest["testing"]["unit_test_framework"]
    assert validate(valid_manifest) is False


def test_manifest_empty_dict():
    assert validate({}) is False


def test_manifest_none_input():
    assert validate(None) is False


def test_manifest_string_input():
    assert validate("not a dict") is False


def test_manifest_coding_style_not_dict(valid_manifest):
    valid_manifest["coding_style"] = "invalid"
    assert validate(valid_manifest) is False


def test_manifest_testing_not_dict(valid_manifest):
    valid_manifest["testing"] = "invalid"
    assert validate(valid_manifest) is False
