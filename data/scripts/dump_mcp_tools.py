"""Dump the reNgine MCP registry as JSON. Read-only: imports modules and prints.

Run:
  docker exec -i rengine-api-1 /app/.venv/bin/python - < dump_mcp_tools.py > mcp-tools.json

Everything is read from the live registry except RETURNS and TRAFFIC, which are
written by hand from the `run` method of each tool in mcp/tools/*.py.
"""

import json
import sys

from mcp import clients, registry, server
from mcp import settings as s
from mcp.capabilities import (
    ALWAYS_GRANTED,
    CAPABILITY_HELP,
    CAPABILITY_LABELS,
    CAPABILITY_ORDER,
    CAPABILITY_REACH,
    DEFAULT_CEILING,
    TOUCHES_TARGETS,
)
from mcp.service import context_tokens

RETURNS = {
    "resolve_target": "data.target{id,value,type,project_id}; data.surface[] one entry per dimension {dimension,label,covered,count,observed_at,scan_id,is_latest_scan,added,gone,previous}; data.risk{total,actionable,kev,suppressed,by_severity[]}; data.scans{total,running,failed,last_completed_at}; data.sensitive_services; data.monitored. open_in_rengine: /targets/<target id>. Caveats name dimensions not scanned and scans running.",
    "surface_brief": "data{dimension,scan_id,total_in_scope,total_capped,leads[{query,count,capped,means,group}]} - up to 60 curated queries counted against the most recent covering scan; zero-count queries omitted unless include_empty. open_in_rengine: /scans/<scan id>?tab=<dimension tab>.",
    "describe_query_language": "data{dimension,noun,max_query_length,connectors[{symbol,means}],operators[{symbol,means}],flags[{flag,means}],fields[{name,type,operators,means,example,values?,aliases?}],group_keys[{key,label,means}],examples[{query,means}] (first 20)}; with fields_only: data{dimension,fields[names]}. No open_in_rengine link.",
    "list_targets": "data{scope ('all projects' or the project name),total,targets[{value,type,project,added_at}]} ordered by value, cut at limit. open_in_rengine: /targets.",
    "list_projects": "data[] of {id,name,slug} for each active project the token reaches. open_in_rengine: /dashboard.",
    "list_engines": "data[] of {id,name,description,intensity,stages[enabled stage names],last_used_at}. open_in_rengine: /automation/engines.",
    "list_contexts": "data[] of {id,name,description,auth,rate_limit_per_minute,excluded{hosts,paths,addresses},only_these_hosts,through_proxy,last_used_at}. Credentials are not returned. open_in_rengine: /automation/contexts.",
    "scan_status": "With scan or target: data{scan_id,status,engine,started_at,completed_at,elapsed_seconds,stages{done,running,failed,skipped},found_so_far{label:count},error}; open_in_rengine: /scans/<scan id>. With neither: data[] of {scan_id,target,engine,status,started_at,elapsed_seconds} for live scans, or the most recent runs when nothing is running; open_in_rengine: /scans.",
    "query_assets": "data{dimension,query,total,total_capped,returned,offset,rows[]} - rows carry a subset of columns for the dimension. open_in_rengine: /scans/<scan id>?tab=<tab>&q=<query> when a target is named, else /surface/<tab>?q=<query>. Flagged untrusted_content when rows are returned.",
    "group_assets": "data{dimension,group_by,rows_in_scope,rows_with_a_value,total_groups,groups[{value,count,query}]} - largest 40 groups. open_in_rengine: /scans/<scan id>?tab=<tab>&q=<query>. Flagged untrusted_content.",
    "what_changed": "data{window,generated_at,targets{total,scanned,never_scanned,stale,monitored},risk,changes[{target,type,runs,last_scan_at,last_status,new{},first_time_covered[],web_assets_gone}]} - up to 30 targets. open_in_rengine: /dashboard.",
    "compare_runs": "data{target,baseline{scan_id,engine,started_at},current{scan_id,engine,started_at},comparability,run_setup[{what,baseline,current,material}],runs_between,dimensions[{dimension,comparability,covered,appeared,changed,disappeared,unconfirmed,unchanged,was,now}]}; with dimension: also changes[{verb,signal,asset,where,severity,fields[{field,was,now}]}] (up to 25) and changes_total. open_in_rengine: /scans/compare?current=<id>&baseline=<id>. Flagged untrusted_content.",
    "cve_exposure": "data{cve,record{known,severity,cvss_score,epss_score,epss_percentile,known_exploited,ransomware,kev_due_date,published_at},exposure{assets,targets,software_rows,finding_rows,first_seen,ladder[{evidence,count,software,findings}]},by_target[{target,assets,software,findings,first_seen}],locations[{host,ip,port,evidence,basis,dimension,state,target,first_seen}] (up to 50),locations_total}. open_in_rengine: /surface/cve/<CVE id>. Flagged untrusted_content.",
    "domain_posture": "data{target,scan_id,zones_checked,mail_hosts_checked,warning,info,clean,spoofable,checks[{check,label,tone,failing,applicable,fix}],zones[{zone,under,web_assets,spf,spf_lookups,dmarc,dmarc_subdomains,dmarc_inherited,dkim_selectors,dkim_key_bits,mail,mta_sts,tls_rpt,dnssec,caa,failing[],evidence{}}] (up to 25)}. open_in_rengine: /targets/<target id>. Flagged untrusted_content. Errors when posture was never checked.",
    "explain_finding": "data{check{template_id,name,severity,scanner,description,impact,remediation,references,tags},risk{cve_ids,cwe_ids,cvss_score,epss_score,epss_percentile,known_exploited},review{state,reason},occurrences,set_aside,locations[{matched_at,host,ip,port,state,is_new}] (up to 25),evidence{matched_at,extracted,curl}}. open_in_rengine: /scans/<scan id>?tab=vulnerabilities&q=template=\"<id>\". Flagged untrusted_content.",
    "scan_coverage": "data{dimension,scan_id,runs[coverage rows with empty values dropped],surface[{dimension,covered,count}]}. open_in_rengine: /scans/<scan id>?tab=<tab>.",
    "plan_scan": "data{target,target_type,engine,context,summary,phases[{phase,stages[{stage,label,status,reason}]}],warnings}. Caveat 'Nothing ran.' No open_in_rengine link.",
    "start_scan": "data{scan_id,status,engine,target,target_id,started_at}. open_in_rengine: /scans/<scan id>. Caveats state whether traffic is sent, and name the agent token.",
    "focused_rescan": "data{scan_id,parent_scan_id,dimension,assets (count),stages,status}. open_in_rengine: /scans/<new scan id>.",
    "pause_scan": "data{scan_id,status,engine,kept{label:count}}. open_in_rengine: /scans/<scan id>.",
    "resume_scan": "data{scan_id,status,engine}. open_in_rengine: /scans/<scan id>.",
    "cancel_scan": "data{scan_id,status,engine,kept{label:count}}. open_in_rengine: /scans/<scan id>.",
    "record_triage": "data{fingerprint,state,reason,observations_updated}. open_in_rengine: /scans/<scan id>?tab=vulnerabilities.",
    "add_target": "data{project,created[{id,value,type,link}],already_present[],rejected[]}. open_in_rengine: /targets/<id> when exactly one target was created and none existed, else /targets.",
    "update_target": "data{value,display_name,tags[],organizations[]}. open_in_rengine: /targets/<target id>.",
    "delete_target": "Without confirm=true: a tool error (isError) whose text states what the delete would remove. With confirm=true: data{value,scans_deleted,results_deleted{label:count}}; open_in_rengine: /targets.",
}

