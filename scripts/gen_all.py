"""Run every reference generator."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for name in ("gen_query", "gen_stages", "gen_mcp", "gen_api", "gen_ops", "gen_chat", "gen_shortcuts"):
    importlib.import_module(name).main()
