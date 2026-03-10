import logging
from pythonjsonlogger import jsonlogger

def configure_json_logging(service_name: str = "gstore"):
    handler = logging.StreamHandler()
    fmt = '%(asctime)s %(levelname)s %(name)s %(service)s %(trace_id)s %(span_id)s %(message)s'
    formatter = jsonlogger.JsonFormatter(fmt)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)
    root.setLevel(logging.INFO)

    # attach default extra fields via LoggerAdapter when needed
    return logging.LoggerAdapter(logging.getLogger(service_name), {"service": service_name})
