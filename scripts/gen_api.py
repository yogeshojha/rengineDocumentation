"""Write reference/http-api.md and developers/api/search-*.md from data/openapi.json, data/route-access.json and data/query-schema.json."""

from __future__ import annotations

import json
import sys

from gen_common import DOCS, code, front_matter, gen_line, load, sentence, table, write

SCRIPT = "scripts/gen_api.py"
METHODS = ("get", "post", "put", "patch", "delete")

SEARCH = {
    "web_assets": ("search-web-assets", "Search web assets", "/api/v1/subdomains/search", "api/app/api/v1/subdomains.py"),
    "endpoints": ("search-endpoints", "Search endpoints", "/api/v1/endpoints/search", "api/app/api/v1/endpoints.py"),
    "services": ("search-services", "Search services", "/api/v1/ports/search", "api/app/api/v1/ports.py"),
    "ips": ("search-ips", "Search IP addresses", "/api/v1/ips/search", "api/app/api/v1/ip_addresses.py"),
    "vulnerabilities": ("search-vulnerabilities", "Search vulnerabilities", "/api/v1/vulnerabilities/search", "api/app/api/v1/vulnerabilities.py"),
    "software": ("search-software", "Search software", "/api/v1/software/search", "api/app/api/v1/software.py"),
    "secrets": ("search-secrets", "Search secrets", "/api/v1/secrets/search", "api/app/api/v1/secrets.py"),
}
QUERY_PAGES = {
    "web_assets": "web-assets", "endpoints": "endpoints", "services": "services", "ips": "ips",
    "vulnerabilities": "vulnerabilities", "software": "software", "secrets": "secrets",
}
HAND_PAGES = {
    ("post", "/api/v1/scans/batch"): "../developers/api/start-scan.md",
    ("get", "/api/v1/scans/{id}"): "../developers/api/get-scan.md",
    ("get", "/api/v1/scans/compare"): "../developers/api/compare-runs.md",
    ("post", "/api/v1/targets"): "../developers/api/create-target.md",
    ("post", "/api/v1/exports"): "../developers/api/export.md",
}
EXAMPLES = {
    "web_assets": ("tech:jenkins is:live", {"name": "ci.example.com", "http_status": 200, "page_title": "Dashboard [Jenkins]",
                                            "tech": ["Jenkins", "Jetty"], "resolved_ips": ["203.0.113.10"]}),
    "endpoints": ("is:param and is:live", {"url": "https://shop.example.com/api/cart?id=", "status_code": 200,
                                           "param_count": 1, "endpoint_class": "api", "sources": ["crawl"]}),
    "services": ("port:22 and is:sensitive", {"ip": "203.0.113.10", "port": 22, "service_name": "ssh",
                                              "product": "OpenSSH", "version": "9.6", "is_sensitive": True}),
    "ips": ("is:open not is:cdn", {"ip": "203.0.113.10", "version": 4, "asn_org": "Example Hosting",
                                  "port_count": 3, "host_count": 2, "is_cdn": False}),
    "vulnerabilities": ("severity:critical or is:kev", {"template_id": "CVE-2024-23897", "severity": "critical",
                                                        "host": "ci.example.com", "is_kev": True, "cve_ids": ["CVE-2024-23897"]}),
    "software": ("severity:critical and is:stated", {"cve": "CVE-2023-25690", "name": "Apache HTTP Server", "version": "2.4.54",
                                                     "severity": "critical", "version_source": "banner", "host": "www.example.com"}),
    "secrets": ("group:cloud and is:exposed", {"kind": "aws_access_key", "group": "cloud", "state": "exposed",
                               "host": "app.example.com", "url": "https://app.example.com/static/app.js"}),
}
COMMON_BODY = {
    "q": "Query in the grammar of the dimension. Empty or null returns every row in scope.",
    "ids": "Only these row ids.",
    "sort": "Sort key.",
    "order": "`asc` or `desc`.",
    "direction": "`asc` or `desc`.",
    "limit": "Rows per page.",
    "offset": "Rows to skip.",
    "page": "Page number.",
    "size": "Rows per page.",
}
ACCESS = {
    "user": "Signed-in user",
    "administrator": "Administrator",
    "connector": "Connector token",
    "mcp": "MCP token",
    "none": "None",
}


