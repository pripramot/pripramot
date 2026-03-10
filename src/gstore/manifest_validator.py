def validate(manifest: dict) -> bool:
    # minimal validation for MVP
    return manifest.get("project") == "GSTORE"
