"""Read-only: the document GET /engines/{id}/export builds for the built-in Default engine.

    docker exec -i rengine-api-1 /app/.venv/bin/python - \
        < scripts/dump_default_engine_yaml.py > data/default-engine.yaml 2> /dev/null

Mirrors ScanEngineService.export_yaml (api/app/services/scan_engine/service.py:329-344)
without reading the database: the engine row is the one ensure_builtin writes.
"""
import sys

import yaml

from app.services.scan_engine.validation import _full_stages, _validate_stages
from shared.definitions.default_engine import (
    DEFAULT_ENGINE_DESCRIPTION,
    DEFAULT_ENGINE_INTENSITY,
    DEFAULT_ENGINE_NAME,
    default_engine_stages,
)

stored = _validate_stages(default_engine_stages())
data = {
    "name": DEFAULT_ENGINE_NAME,
    "description": DEFAULT_ENGINE_DESCRIPTION,
    "intensity": DEFAULT_ENGINE_INTENSITY,
    "global_headers": [],
    "stages": _full_stages(stored),
    "transport_overrides": {},
    "tool_options": {},
}
sys.stdout.write(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
sys.stderr.write(f"stored sparse stages: {stored!r}\n")