def resolve(schema: dict, S: dict) -> dict:
    while "$ref" in schema:
        schema = S[schema["$ref"].split("/")[-1]]
    return schema


def type_of(schema: dict, S: dict) -> str:
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    if "anyOf" in schema:
        parts = [type_of(s, S) for s in schema["anyOf"]]
        return " or ".join(dict.fromkeys(p for p in parts))
    t = schema.get("type")
    if t == "array":
        return f"array of {type_of(schema.get('items', {}), S)}"
    if t == "string" and schema.get("format"):
        return f"string ({schema['format']})"
    if "enum" in schema:
        return " or ".join(code(v) for v in schema["enum"])
    return t or "object"


def limits_of(schema: dict) -> str:
    parts = []
    for s in [schema] + schema.get("anyOf", []):
        if "maxLength" in s:
            parts.append(f"at most {s['maxLength']:,} characters")
        if "maxItems" in s:
            parts.append(f"at most {s['maxItems']:,} items")
        if "minimum" in s or "maximum" in s:
            lo, hi = s.get("minimum"), s.get("maximum")
            fmt = lambda v: f"{int(v):,}" if isinstance(v, float) and v.is_integer() else str(v)
            parts.append(f"{fmt(lo) if lo is not None else ''} to {fmt(hi) if hi is not None else ''}".strip())
    return ", ".join(dict.fromkeys(parts)).capitalize()


def default_of(schema: dict) -> str:
    if "default" not in schema:
        return ""
    d = schema["default"]
    if isinstance(d, bool):
        return code("true" if d else "false")
    if d is None:
        return code("null")
    if isinstance(d, (list, dict)):
        return code(json.dumps(d))
    return code(d)


def access_map() -> dict:
    out = {}
    for r in load("route-access.json"):
        level = r["access"]
        if level == "none" and r["path"].startswith("/api/v1/connectors"):
            level = "connector"
        if level == "none" and r["path"].startswith("/api/v1/mcp"):
            level = "mcp"
        out[(r["method"].lower(), r["path"])] = level
    return out


def index_page(o: dict, access: dict) -> str:
    paths = o["paths"]
    ops = [(m, p, op) for p, v in paths.items() for m, op in v.items() if m in METHODS]
    tags: dict[str, list] = {}
    for m, p, op in ops:
        for t in op.get("tags", ["untagged"]):
            tags.setdefault(t, []).append((m, p, op))
    out = front_matter(
        "HTTP API paths",
        f"All {len(paths)} paths and {len(ops)} operations of the reNgine HTTP API, in {len(tags)} tags, "
        "with the access each operation requires. Use it to find the operation you want to call and check who may call it.",
        ["api/app/main.py", "api/app/api/v1/", "api/app/api/deps.py"], SCRIPT, layout="reference")
    out += gen_line(["openapi.json", "route-access.json"], SCRIPT)
    out += ("Every path is relative to the address you open the interface on. "
            "The **Access** column tells you what an operation checks before it runs: "
            "a signed-in user, an administrator, a connector token, an MCP token, or nothing. "
            "To call the API from a script, see [Authentication](../developers/api/authentication.md). "
            "For error responses and limits, see [Errors, limits and counts](../developers/api/errors.md).\n\n")
    out += "This is how the operations divide by access.\n\n"
    counts = {}
    for m, p, _ in ops:
        counts[access.get((m, p), "none")] = counts.get(access.get((m, p), "none"), 0) + 1
    out += table(["Access", "Operations"], [[ACCESS[k], str(v)] for k, v in sorted(counts.items(), key=lambda kv: -kv[1])])
    out += "## Tags\n\n"
    out += ("Each tag below lists its operations, with a summary and the access each one requires. "
            "Where a path has its own page, the path links to it. Jump to a tag:\n\n")
    out += ", ".join(f"[{t}](#{tag_id(t)})" for t in sorted(tags, key=str.lower)) + "\n\n"
    dim_pages = {v[2]: v[0] for v in SEARCH.values()}
    for t in sorted(tags, key=str.lower):
        out += f"## {t} {{ #{tag_id(t)} }}\n\n"
        rows = []
        for m, p, op in sorted(tags[t], key=lambda x: (x[1], METHODS.index(x[0]))):
            path = code(p)
            if m == "post" and p in dim_pages:
                path = f"[{path}](../developers/api/{dim_pages[p]}.md)"
            elif (m, p) in HAND_PAGES:
                path = f"[{path}]({HAND_PAGES[(m, p)]})"
            rows.append([f"`{m.upper()}`", path, op.get("summary", ""), ACCESS[access.get((m, p), "none")]])
        out += table(["Method", "Path", "Summary", "Access"], rows)
    return out


