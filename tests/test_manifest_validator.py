from src.gstore.manifest_validator import validate

def test_manifest_valid_sample():
    sample = {"project": "GSTORE", "coding_style": {"line_length": 100}}
    assert validate(sample) is True
