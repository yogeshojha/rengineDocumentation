"""Read-only introspection of the reNgine 3.0 scan pipeline.

Run inside the api container (imports modules and prints JSON, writes nothing):

    docker exec -i rengine-api-1 /app/.venv/bin/python - \
        < scripts/dump_stage_catalog.py > data/stages.json 2> /dev/null

Everything under "stages[].fields", "intensity.profiles", "default_engine",
"presets", "execution_steps" and "resolution" comes from the live registry.
The hand-written parts are WRITES, PASSIVE_NOTE and UI_COPY below; each names
the source file it was read from.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from app.services.scan_engine.catalog import _field_specs, _resolve
from app.services.scan_engine.effects import stage_effects
from shared.definitions import constants, rescan
from shared.definitions.default_engine import (
    DEFAULT_ENGINE_DESCRIPTION,
    DEFAULT_ENGINE_INTENSITY,
    DEFAULT_ENGINE_NAME,
    default_engine_stages,
)
from shared.definitions.intensity import (
    PROFILES,
    RATE_TOOLS,
    TOOL_RETRIES,
    TOOL_TIMEOUT,
)
from shared.definitions.launch import STAGE_GROUP_LABELS
from shared.definitions.ports import (
    CDN_EDGE_PORTS,
    EXPOSURE_PORTS,
    PORT_PROFILES,
    SENSITIVE_PORTS,
    WEB_PORTS,
)
from shared.definitions.wordlists import (
    BUILTIN_ROOT,
    BUILTIN_WORDLISTS,
    CUSTOM_ROOT,
    DEFAULT_WORDLIST,
    MAX_WORD_LENGTH,
    MAX_WORDLIST_BYTES,
    MAX_WORDLIST_UPLOAD,
)
from shared.enums.scan import INTENSITIES
from shared.enums.target import TargetType
from shared.services.focused import focused_overrides
from shared.services.scan_resolve import merge_engine_context
from stages.presets import PRESETS, preset_stages
from stages.registry import execution_plan, rate_tools, stages

# what each stage stores, read from each stages/<dir>/stage.py
WRITES: dict[str, dict] = {
    "asset_seed": {
        "dimensions": ["web_assets", "ips", "endpoints", "services"],
        "note": "Subdomain rows for seeded hosts, IpAddress rows (source seed), Endpoint rows for URL seeds (source import or proxy), Port rows (source seed) for URL seeds on a non-default port.",
    },
    "lookalike_domains": {
        "dimensions": [],
        "note": "Lookalike rows for the target apex (lookalikes table). Not a surface dimension.",
    },
    "seed_resolution": {
        "dimensions": ["ips"],
        "note": "IpAddress rows with source seed, cidr_expansion or asn_expansion.",
    },
    "target_enrichment": {
        "dimensions": [],
        "note": "The target's DNS lookup, WHOIS record and BGP summary. Not a surface dimension.",
    },
    "session_check": {
        "dimensions": [],
        "note": "Nothing. The verdict is the stage's own status and note.",
    },
    "netblock_sweep": {
        "dimensions": ["web_assets"],
        "note": "Subdomain rows with source netblock for PTR names under the target.",
    },
    "reverse_dns": {
        "dimensions": ["ips"],
        "note": "IpAddress.ptr_hostnames.",
    },
    "subdomain_discovery": {
        "dimensions": ["web_assets"],
        "note": "Subdomain rows with sources, resolved_ips, cname, is_active, is_wildcard, is_excluded.",
    },
    "host_discovery": {
        "dimensions": ["ips"],
        "note": "IpAddress.is_alive.",
    },
    "cdn_check": {
        "dimensions": ["ips"],
        "note": "IpAddress rows for every known address, with cdn_type, cdn_name and is_cdn.",
    },
    "passive_ports": {
        "dimensions": ["services"],
        "note": "Port rows with source internetdb.",
    },
    "port_scan": {
        "dimensions": ["services", "ips"],
        "note": "Port rows with source naabu. IpAddress.scan_policy and scan_policy_reason.",
    },
    "vhost": {
        "dimensions": ["web_assets"],
        "note": "Subdomain rows for virtual hosts that answered.",
    },
    "http_probe": {
        "dimensions": ["web_assets", "services"],
        "note": "HttpAsset rows. Port rows with source http_probe. HTTP fields copied onto Subdomain rows for a domain target. Subdomain rows for referenced hostnames.",
    },
    "origin_probe": {
        "dimensions": ["web_assets", "vulnerabilities"],
        "note": "HttpAsset rows for addresses requested without a hostname. Origin exposure findings (scanner rengine).",
    },
    "service_fingerprint": {
        "dimensions": ["services"],
        "note": "Port service_name, product, version, banner and tls (source banner).",
    },
    "waf_detect": {
        "dimensions": ["web_assets"],
        "note": "HttpAsset.waf.",
    },
    "screenshot": {
        "dimensions": ["web_assets"],
        "note": "Image files under /app/scan_media/<scan id> and HttpAsset.screenshot_path, copied to Subdomain for a domain target.",
    },
    "dns_posture": {
        "dimensions": [],
        "note": "domain_posture rows, one per zone, folded onto host rows. Not a surface dimension.",
    },
    "takeover": {
        "dimensions": ["vulnerabilities"],
        "note": "Findings with template rengine-dangling-cname, severity medium.",
    },
    "zone_transfer": {
        "dimensions": ["vulnerabilities"],
        "note": "One finding with template rengine-zone-transfer, severity high.",
    },
    "ai_detection": {
        "dimensions": ["web_assets"],
        "note": "AI service verdicts on HttpAsset rows, folded onto host rows.",
    },
    "broken_links": {
        "dimensions": ["vulnerabilities"],
        "note": "Findings for embedded resources on a registrable domain.",
    },
    "content_discovery": {
        "dimensions": ["endpoints"],
        "note": "Endpoint rows with source fuzz.",
    },
    "url_discovery": {
        "dimensions": ["endpoints"],
        "note": "Endpoint rows per source and one EndpointCoverage row per source.",
    },
    "endpoint_probe": {
        "dimensions": ["endpoints"],
        "note": "Status, content type, length, title, hash, tech and stored response on Endpoint rows. One EndpointCoverage row.",
    },
    "ip_enrichment": {
        "dimensions": ["ips"],
        "note": "IpAddress rows for every address the scan found, with ASN, operator and country.",
    },
    "name_ownership": {
        "dimensions": ["vulnerabilities"],
        "note": "Findings for hostnames on third-party servers.",
    },
    "vulnerability_scan": {
        "dimensions": ["vulnerabilities"],
        "note": "Vulnerability rows (at most 20,000 per scan), VulnerabilityCoverage rows and scan surface items.",
    },
    "dast_scan": {
        "dimensions": ["vulnerabilities"],
        "note": "Vulnerability rows, VulnerabilityCoverage rows and scan surface items of class request and base.",
    },
    "secret_mining": {
        "dimensions": ["secrets"],
        "note": "Secret rows read from stored responses.",
    },
}

# what a passive_capable stage drops under passive intensity
PASSIVE_NOTE: dict[str, str] = {
    "subdomain_discovery": "Zone transfer, bruteforce and permutations are skipped with 'a passive scan does not query the target's nameservers'. A source with touches_target (tlsx) is skipped with 'a passive scan does not connect to the target'. Names are still resolved with dnsx. (stages/subdomain/stage.py:285-292, 335-338, 553-568)",
    "url_discovery": "Sources with touches_target (sitemap, crawl, js, api_spec) are skipped with 'This source sends requests to the target. A passive scan does not run it.' response_mining and archive stay. (stages/url_discovery/stage.py:179-185)",
    "dns_posture": "The MTA-STS policy file is not fetched (fetch_policy is False). DNS lookups run. (stages/dns_posture/stage.py:93,106)",
    "lookalike_domains": "Lookalike pages are not fetched, whatever page_similarity says. DNS lookups and RDAP run. (stages/lookalike_domains/stage.py:203-204)",
}

# frontend/src/lib/types/scan-engine.ts:7-27
UI_COPY = {
    "passive": {
        "label": "Passive",
        "tagline": "No traffic to the target.",
        "help": "Findings come from public sources only. No request reaches the target.",
    },
    "normal": {
        "label": "Normal",
        "tagline": "Default rates for every tool.",
        "help": "150 requests a second per tool. 1,000 packets a second for the port scan.",
    },
    "aggressive": {
        "label": "Aggressive",
        "tagline": "Higher rates and concurrency.",
        "help": "400 requests a second per tool. 3,000 packets a second for the port scan, and higher concurrency.",
    },
    "custom": {
        "label": "Custom",
        "tagline": "Rates and concurrency set per tool.",
        "help": "Rates and concurrency set per tool. An empty value uses the preset.",
    },
}


def _passive_behaviour(spec) -> str:
    if not spec.touches_target:
        return "unchanged"
    return "degraded" if spec.passive_capable else "disabled"


def _fields(spec) -> list[dict]:
    schema = spec.schema
    defs = schema.get("$defs") or {}
    props = schema.get("properties") or {}
    out = []
    for field in _field_specs(spec, {}):
        prop = _resolve(props.get(field.name) or {}, defs)
        out.append(
            {
                "name": field.name,
                "title": field.title,
                "type": field.type,
                "default": field.default,
                "choices": field.options,
                "choice_labels": field.option_labels,
                "minimum": field.minimum,
                "maximum": field.maximum,
                "max_length": prop.get("maxLength"),
                "max_items": prop.get("maxItems"),
                "description": field.description,
                "advanced": field.tier == "advanced",
                "launch": field.launch,
                "widget": field.widget,
                "widget_kind": field.kind,
                "needs": field.needs,
            }
        )
    return out


def _transport(spec) -> dict | None:
    if spec.transport_tool is None:
        return None
    by = {level: spec.transport(level) for level in INTENSITIES}
    return {
        "tool": spec.transport_tool,
        "rate": {level: t.rate for level, t in by.items()},
        "threads": {level: t.threads for level, t in by.items()},
        "timeout_seconds": by["normal"].timeout,
        "retries": by["normal"].retries,
        "rate_weight": spec.stage_cls.rate_weight,
        "thread_weight": spec.stage_cls.thread_weight,
    }


def _source(spec) -> str:
    path = Path(inspect.getsourcefile(spec.stage_cls))
    line = inspect.getsourcelines(spec.stage_cls)[1]
    return f"{path.relative_to('/app')}:{line}"


def _step_of() -> dict[str, int]:
    return {
        name: index for index, step in enumerate(execution_plan()) for name in step
    }


def _stage(spec, step: dict[str, int]) -> dict:
    writes = WRITES[spec.name]
    return {
        "id": spec.name,
        "label": spec.title,
        "description": spec.description,
        "source": _source(spec),
        "phase": spec.phase,
        "level": spec.level,
        "step": step[spec.name],
        "depends_on": sorted(spec.depends_on),
        "group": spec.group,
        "group_label": STAGE_GROUP_LABELS.get(spec.group),
        "role": spec.role,
        "tools": list(spec.tools),
        "api_keys": list(spec.api_keys),
        "requires_api_keys": spec.requires_api_keys,
        "touches_target": spec.touches_target,
        "passive_capable": spec.passive_capable,
        "always_on": spec.always_on,
        "catalog_hidden": spec.catalog_hidden,
        "deferrable": spec.deferrable,
        "default_enabled": bool(spec.defaults.get("enabled")),
        "passive_behaviour": _passive_behaviour(spec),
        "passive_note": PASSIVE_NOTE.get(spec.name),
        "target_types": sorted(spec.applies_to),
        "consumes": sorted(spec.consumes),
        "produces": sorted(spec.produces),
        "writes": writes["dimensions"],
        "writes_note": writes["note"],
        "check_of": spec.check_of,
        "finding_severities": list(spec.finding_severities),
        "launch_fields": list(spec.launch_fields),
        "transport": _transport(spec),
        "fields": _fields(spec),
    }


def _engine(stage_map: dict, intensity: str) -> SimpleNamespace:
    return SimpleNamespace(
        id=None,
        name="introspection",
        intensity=intensity,
        global_headers=[],
        stages=stage_map,
        tool_options={},
        transport_overrides={},
    )


_SAMPLE = {
    "domain": "example.com",
    "ip": "192.0.2.10",
    "ip_range": "192.0.2.0/24",
    "asn": "AS64496",
    "url": "https://example.com/app",
}


def _resolution(stage_map: dict) -> dict:
    """Per target type and intensity, what the launch preview says each stage does."""
    out: dict = {}
    for target_type in (t.value for t in TargetType):
        out[target_type] = {}
        for level in INTENSITIES:
            resolved = merge_engine_context(
                _engine(stage_map, level), None, _SAMPLE[target_type], target_type
            )
            phases, warnings = stage_effects(resolved, set())
            rows = {}
            for phase in phases:
                for tool in phase.tools:
                    rows[tool.capability] = {
                        "status": tool.status.value,
                        "reason": tool.reason,
                        "rate": tool.rate,
                        "threads": tool.threads,
                        "timeout": tool.timeout,
                    }
            out[target_type][level] = {"stages": rows, "warnings": warnings}
    return out


def _wordlists() -> list[dict]:
    rows = []
    for item in BUILTIN_WORDLISTS:
        path = Path(BUILTIN_ROOT) / item.filename
        lines = sample = None
        if path.is_file():
            words = [w for w in path.read_text(errors="replace").splitlines() if w]
            lines = len(words)
            sample = words[:10]
        rows.append({**item.model_dump(), "words": lines, "first_words": sample})
    return rows


def main() -> None:
    specs = stages()
    step = _step_of()
    default_map = default_engine_stages()
    passive_resolved = merge_engine_context(
        _engine({}, "passive"), None, "example.com", "domain"
    )
    out = {
        "generated_by": "scripts/dump_stage_catalog.py",
        "stage_count": len(specs),
        "stages": [_stage(spec, step) for spec in specs],
        "execution_steps": [list(s) for s in execution_plan()],
        "groups": [{"key": k, "label": v} for k, v in STAGE_GROUP_LABELS.items()],
        "intensity": {
            "levels": list(INTENSITIES),
            "ui_copy": UI_COPY,
            "profiles": {
                level: {
                    tool: {"rate": rate, "threads": threads}
                    for tool, (rate, threads) in PROFILES[level].items()
                }
                for level in INTENSITIES
            },
            "tool_timeout_seconds": dict(TOOL_TIMEOUT),
            "tool_retries": dict(TOOL_RETRIES),
            "rate_tools_defined": list(RATE_TOOLS),
            "rate_tools_tunable": list(rate_tools()),
            "limits": {
                "MAX_RATE": constants.MAX_RATE,
                "MAX_THREADS": constants.MAX_THREADS,
                "MAX_TIMEOUT": constants.MAX_TIMEOUT,
            },
            "disabled_under_passive": sorted(
                s.name for s in specs if s.touches_target and not s.passive_capable
            ),
            "degraded_under_passive": sorted(
                s.name for s in specs if s.touches_target and s.passive_capable
            ),
            "unchanged_under_passive": sorted(
                s.name for s in specs if not s.touches_target
            ),
            "resolved_enabled_at_passive_with_all_defaults": {
                name: values.get("enabled")
                for name, values in passive_resolved.stages.items()
            },
            "passive_notes": PASSIVE_NOTE,
        },
        "default_engine": {
            "name": DEFAULT_ENGINE_NAME,
            "description": DEFAULT_ENGINE_DESCRIPTION,
            "intensity": DEFAULT_ENGINE_INTENSITY,
            "builtin": True,
            "stages": default_map,
            "resolution": _resolution(default_map),
        },
        "presets": [
            {
                "name": p.name,
                "title": p.title,
                "description": p.description,
                "intensity": p.intensity,
                "stages": preset_stages(p.name),
            }
            for p in PRESETS
        ],
        "rescan": {
            "max_assets": rescan.MAX_RUN_ASSETS,
            "max_scans": rescan.MAX_RUN_SCANS,
            "max_templates": rescan.MAX_RUN_TEMPLATES,
            "rescannable_stages": sorted(rescan.RESCANNABLE_STAGES),
            "dimension_seed": dict(rescan.DIMENSION_SEED),
            "dimension_stages": {k: list(v) for k, v in rescan.DIMENSION_STAGES.items()},
            "focused_overrides": {
                dimension: focused_overrides(names)
                for dimension, names in rescan.DIMENSION_STAGES.items()
            },
        },
        "port_profiles": {
            "profiles": [
                {
                    "key": p.key,
                    "label": p.label,
                    "description": p.description,
                    "approx": p.approx,
                }
                for p in PORT_PROFILES
            ],
            "web_ports": list(WEB_PORTS),
            "sensitive_ports": list(SENSITIVE_PORTS),
            "exposure_ports": list(EXPOSURE_PORTS),
            "cdn_edge_ports": list(CDN_EDGE_PORTS),
        },
        "wordlists": {
            "builtin_root": BUILTIN_ROOT,
            "custom_root": CUSTOM_ROOT,
            "default": dict(DEFAULT_WORDLIST),
            "max_bytes": MAX_WORDLIST_BYTES,
            "max_upload": MAX_WORDLIST_UPLOAD,
            "max_word_length": MAX_WORD_LENGTH,
            "builtin": _wordlists(),
        },
    }
    json.dump(out, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


main()
