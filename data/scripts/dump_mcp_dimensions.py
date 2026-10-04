"""Print the result dimensions the MCP tools accept. Read-only."""
import json
from mcp.dimensions import DIMENSIONS, DIMENSION_KEYS, MAX_ROWS, DEFAULT_ROWS
from shared.definitions.surface import SURFACE_ORDER, SURFACE_LABELS, SURFACE_NOUN, SURFACE_COLUMNS
from shared.definitions.dashboard import WINDOW_DELTAS, DEFAULT_WINDOW, CHANGES_LIMIT
from shared.enums.scan import INTENSITIES, SCAN_LIVE_STATUSES, SCAN_OPEN_STATUSES
from shared.definitions.channels import CHANNEL_ORDER
from shared.definitions.ask import ASK_CLIENT
by = {d.key: d for d in DIMENSIONS}
print(json.dumps({
  "surface_order": list(SURFACE_ORDER),
  "dimension_keys": list(DIMENSION_KEYS),
  "dimensions": [{"key": k, "label": SURFACE_LABELS[k], "noun": list(SURFACE_NOUN[k]), "tab": by[k].tab, "columns": list(SURFACE_COLUMNS[k]), "paging": list(by[k].page_args)} for k in DIMENSION_KEYS],
  "max_rows": MAX_ROWS, "default_rows": DEFAULT_ROWS,
  "windows": list(WINDOW_DELTAS), "default_window": DEFAULT_WINDOW, "changes_limit": CHANGES_LIMIT,
  "intensities": list(INTENSITIES),
  "scan_live_statuses": sorted(str(s) for s in SCAN_LIVE_STATUSES),
  "scan_open_statuses": sorted(str(s) for s in SCAN_OPEN_STATUSES),
  "hidden_clients": [*CHANNEL_ORDER, ASK_CLIENT],
}, indent=1, default=str))
try:
    from app.services.rescan import rescan_schema
    s = rescan_schema()
    print(json.dumps({"rescannable_stages": list(s.rescannable_stages), "rescan_dimensions": [{"dimension": d.dimension, "default_stages": list(d.default_stages), "noun_plural": d.noun_plural} for d in s.dimensions]}, indent=1, default=str))
except Exception as exc:
    print("rescan_schema unavailable:", type(exc).__name__, exc)