# Whether the call itself causes traffic to reach a scanned target, read from each run().
TRAFFIC = {
    "start_scan": "Yes, unless the resolved intensity is passive (caveat: 'Passive intensity. No traffic reaches the target.').",
    "focused_rescan": "Yes (caveat: 'Traffic is being sent to these assets.').",
    "resume_scan": "Yes: the paused run restarts at its first unfinished stage.",
    "pause_scan": "No new traffic: stages in flight stop.",
    "cancel_scan": "No new traffic: stages in flight are aborted.",
    "add_target": "No scan. Queues WHOIS, DNS and routing enrichment.",
    "plan_scan": "No. Nothing runs and the target is not contacted.",
}


def type_of(prop: dict) -> str:
    if "anyOf" in prop:
        return " | ".join(type_of(p) for p in prop["anyOf"])
    kind = prop.get("type", "any")
    if kind == "array":
        return f"array<{type_of(prop.get('items', {}))}>"
    return kind


CONSTRAINT_KEYS = (
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "minLength",
    "maxLength",
    "minItems",
    "maxItems",
    "enum",
)


def constraints(prop: dict) -> dict:
    out = {k: prop[k] for k in CONSTRAINT_KEYS if k in prop}
    for branch in prop.get("anyOf", []):
        for k in CONSTRAINT_KEYS:
            if k in branch:
                out[k] = branch[k]
    return out