def tag_id(t: str) -> str:
    return "tag-" + "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")


def search_page(dim_id: str, dim: dict, o: dict, access: dict) -> str:
    slug, title, path, src = SEARCH[dim_id]
    S = o["components"]["schemas"]
    op = o["paths"][path]["post"]
    body_name = op["requestBody"]["content"]["application/json"]["schema"]["$ref"].split("/")[-1]
    body = S[body_name]
    result_ref = op["responses"]["200"]["content"]["application/json"]["schema"]
    result_name = result_ref["$ref"].split("/")[-1]
    result = S[result_name]
    row_name = result["properties"]["items"]["items"]["$ref"].split("/")[-1]
    row = S[row_name]
    query, example_row = EXAMPLES[dim_id]
    missing = [k for k in example_row if k not in row["properties"]]
    if missing:
        sys.exit(f"gen_api: example fields {missing} are not in {row_name}")

    desc = (f"Search {dim['noun_plural']} with a query and get the matching rows with their total count. "
            f"The interface runs the same search for its {dim['label']} table, so you can pull the same rows into your own scripts.")
    out = front_matter(title, desc, [src, "shared/definitions/asset_query.py", f"shared/services/surface_query/"],
                       SCRIPT, layout="pane", endpoint=f"POST {path}")
    out += gen_line(["openapi.json", "query-schema.json"], SCRIPT)
    out += '<div class="rn-split" markdown>\n<div class="rn-prose" markdown>\n\n'

    out += "## Query parameters\n\n"
    out += "These go in the URL. They decide which project, runs and targets the search covers.\n\n"
    rows = []
    for p in op.get("parameters", []):
        sch = p.get("schema", {})
        rows.append([code(p["name"]), type_of(sch, S), "Yes" if p.get("required") else "No", sentence(p.get("description") or sch.get("description") or "")])
    out += table(["Name", "Type", "Required", "Description"], rows)
    who = {"user": "Any signed-in user can call this operation.",
           "administrator": "Only an administrator can call this operation."}.get(
        access.get(("post", path), "user"), "Access: " + ACCESS[access.get(("post", path), "user")].lower() + ".")
    out += ("`project_id` scopes the search to one project. Add `scan_id` to search one run, "
            "or `target_id`, repeated for several, to search some targets. " + who + "\n\n")

    out += (f"## Request body\n\nSend a JSON body of type `{body_name}`. Put your query in `q`. "
            "Most other fields are filters that the interface sets from its controls, and they combine with `q`.")
    out += " A field that is not listed here is refused with HTTP 422.\n\n" if body.get("additionalProperties") is False else "\n\n"
    rows = []
    for name, sch in body["properties"].items():
        d = COMMON_BODY.get(name, "A filter the interface sets from its controls. Combined with `q`." if name not in ("new",) else "Only rows that are new in the run.")
        if name == "q":
            d = f"Query in the [{dim['label'].lower()} grammar](../../reference/query/{QUERY_PAGES[dim_id]}.md). Empty or null returns every row in scope."
        if name == "sort" and dim.get("sort", {}).get("keys"):
            d = "Sort key: " + ", ".join(code(k) for k in dim["sort"]["keys"]) + "."
        rows.append([code(name), type_of(sch, S), default_of(sch), limits_of(sch), d])
    out += table(["Field", "Type", "Default", "Limits", "Description"], rows)

    out += "## Response\n\n"
    out += f"You get back a `{result_name}`.\n\n"
    rrows = []
    for name, sch in result["properties"].items():
        d = {
            "items": f"The rows, `{row_name}`.",
            "total": "Rows that match, up to the count cap.",
            "total_capped": "`true` when the count stopped at the cap. The total is then a lower bound.",
            "error": "Set when the query does not parse. The rows are then empty.",
            "page": "The page returned.",
            "size": "Rows per page.",
        }.get(name, "")
        rrows.append([code(name), type_of(sch, S), d])
    out += table(["Field", "Type", "Description"], rrows)
    out += ("If reNgine cannot parse your query, you still get HTTP 200, with `error` set to `{message, hint, start, end}`. "
            "`start` and `end` are offsets into the query, so you can show where the problem is. "
            "A body that fails validation returns HTTP 422.\n\n")

    out += f"### Row fields\n\nEach row in `items` is a `{row_name}` with {len(row['properties'])} fields.\n\n"
    out += table(["Field", "Type"], [[code(n), type_of(s, S)] for n, s in row["properties"].items()])

    related = sorted(p for p in o["paths"] if p.startswith(path + "/"))
    if related:
        out += "## Related operations\n\n"
        out += "You also find these operations under the same path.\n\n"
        out += table(["Operation", "Summary"], [[code("POST " + p), o["paths"][p]["post"]["summary"]] for p in related if "post" in o["paths"][p]])

    out += "</div>\n<div class=\"rn-pane\" markdown>\n"
    out += f'<div class="rn-pane-head"><b>Request</b><span>POST</span></div>\n\n'
    body_example = {"q": query}
    page_keys = ("limit", "size")
    for k in page_keys:
        if k in body["properties"]:
            body_example[k] = 50
            break
    out += "/// tab | curl\n"
    out += "```bash\n"
    out += "# RENGINE=https://asm.example.com; jar holds the session\n"
    out += "curl -b jar -X POST \\\n"
    out += f"  \"$RENGINE{path}?project_id=$PROJECT\" \\\n"
    out += "  -H \"Content-Type: application/json\" \\\n"
    out += f"  -d '{json.dumps(body_example)}'\n"
    out += "```\n///\n\n"
    out += "/// tab | Python\n"
    out += "```python\nimport httpx\n\n"
    out += "with httpx.Client(base_url=\"https://asm.example.com\") as client:\n"
    out += "    client.post(\"/api/v1/auth/login\",\n                json={\"username\": user, \"password\": password})\n"
    out += f"    r = client.post(\"{path}\",\n"
    out += "                    params={\"project_id\": project},\n"
    out += f"                    json={json.dumps(body_example)})\n"
    out += "    page = r.json()\n```\n///\n\n"
    out += "/// tab | MCP\n" if dim_id != "software" else ""
    if dim_id != "software":
        args = {"target": "example.com", "dimension": dim_id, "query": query}
        out += "```json\n" + json.dumps({"name": "query_assets", "arguments": args}, indent=2) + "\n```\n///\n\n"
    resp = {"items": [example_row], "total": 3, "total_capped": False, "error": None}
    if "page" in result["properties"]:
        resp = {"items": [example_row], "total": 3, "total_capped": False, "page": 1, "size": 50, "error": None}
    out += '<div class="rn-pane-label">response · 200, one row shown, fields abridged</div>\n\n'
    out += "```json\n" + json.dumps(resp, indent=2) + "\n```\n\n"
    out += "</div>\n</div>\n"
    return out


def main() -> None:
    o = load("openapi.json")
    schema = load("query-schema.json")
    access = access_map()
    dims = {d["id"]: d for d in schema["dimensions"]}
    changed = write(DOCS / "reference" / "http-api.md", index_page(o, access))
    for dim_id, (slug, *_rest) in SEARCH.items():
        changed += write(DOCS / "developers" / "api" / f"{slug}.md", search_page(dim_id, dims[dim_id], o, access))
    print(f"gen_api: {1 + len(SEARCH)} pages, {changed} changed")


if __name__ == "__main__":
    main()