def default_of(model, name: str):
    field = model.model_fields[name]
    if field.is_required():
        return None
    if field.default_factory is not None:
        return field.default_factory()
    return field.default


def params(schema: dict, model) -> list[dict]:
    required = set(schema.get("required", []))
    rows = []
    for name, prop in schema.get("properties", {}).items():
        rows.append(
            {
                "name": name,
                "type": type_of(prop),
                "required": name in required,
                "default": default_of(model, name),
                "description": prop.get("description", ""),
                "constraints": constraints(prop),
            }
        )
    return rows


tools = []
for spec in registry.registry().values():
    descriptor = spec.descriptor()
    tools.append(
        {
            "name": spec.name,
            "title": spec.title,
            "group": spec.group,
            "capability": spec.capability,
            "description": spec.description,
            "touches_target": spec.capability in TOUCHES_TARGETS,
            "traffic_note": TRAFFIC.get(spec.name, "No. Reads or writes reNgine's own database."),
            "read_only_hint": descriptor["annotations"]["readOnlyHint"],
            "destructive_hint": descriptor["annotations"]["destructiveHint"],
            "chat_command": spec.command,
            "chat_value_field": spec.value_field or None,
            "examples": list(spec.examples),
            "context_tokens": context_tokens(descriptor),
            "params": params(spec.schema, spec.tool_cls.Input),
            "returns": RETURNS.get(spec.name, ""),
            "input_schema": spec.schema,
        }
    )

group_order = ["Orient", "Interrogate", "Explain", "Act"]
tools.sort(key=lambda t: (group_order.index(t["group"]), t["name"]))

out = {
    "server": {
        "name": s.SERVER_NAME,
        "protocol": s.PROTOCOL_VERSION,
        "supported_protocols": list(s.SUPPORTED_PROTOCOLS),
        "endpoint": s.HTTP_PATH,
        "endpoint_url_shape": "<UI origin>" + s.HTTP_PATH,
        "stdio_command": s.stdio_command(),
        "default_rate_limit_per_minute": s.DEFAULT_RATE_LIMIT,
        "methods": sorted(str(m) for m in server._HANDLERS) + ["notifications/initialized"],
        "instructions": server.INSTRUCTIONS,
    },
    "capabilities": [
        {
            "id": key,
            "label": CAPABILITY_LABELS[key],
            "description": CAPABILITY_HELP[key],
            "reach": CAPABILITY_REACH[key],
            "always_granted": key in ALWAYS_GRANTED,
            "touches_targets": key in TOUCHES_TARGETS,
            "default_ceiling": DEFAULT_CEILING[key],
        }
        for key in CAPABILITY_ORDER
    ],
    "clients": [
        {
            "key": c["key"],
            "label": c["label"],
            "where": c["where"],
            "lang": c["lang"],
            "text": c["text"],
        }
        for c in clients.snippets("<ENDPOINT_URL>", "<TOKEN>")
    ],
    "tool_count": len(tools),
    "tools": tools,
}

json.dump(out, sys.stdout, indent=2, default=str)
sys.stdout.write("\n")
