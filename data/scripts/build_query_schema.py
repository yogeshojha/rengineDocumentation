"""Build query-schema.json from the live schema definitions. Read-only: imports and prints.

Run from the host:
  docker exec -i rengine-api-1 /app/.venv/bin/python - \
      < scratchpad/scripts/build_query_schema.py > scratchpad/data/query-schema.json

Everything under "grammar" and each dimension's fields, flags, group_by and examples is read
from shared/definitions/asset_query.py at import time. The hand-entered parts are marked
"source" with the file and line they were transcribed from (row descriptions, sort keys,
per-field matching notes).
"""

import ast
import contextlib
import importlib
import io
import json
import sys

# keep import-time chatter (dnstwist, bootstrap logging) out of stdout
_real_stdout = sys.stdout
sys.stdout = sys.stderr
with contextlib.redirect_stdout(io.StringIO()):
    import shared.definitions.asset_query as aq
    from shared.definitions import (
        correlation,
        domain_posture,
        endpoints,
        evidence,
        exports,
        hygiene,
        interest,
        ports,
        relations,
        secrets,
        software,
        surface,
        threat_intel,
        tripwires,
        vulnerabilities,
    )
    from shared.services.scan_scope import covering_stages, producing_stages
    from shared.services.asset_query import parser as parser_mod
    from shared.services.asset_query import terms as terms_mod
    from shared.services.asset_query import values as values_mod
sys.stdout = _real_stdout

SRC = "shared/definitions/asset_query.py"

# ---------- source line numbers ----------

tree = ast.parse(open(aq.__file__, encoding="utf-8").read())
ASSIGN_LINE: dict[str, int] = {}
FIELD_LINE: dict[str, dict[str, int]] = {}
for node in tree.body:
    target = None
    value = None
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        target, value = node.target.id, node.value
    elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        target, value = node.targets[0].id, node.value
    if target is None:
        continue
    ASSIGN_LINE[target] = node.lineno
    if isinstance(value, ast.Tuple):
        lines: dict[str, int] = {}
        for element in value.elts:
            if not isinstance(element, ast.Call):
                continue
            for kw in element.keywords:
                if kw.arg in ("name", "key", "query") and isinstance(kw.value, ast.Constant):
                    lines.setdefault(str(kw.value.value), element.lineno)
                    break
                if kw.arg == "name" and isinstance(kw.value, ast.Name):
                    lines.setdefault(str(getattr(aq, kw.value.id, kw.value.id)), element.lineno)
                    break
        if lines:
            FIELD_LINE[target] = lines

REGISTRY_VARS = {
    "web_assets": ("FIELDS", "FLAGS", "GROUP_DIMENSIONS", "EXAMPLES", "HOST_QUERY"),
    "endpoints": ("ENDPOINT_FIELDS", "ENDPOINT_FLAGS", "ENDPOINT_GROUP_DIMENSIONS", "ENDPOINT_EXAMPLES", "ENDPOINT_QUERY"),
    "services": ("SERVICE_FIELDS", "SERVICE_FLAGS", "SERVICE_GROUP_DIMENSIONS", "SERVICE_EXAMPLES", "SERVICE_QUERY"),
    "ips": ("IP_FIELDS", "IP_FLAGS", "IP_GROUP_DIMENSIONS", "IP_EXAMPLES", "IP_QUERY"),
    "vulnerabilities": ("VULN_FIELDS", "VULN_FLAGS", "VULN_GROUP_DIMENSIONS", "VULN_EXAMPLES", "VULN_QUERY"),
    "software": ("SOFTWARE_FIELDS", "SOFTWARE_FLAGS", "SOFTWARE_GROUP_DIMENSIONS", "SOFTWARE_EXAMPLES", "SOFTWARE_QUERY"),
    "secrets": ("SECRET_FIELDS", "SECRET_FLAGS", "SECRET_GROUP_DIMENSIONS", "SECRET_EXAMPLES", "SECRET_QUERY"),
}

# ---------- hand-entered, transcribed from source ----------

ROW = {
    "web_assets": {
        "row": "One hostname recorded by one scan (a subdomains row), with the HTTP response probed on it.",
        "identity": "name",
        "source": "shared/services/surface_query/web_assets.py:96-108; shared/definitions/notes.py:46",
    },
    "endpoints": {
        "row": "One URL (host, path and parameter shape) recorded by one scan (an endpoints row).",
        "identity": "signature",
        "source": "shared/services/surface_query/endpoints.py:106-109; shared/definitions/notes.py:47",
    },
    "services": {
        "row": "One open port on one address recorded by one scan (a ports row), joined to the address, its hostnames and the HTTP response on that port.",
        "identity": "ip, number, protocol",
        "source": "shared/services/surface_query/services.py:36-115; shared/definitions/compare.py:168",
    },
    "ips": {
        "row": "One distinct IP address across the scans in scope, folded from resolved hostnames, ports, HTTP assets and ip_addresses rows. One row serves every target that shares the address.",
        "identity": "ip",
        "source": "shared/services/surface_query/ips.py:40-89",
    },
    "vulnerabilities": {
        "row": "One finding: one check that fired at one location in one scan (a vulnerabilities row, unique per scan and fingerprint).",
        "identity": "fingerprint = sha256(scanner|template_id|matcher|matched_at)",
        "source": "tools/nuclei/parser.py:120-124; shared/services/vuln_inventory.py:229",
    },
    "software": {
        "row": "One software CVE: one published CVE inferred for one software name and version on one asset in one scan (a software_cves row).",
        "identity": "fingerprint = md5(host or ip|port|vendor|product|version|cve)",
        "source": "shared/services/software_match.py:171-249",
    },
    "secrets": {
        "row": "One distinct value a detector matched in a stored response, per scan (a secrets row), with its sightings.",
        "identity": "fingerprint",
        "source": "shared/services/surface_query/secrets.py:73-75; shared/definitions/notes.py:52",
    },
}

SORT = {
    "web_assets": {
        "keys": ["name", "status", "size", "time", "title", "cert", "discovered", "ip"],
        "api_default": {"sort": "name", "order": "asc"},
        "ui_default": {"sort": "status", "order": "asc"},
        "tiebreak": "name asc, id asc; NULLs last",
        "source": "shared/services/surface_query/web_assets.py:80-93; shared/models/subdomain.py (SubdomainFilter.sort); frontend/src/lib/components/scans/results/web-assets-table.svelte:139",
    },
    "endpoints": {
        "keys": ["relevance", "path", "url", "host", "status", "length", "params", "depth", "seen", "class"],
        "api_default": {"sort": "path", "direction": "asc"},
        "ui_default": {"sort": "relevance", "direction": "desc"},
        "relevance": "matched an interest pattern, then has parameters, then probed, then 2xx, then shallower depth, then host, path",
        "tiebreak": "host asc, path asc, id asc; NULLs last",
        "source": "shared/services/surface_query/endpoints.py:72-103; frontend/src/lib/components/scans/results/endpoints-table.svelte:148",
    },
    "services": {
        "keys": ["exposure", "port", "ip", "service", "class", "product", "hosts", "asn", "country", "status"],
        "api_default": {"sort": "exposure", "order": "desc"},
        "ui_default": {"sort": "exposure", "order": "desc"},
        "exposure": "sensitive ports first, then non-HTTP before HTTP, then more hostnames, then address, port",
        "tiebreak": "address asc, port asc, id asc; NULLs last",
        "source": "shared/services/surface_query/services.py:198-222; frontend/src/lib/components/scans/results/services-table.svelte:116",
    },
    "ips": {
        "keys": ["ip", "hosts", "ports", "assets", "asn", "country"],
        "api_default": {"sort": "hosts", "order": "desc"},
        "ui_default": {"sort": "hosts", "order": "desc"},
        "tiebreak": "address asc (numeric); NULLs last",
        "source": "shared/services/surface_query/ips.py:173-183; frontend/src/lib/components/scans/results/ips-table.svelte:113",
    },
    "vulnerabilities": {
        "keys": ["risk", "severity", "name", "template", "host", "seen", "cvss", "epss", "exploit", "type"],
        "issue_view_keys": ["risk", "severity", "name", "template", "host", "seen", "cvss", "epss", "findings"],
        "api_default": {"sort": "risk", "order": "desc"},
        "ui_default": {"sort": "risk", "order": "desc"},
        "risk": "severity rank, then KEV, then exploitation rank, then corroborated, then EPSS, then CVSS, then check id, location",
        "tiebreak": "template_id asc, matched_at asc, id asc; NULLs last",
        "source": "shared/services/surface_query/vulnerabilities.py:84-115; api/app/services/vulnerability.py:366-389; frontend/src/lib/components/scans/results/vulnerabilities-table.svelte:155",
    },
    "software": {
        "keys": ["rank", "cvss", "epss", "cve", "software", "host", "seen"],
        "api_default": {"sort": None, "direction": None},
        "ui_default": {"sort": "rank", "direction": "desc"},
        "default_order": "exploitation rank desc, CVSS desc, CVE desc",
        "tiebreak": "cve, id",
        "source": "shared/services/surface_query/software.py:23-59; frontend/src/lib/components/scans/results/software-table.svelte:99",
    },
    "secrets": {
        "keys": ["state", "kind", "hosts", "sightings", "seen"],
        "api_default": {"sort": None, "direction": None},
        "ui_default": {"sort": "state", "direction": "desc"},
        "default_order": "state rank (exposed, expired, public) desc, hosts desc, discovered desc",
        "source": "shared/services/surface_query/secrets.py:24-70; frontend/src/lib/components/scans/results/secrets-table.svelte:87",
    },
}

UI_COLUMNS = {
    "web_assets": {
        "lead": ["Host", "Status", "Title"],
        "optional": ["Tech", "IP / Network", "Ports", "Sources", "Hygiene", "First seen", "Size", "Time", "Screenshot"],
        "default_visible": ["Tech", "IP / Network", "Ports", "Screenshot"],
        "source": "frontend/src/lib/components/scans/results/web-assets/columns.ts:3-26",
    },
    "endpoints": {
        "lead": ["Status", "Path"],
        "optional": ["Host", "Kind", "Parameters", "Title", "Technology", "Size", "Found by", "First seen"],
        "default_visible": ["Host", "Kind", "Parameters", "Size", "Found by"],
        "source": "frontend/src/lib/components/scans/results/endpoints/columns.ts:3-27",
    },
    "services": {
        "lead": ["Service", "Software"],
        "optional": ["Web assets", "Web", "Network", "Country", "Evidence"],
        "default_visible": ["Web assets", "Web", "Country"],
        "source": "frontend/src/lib/components/scans/results/services/columns.ts:3-26",
    },
    "ips": {
        "lead": ["Address", "Network"],
        "optional": ["Web assets", "Ports", "Country", "Prefix", "PTR", "Web"],
        "default_visible": ["Web assets", "Ports", "Country"],
        "source": "frontend/src/lib/components/scans/results/ips/columns.ts:3-27",
    },
    "vulnerabilities": {
        "lead": ["Finding", "Location"],
        "issue_view_lead": ["Weakness"],
        "issue_view_columns": ["Affected", "Risk", "Review", "First seen"],
        "source": "frontend/src/lib/components/scans/results/vulnerabilities/columns.ts:3-32",
    },
    "software": {
        "lead": ["CVE", "Software"],
        "optional": ["Asset", "Severity", "Exploitation", "Evidence", "Confidence", "Seen"],
        "default_visible": ["Asset", "Severity", "Exploitation", "Evidence", "Confidence"],
        "source": "frontend/src/lib/components/scans/results/software/columns.ts:3-33",
    },
    "secrets": {
        "lead": ["Secret"],
        "columns": ["Target (project view)", "Kind", "State", "Web asset", "Seen"],
        "source": "frontend/src/lib/components/scans/results/secrets/columns.ts:21-32",
    },
}

UI_HINT = {
    "web_assets": "status:>=500 not is:cdn",
    "endpoints": "is:param and is:live",
    "services": "class:database not is:cdn",
    "ips": "is:sensitive not cdn:yes",
    "vulnerabilities": "severity:critical and not is:cdn",
    "software": "severity:critical and is:stated",
    "secrets": "group:cloud and is:exposed",
}

# how ':' and the other operators behave for a field, by how its builder compiles it
MATCH = {
    "string": "':' case-insensitive substring; '=' case-insensitive exact; '!=' not equal (rows with no value match); '~' / '!~' case-insensitive PostgreSQL regular expression",
    "folded": "stored lowercase: ':' substring; '=' exact; '!=' not equal; '~' / '!~' regular expression",
    "list": "list-valued: ':' substring of any element; '=' exact element (case-sensitive); '!=' no element contains the value; '~' / '!~' regular expression on any element",
    "number": "':' and '=' equal; accepts a list and an inclusive a..b range; '>' '>=' '<' '<=' compare; '!=' also matches rows with no value",
    "date": "calendar date or relative age; see grammar.dates",
    "ip": "CIDR is containment; a full IPv4 or '=' is exact; anything else is a substring; '!=' negates",
    "exact": "value compared exactly (lowercased); ':' and '=' behave the same; '!=' negates",
    "flag": "one or more flag names; a list is any-of; unknown names are an error",
}

NOTES = {
    "web_assets": {
        "target": ("string", "Matches the target's value. source: compiler.py:301, terms.py:88-90"),
        "host": ("folded", "source: compiler.py:302, terms.py:76-85"),
        "url": ("string", "Matches the final URL after redirects, else the probed URL. As free text only the final URL is searched. source: compiler.py:213-214,303,379"),
        "path": ("string", "Read from the host's HTTP asset. source: compiler.py:359"),
        "cname": ("string", "source: compiler.py:304"),
        "source": ("list", "Values are not validated. source: compiler.py:305"),
        "discovered": ("date", "Past-facing. source: compiler.py:306-308"),
        "status": ("number", "Also accepts 1xx-5xx classes and none (no HTTP response); '!=' also matches rows with no status. source: compiler.py:138-168, values.py:21,64-69"),
        "title": ("string", "source: compiler.py:310"),
        "server": ("string", "source: compiler.py:311"),
        "tech": ("list", "source: compiler.py:312"),
        "content_type": ("string", "source: compiler.py:313"),
        "size": ("number", "Units b, k/kb, m/mb, gb (1024-based). source: compiler.py:314-316, values.py:14"),
        "words": ("number", "Read from the host's HTTP asset. source: compiler.py:360"),
        "paths": ("number", "Count of endpoint rows on the host in scope. source: compiler.py:217-224,320"),
        "lines": ("number", "Read from the host's HTTP asset. source: compiler.py:361"),
        "time": ("number", "Units ms, s, m, h. Stored in seconds. source: compiler.py:317-319, values.py:15"),
        "redirect": ("string", "Location header on the host's HTTP asset. source: compiler.py:362"),
        "favicon": ("string", "As free text the hash must equal the word exactly. source: compiler.py:321,380"),
        "screenshot": ("exact", "16 hex digits (optional 0x). Matches every render within 2 bits of the hash. Only the first value is read. source: compiler.py:322-324, values.py:84-88, predicates.py:306-311, shared/definitions/correlation.py:13"),
        "body": ("text", "Full-text over the stored body: a single unquoted word is a prefix match, several words are a phrase, a quoted value is matched as whole words. source: compiler.py:108-119,365, values.py:135-140"),
        "header": ("text", "header:word is full-text over the headers; a quoted value is a substring of the raw header block; header.<name>:<value> is a substring of that one header (name lowercased, '-' read as '_'). source: compiler.py:122-130,366"),
        "ip": ("ip", "source: compiler.py:81-105"),
        "asn": ("number", "Accepts 13335 or AS13335. Maximum 4294967295. source: compiler.py:326-328, values.py:22,72-81"),
        "org": ("string", "source: compiler.py:329"),
        "cdn": ("string", "yes/true/1/any/present and no/false/0/none/absent filter on presence; anything else matches the CDN name. source: compiler.py:330, terms.py:39-40,197-224"),
        "waf": ("string", "yes/no words filter on presence; anything else matches the WAF name. source: compiler.py:198-202"),
        "port": ("number", "True when a resolved address has that port open in the row's scan. source: compiler.py:332-334, predicates.py:124-137"),
        "service": ("string", "Declared enum (':' '=' '!=' only) and compiled as a string match on the port's service name. source: compiler.py:335-337"),
        "hygiene": ("exact", "Validated: an unknown value is an error. warning / info expand to every check of that tone, any = fails at least one, none = checked and failing none. source: compiler.py:246-253, predicates.py:768-785"),
        "posture": ("exact", "Validated like hygiene, over the checks of the host's zone. source: compiler.py:256-263, predicates.py:806-823"),
        "ai": ("exact", "A service key, a category (self_hosted, gateway, mcp, application, cloud, generic), or a yes/no word. source: compiler.py:266-286"),
        "ai.model": ("list", "yes/no words filter on presence. source: compiler.py:289-297"),
        "cert": ("exact", "expired: flagged expired or not-after in the past. expiring: not expired and not-after within 30 days. self-signed. valid: not-after 30 days or more away and not self-signed. source: predicates.py:100-121, shared/definitions/dashboard.py:38"),
        "cert.cn": ("string", "source: compiler.py:367"),
        "cert.san": ("list", "source: compiler.py:368"),
        "cert.issuer": ("string", "Searches issuer, issuer organisation and issuer common name. source: compiler.py:205-210"),
        "cert.expires": ("date", "Future-facing: cert.expires:<30d is not-after earlier than 30 days from now (already expired certificates included). source: compiler.py:339-341, terms.py:121-136"),
        "tls.version": ("string", "source: compiler.py:370"),
        "content_hash": ("string", "source: compiler.py:363"),
        "tracking": ("list", "source: compiler.py:364"),
        "jarm": ("string", "source: compiler.py:371"),
        "cert.fingerprint": ("string", "source: compiler.py:372"),
        "header_hash": ("string", "source: compiler.py:373"),
        "is": ("flag", "is:interesting is accepted as an unlisted alias of is:exposed. source: compiler.py:171-195, walk.py:27-41"),
        "vuln": ("string", "Severity of any finding in scope whose host is this hostname; compiled as a substring match. source: compiler.py:342-344"),
        "cve": ("list", "CVE ids on any finding on this hostname. source: compiler.py:351-353"),
        "exposure": ("exact", "source: compiler.py:227-231"),
        "flagged": ("exact", "source: compiler.py:234-238"),
        "exposure_band": ("exact", "source: compiler.py:241-243"),
    },
    "endpoints": {
        "dir": ("string", "dir: matches the directory and everything below it; dir= only that directory. A leading and trailing '/' are added. source: endpoint_compiler.py:85-97"),
        "status": ("number", "Also accepts 2xx, 3xx, 4xx, 5xx and none. source: endpoint_compiler.py:100-114"),
        "length": ("number", "Units b, k/kb, m/mb, gb. source: endpoint_compiler.py:147-149"),
        "class": ("string", "Declared enum; compiled as a substring match. source: endpoint_compiler.py:140"),
        "scheme": ("string", "Declared enum; compiled as a substring match. source: endpoint_compiler.py:138"),
        "param": ("list", "source: endpoint_compiler.py:141"),
        "interest": ("list", "source: endpoint_compiler.py:143"),
        "tech": ("list", "source: endpoint_compiler.py:151"),
        "method": ("list", "source: endpoint_compiler.py:152"),
        "source": ("list", "source: endpoint_compiler.py:153"),
        "seen": ("date", "Past-facing. source: endpoint_compiler.py:155"),
        "vuln": ("string", "A finding in scope on the endpoint's HTTP asset or on its host. source: endpoint_compiler.py:117-119, predicates.py:683-696"),
        "cve": ("list", "source: endpoint_compiler.py:122-126"),
        "is": ("flag", "source: endpoint_compiler.py:53-82"),
    },
    "services": {
        "ip": ("ip", "source: service_compiler.py:128, terms.py:206-217"),
        "asn": ("number", "Accepts AS13335. source: service_compiler.py:129-131"),
        "cdn": ("string", "yes/no words filter on presence. source: service_compiler.py:134"),
        "host": ("folded", "True when a hostname in scope resolving to the address matches. source: service_compiler.py:51-58,135"),
        "banner": ("string", "Declared text (':' '=' '!=' only); compiled as a substring match. source: service_compiler.py:127"),
        "class": ("string", "Declared enum; compiled as a substring match. source: service_compiler.py:122"),
        "protocol": ("string", "Declared enum; compiled as a substring match. source: service_compiler.py:123"),
        "source": ("string", "Declared enum; compiled as a substring match. source: service_compiler.py:124"),
        "country": ("string", "Declared enum; compiled as a substring match. source: service_compiler.py:133"),
        "status": ("number", "HTTP status on this port. No status classes here. source: service_compiler.py:136"),
        "seen": ("date", "Past-facing. source: service_compiler.py:118-120"),
        "ai": ("exact", "source: service_compiler.py:61-81"),
        "ai.model": ("list", "source: service_compiler.py:84-91"),
        "vuln": ("string", "A finding in scope on the same address and port. source: service_compiler.py:137-142"),
        "cve": ("list", "source: service_compiler.py:143-148"),
        "is": ("flag", "source: service_compiler.py:94-113"),
    },
    "ips": {
        "target": ("string", "True when any target the address serves matches. source: ip_compiler.py:87, terms.py:93-102"),
        "ip": ("ip", "source: ip_compiler.py:88"),
        "ptr": ("list", "source: ip_compiler.py:89"),
        "seen": ("date", "Past-facing. source: ip_compiler.py:90-92"),
        "asn": ("number", "Accepts AS13335. source: ip_compiler.py:93-95"),
        "cdn": ("string", "yes/no words filter on presence. source: ip_compiler.py:99"),
        "port": ("number", "source: ip_compiler.py:100-102"),
        "service": ("string", "Declared enum; compiled as a substring match on a port's service name. source: ip_compiler.py:103"),
        "country": ("string", "Declared enum; compiled as a substring match. source: ip_compiler.py:97"),
        "host": ("folded", "source: ip_compiler.py:105"),
        "vuln": ("string", "A finding in scope on the address. source: ip_compiler.py:108-110"),
        "cve": ("list", "source: ip_compiler.py:111-113"),
        "is": ("flag", "source: ip_compiler.py:68-84"),
    },
    "vulnerabilities": {
        "severity": ("string", "Declared enum; compiled as a substring match. source: vuln_compiler.py:128"),
        "type": ("string", "Declared enum; compiled as a substring match. source: vuln_compiler.py:129"),
        "scanner": ("string", "Declared enum; compiled as a substring match. source: vuln_compiler.py:130"),
        "tag": ("list", "source: vuln_compiler.py:131"),
        "author": ("list", "source: vuln_compiler.py:136"),
        "cve": ("list", "source: vuln_compiler.py:137"),
        "cwe": ("list", "source: vuln_compiler.py:138"),
        "signal": ("list", "source: vuln_compiler.py:145"),
        "extracted": ("string", "Matches the extracted values as text. source: vuln_compiler.py:133-135"),
        "cvss": ("number", "Decimal. source: vuln_compiler.py:139"),
        "epss": ("number", "Decimal 0 to 1. source: vuln_compiler.py:140"),
        "ip": ("ip", "source: vuln_compiler.py:148-150"),
        "status": ("number", "HTTP status of the asset the finding sits on. source: vuln_compiler.py:152-157"),
        "tech": ("list", "Technology on the finding's HTTP asset or host. source: vuln_compiler.py:56-62,158"),
        "asn": ("number", "source: vuln_compiler.py:159-161"),
        "country": ("string", "source: vuln_compiler.py:162"),
        "state": ("exact", "'-' and spaces are read as '_'. Defaults to open when nobody has decided. source: vuln_compiler.py:105-109, predicates.py:629-642"),
        "ticket": ("exact", "'-' and spaces are read as '_'. Matches findings held by a filed tracker issue in that category. source: vuln_compiler.py:112-115, predicates.py:609-626"),
        "evidence": ("exact", "proven, corroborated (and not proven), observed (and not corroborated). source: vuln_compiler.py:118-121, predicates.py:595-606"),
        "seen": ("date", "Past-facing. source: vuln_compiler.py:166-168"),
        "is": ("flag", "source: vuln_compiler.py:72-102"),
    },
    "software": {
        "source": ("string", "Declared enum; compiled as a substring match. source: software_compiler.py:87"),
        "severity": ("string", "Declared enum; compiled as a substring match. source: software_compiler.py:88"),
        "confidence": ("string", "Declared enum; compiled as a substring match. source: software_compiler.py:92"),
        "evidence": ("string", "Declared enum; compiled as a substring match. source: software_compiler.py:93"),
        "caveat": ("exact", "source: software_compiler.py:40-46"),
        "cvss": ("number", "Decimal. source: software_compiler.py:89"),
        "epss": ("number", "Decimal. source: software_compiler.py:90"),
        "ip": ("ip", "source: software_compiler.py:96-98"),
        "seen": ("date", "Past-facing. source: software_compiler.py:100-102"),
        "is": ("flag", "source: software_compiler.py:56-77"),
    },
    "secrets": {
        "secret": ("string", "Declared enum; compiled as a substring match on the detector key. source: secret_compiler.py:34"),
        "group": ("string", "Declared enum; compiled as a substring match. source: secret_compiler.py:36"),
        "state": ("string", "Declared enum; compiled as a substring match. source: secret_compiler.py:39"),
        "source": ("string", "Declared enum; compiled as a substring match. source: secret_compiler.py:40"),
        "seen": ("date", "Past-facing. source: secret_compiler.py:43"),
        "is": ("flag", "source: secret_compiler.py:22-29"),
    },
}

TYPE_DEFAULT_MATCH = {
    "string": "string",
    "enum": "string",
    "number": "number",
    "bytes": "number",
    "duration": "number",
    "date": "date",
    "ip": "ip",
    "text": "string",
    "flag": "flag",
}

FLAG_RULES = {
    "web_assets": {
        "live": "HTTP status from 200 to 399",
        "web": "an HTTP status was recorded",
        "new": "an earlier scan of the same target recorded at least one hostname, and none of them recorded this hostname",
        "resolved": "resolved_ips holds at least one address",
        "auth": "HTTP status 401 or 403, or the page title matches login|sign ?in|log ?in|admin|dashboard|portal|console|authenticat",
        "cdn": "is_cdn is true",
        "cloud": "an HTTP asset on the hostname has cdn_type 'cloud'",
        "waf": "a WAF name is recorded",
        "screenshot": "a screenshot path is recorded",
        "important": "is_important is true",
        "wildcard": "is_wildcard is true",
        "issue": "certificate expired, expiring within 30 days or self-signed; or status 500 or above; or live with no WAF and no CDN; or a sensitive port open",
        "sensitive": "a resolved address has a port from SENSITIVE_PORTS open in the row's scan",
        "http2": "an HTTP asset on the hostname supports HTTP/2",
        "redirect": "final_url is set and differs from the probed URL",
        "vulnerable": "a finding in scope has this hostname as its host",
        "kev": "a finding in scope on this hostname is KEV-listed",
        "exposed": "interest_score above 0",
    },
    "endpoints": {
        "new": "an earlier scan of the target recorded at least one endpoint, and none recorded this signature",
        "param": "param_count above 0",
        "probed": "is_probed is true",
        "live": "status from 200 to 399",
        "redirect": "status from 300 to 399",
        "auth": "status 401 or 403",
        "missing": "status 404 or 410",
        "api": "class is api",
        "js": "class is script",
        "static": "class is style, image or media",
        "interesting": "at least one interest pattern matched",
        "sensitive": "interest includes vcs, secrets or backup",
        "orphan": "no source among crawl, response_mining, sitemap, js, and no found_on URL",
        "archive-only": "source includes archive or deep_archive, no linked source, and not probed or no status or status 400 and above",
        "linked": "source includes crawl, response_mining, sitemap or js",
        "crawled": "source includes crawl",
        "root": "path is '/' with no parameters",
        "titled": "title is set and not empty",
        "vulnerable": "a finding in scope sits on the endpoint's HTTP asset or host",
        "kev": "such a finding is KEV-listed",
    },
    "services": {
        "new": "an earlier scan of the target recorded at least one port, and none recorded this address and port",
        "http": "is_http is true",
        "tls": "tls is true",
        "sensitive": "port number is in SENSITIVE_PORTS",
        "named": "a product is recorded",
        "passive": "source is internetdb",
        "confirmed": "source is anything but internetdb",
        "cdn": "the address is CDN-fronted",
        "hosted": "at least one hostname in scope resolves to the address",
        "private": "address inside 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16, 100.64/10, ::1, fc00::/7 or fe80::/10",
        "v4": "IPv4",
        "v6": "IPv6",
        "vulnerable": "a finding in scope has the same address and port",
        "kev": "such a finding is KEV-listed",
    },
    "ips": {
        "new": "single scan: an earlier scan of the target recorded at least one address and none recorded this one; project scope: earlier rows exist for a target the address serves and none of them hold this address",
        "alive": "is_alive is true (falls back to: has a port or an HTTP asset)",
        "open": "port_count above 0",
        "sensitive": "a port from SENSITIVE_PORTS is open",
        "hosted": "host_count above 0",
        "web": "asset_count above 0",
        "cdn": "is_cdn is true",
        "ptr": "at least one PTR hostname",
        "private": "address inside a private or reserved range (same list as services)",
        "v4": "IPv4",
        "v6": "IPv6",
        "vulnerable": "a finding in scope has this address",
        "kev": "such a finding is KEV-listed",
    },
    "vulnerabilities": {
        "new": "an earlier scan of the target recorded at least one finding, and none had this fingerprint",
        "kev": "is_kev is true",
        "ransomware": "kev_ransomware is true",
        "overdue": "kev_due_date is before today",
        "weaponised": "poc_count above 0",
        "untestable": "template_available is false",
        "cve": "at least one CVE id",
        "exploitable": "KEV-listed, or EPSS at or above 0.5",
        "corroborated": "another check at the same matched_at names the same CVE or CWE, or a software CVE on the same host names one of its CVEs; informational and suppressed findings do not vouch",
        "proven": "evidence is proven (an out-of-band interaction was recorded)",
        "recorded": "request and response are both stored",
        "extracted": "extracted_results is not empty",
        "web": "bound to an HTTP asset",
        "cdn": "its HTTP asset is CDN-fronted",
        "triaged": "review state is not open",
        "open": "review state is open",
        "suppressed": "review state is false_positive or accepted",
        "ticketed": "held by a tracker issue in a ticketed state",
    },
    "software": {
        "new": "an earlier scan of the target recorded at least one software CVE, and none had this fingerprint",
        "kev": "is_kev is true",
        "ransomware": "kev_ransomware is true",
        "overdue": "kev_due_date is before today",
        "likely": "EPSS at or above 0.088",
        "firm": "confidence is high",
        "conditional": "caveats include conditional",
        "backport": "caveats include backport",
        "fingerprinted": "version_source is fingerprint",
        "stated": "version_source is banner",
        "web": "bound to an HTTP asset",
        "service": "bound to a port",
        "corroborated": "evidence is corroborated",
        "fixable": "fixed_in is set",
    },
    "secrets": {
        "new": "an earlier scan of the target recorded at least one secret, and none had this fingerprint",
        "exposed": "state is exposed",
        "public": "state is public",
        "expired": "state is expired",
        "secret": "is_secret is true",
        "shared": "read on more than one web asset (hosts above 1)",
    },
}

# ---------- assemble ----------

produce = producing_stages()
cover = covering_stages()

grammar = {
    "source": {
        "registry": SRC,
        "parser": "shared/services/asset_query/parser.py",
        "values": "shared/services/asset_query/values.py",
        "terms": "shared/services/asset_query/terms.py",
    },
    "operators": [
        {"symbol": symbol, "description": description} for symbol, description in aq.OP_HELP.items()
    ],
    "operators_by_type": {t.value: [op.value for op in ops] for t, ops in aq.OPS_BY_TYPE.items()},
    "operator_scan_order": list(parser_mod._OPS),
    "connectors": [
        {"symbol": symbol, "description": description} for symbol, description in aq.CONNECTORS.items()
    ],
    "connector_words": dict(parser_mod._CONNECTORS),
    "precedence": ["not / - / !", "and (explicit, or two terms side by side)", "or"],
    "negation": [
        "not <term>",
        "-<term> (no space, at least one character after it)",
        "!<term> (no space; != and !~ are operators, not negation)",
    ],
    "grouping": "( ) around any expression",
    "quoting": 'A value in double quotes is one literal. Inside quotes, backslash escapes the next character (\\" for a quote). Whitespace, ( and ) end an unquoted token.',
    "lists": "field:[a,b,c] matches any listed value; items may be quoted; an empty list is an error",
    "ranges": "a..b inclusive, on number, bytes and duration fields with ':' '=' or '!='",
    "wildcards": "None. *, % and _ are literal characters.",
    "regex": {
        "operators": ["~", "!~"],
        "fields": "string-type fields only",
        "dialect": "PostgreSQL regular expression, case-insensitive (~*); checked with Python re.compile before it runs",
        "max_length": parser_mod._MAX_REGEX,
        "quote_when": "the pattern contains whitespace, ( or )",
    },
    "status_classes": {"pattern": values_mod._STATUS_CLASS_RE.pattern, "values": list(aq.STATUS_CLASSES)},
    "units": {
        "bytes": dict(values_mod._BYTES),
        "duration_seconds": dict(values_mod._SECONDS),
    },
    "dates": {
        "relative_units_seconds": dict(values_mod._RELATIVE),
        "relative_pattern": values_mod._RELATIVE_RE.pattern,
        "absolute_formats": [*values_mod._DATE_FORMATS, "ISO 8601 (datetime.fromisoformat)"],
        "words": ["now", "today"],
        "words_meaning": "both resolve to the current instant",
        "timezone": "UTC when the value carries none",
        "past_fields": "relative age counts back from now: field:<7d and field:7d are within the last 7 days, field:>30d is older than 30 days",
        "future_fields": "cert.expires counts forward from now: cert.expires:<30d is before now + 30 days",
        "absolute": "field:2026-01-15 is that day (24 hours from the given instant); > >= < <= compare with the instant",
        "lists_and_ranges": "not read: only the first value is used",
    },
    "presence_words": {"true": sorted(terms_mod._TRUTHY), "false": sorted(terms_mod._FALSY)},
    "free_text": {
        "meaning": "A bare word or quoted phrase is matched with ':' against every free-text field of the dimension and the branches are ORed.",
        "unknown_field": "name:value where name is not a field is read as one free-text word; the query bar warns '\"name\" is not a field, searched as text'.",
        "max_terms": aq.MAX_FREE_TERMS,
    },
    "case": {
        "field_names": "case-insensitive",
        "connectors": "case-insensitive",
        "values": "case-insensitive, except '=' on list-valued fields (exact element)",
        "flags": "case-insensitive",
    },
    "limits": {
        "max_query_length": aq.MAX_QUERY_LENGTH,
        "max_query_nodes": aq.MAX_QUERY_NODES,
        "max_free_terms": aq.MAX_FREE_TERMS,
        "max_regex_length": parser_mod._MAX_REGEX,
        "max_number": aq.MAX_NUMBER,
        "count_cap": aq.COUNT_CAP,
        "max_groups": aq.MAX_GROUPS,
        "statement_timeout": "20s",
        "count_request_max_queries": 32,
    },
    "errors": {
        "shape": {"message": "str", "hint": "str | null", "start": "int, 0-based offset", "end": "int, exclusive"},
        "transport": "HTTP 200 with an error object on the page; rows are empty",
        "parser_messages": [
            "The query is too long.",
            "The query has too many parts.",
            "Too many free-text words. / Use at most 8, or narrow with a field.",
            "Unknown field '<name>'. / Press ? for the full field list.",
            "<field> does not support <op>. / Accepts: <ops>",
            "This filter needs a value. / Quote the value if it contains a space or a bracket.",
            "This list is empty. / Name at least one value.",
            "Unclosed quote. / Close it with a quote.",
            "Unclosed list. / Close it with ].",
            "Unclosed group. / Close it with ).",
            "Unexpected '<token>'.",
            "The query ends early.",
            "'<token>' has no operand.",
            "The regular expression is too long.",
            "'<value>' is not a valid regular expression. / <re.error text>",
            "Unknown flag '<name>'. / Try one of: <flags>",
            "Unknown hygiene check '<name>'. / Try one of: <values>",
            "Unknown posture check '<name>'. / Try one of: <values>",
            "'<value>' is not a valid number.",
            "'<value>' is not a number.",
            "'<value>' is not a valid date.",
            "'<value>' is not a valid AS number.",
            "'<value>' is not a valid rendered page hash.",
            "'<value>' is out of range.",
            "Field '<name>' cannot be searched.",
        ],
        "database_messages": {
            "2201B": ["Invalid regular expression.", "PostgreSQL regular expression syntax applies."],
            "2201G": ["Invalid regular expression.", None],
            "57014": ["The search timed out.", "Add a field filter."],
            "22003": ["A number is out of range.", None],
            "22P02": ["A value has the wrong type.", None],
            "54000": ["A search term is too long to index.", None],
        },
        "client_messages": [
            "Unmatched )",
            "Unclosed quote",
            "Unclosed list",
            "Unclosed group",
            '"<name>" is not a field, searched as text (warning)',
        ],
    },
    "match_semantics": MATCH,
}

dimensions = []
for dim, registry in aq.REGISTRIES.items():
    fields_var, flags_var, groups_var, examples_var, registry_var = REGISTRY_VARS[dim]
    notes = NOTES.get(dim, {})
    fields = []
    for spec in registry.fields:
        kind, note = notes.get(spec.name, (TYPE_DEFAULT_MATCH[spec.type.value], ""))
        fields.append(
            {
                "name": spec.name,
                "aliases": list(spec.aliases),
                "type": spec.type.value,
                "group": spec.group,
                "operators": [op.value for op in aq.OPS_BY_TYPE[spec.type]],
                "values": list(spec.values),
                "description": spec.description,
                "example": spec.example,
                "free_text": spec.free_text,
                "facet": spec.facet,
                "unit": spec.unit,
                "sub_field": spec.dynamic_sub,
                "match": MATCH.get(kind, kind),
                "note": note,
                "source": f"{SRC}:{FIELD_LINE.get(fields_var, {}).get(spec.name, ASSIGN_LINE.get(fields_var, 0))}",
            }
        )
    dimensions.append(
        {
            "id": dim,
            "registry_key": registry.key,
            "label": surface.SURFACE_LABELS[dim],
            "noun": registry.noun,
            "noun_plural": registry.noun_plural,
            "row": ROW[dim]["row"],
            "identity": ROW[dim]["identity"],
            "row_source": ROW[dim]["source"],
            "producing_stages": sorted(produce[dim]),
            "covering_stages": sorted(cover[dim]),
            "count_columns": list(surface.SURFACE_COUNT_COLUMNS.get(dim, ())),
            "export_columns": [c for c in surface.SURFACE_COLUMNS[dim] if c not in importlib.import_module("shared.services.asset_export.columns").UNAVAILABLE.get(dim, ())],
            "export_text_value": list(surface.SURFACE_TEXT_VALUE[dim]),
            "ui_columns": UI_COLUMNS[dim],
            "ui_placeholder_hint": UI_HINT[dim],
            "field_groups": list(registry.groups),
            "free_text_fields": [f.name for f in registry.fields if f.free_text],
            "fields": fields,
            "flags": [
                {"name": name, "description": description, "rule": FLAG_RULES.get(dim, {}).get(name, "")}
                for name, description in registry.flags.items()
            ],
            "flags_source": f"{SRC}:{ASSIGN_LINE.get(flags_var, 0)}",
            "group_by": [
                {
                    "key": d.key,
                    "label": d.label,
                    "description": d.description,
                    "source": f"{SRC}:{FIELD_LINE.get(groups_var, {}).get(d.key, ASSIGN_LINE.get(groups_var, 0))}",
                }
                for d in registry.dimensions
            ],
            "sort": SORT[dim],
            "example_groups": list(registry.example_groups),
            "examples": [
                {
                    "query": e.query,
                    "description": e.description,
                    "group": e.group,
                    "generic": e.generic,
                    "source": f"{SRC}:{FIELD_LINE.get(examples_var, {}).get(e.query, ASSIGN_LINE.get(examples_var, 0))}",
                }
                for e in registry.examples
            ],
            "registry_source": f"{SRC}:{ASSIGN_LINE.get(registry_var, 0)}",
        }
    )

vocabulary = {
    "severity": {"order": list(vulnerabilities.SEVERITY_ORDER), "labels": vulnerabilities.SEVERITY_LABELS, "help": vulnerabilities.SEVERITY_HELP},
    "review_states": {"order": list(vulnerabilities.VULN_STATES), "labels": vulnerabilities.VULN_STATE_LABELS, "help": vulnerabilities.VULN_STATE_HELP, "suppressed": list(vulnerabilities.SUPPRESSED_STATES)},
    "evidence": {"order": list(evidence.EVIDENCE_ORDER), "labels": evidence.EVIDENCE_LABELS, "help": evidence.EVIDENCE_HELP},
    "exploit_signals": [
        {"kind": s.kind, "label": s.label, "help": s.help, "weight": s.weight, "tone": s.tone}
        for s in threat_intel.SIGNALS
    ],
    "exploit_bands": [
        {"key": b.key, "label": b.label, "floor": b.floor, "description": b.description}
        for b in threat_intel.EXPLOIT_BANDS
    ],
    "feeds": [
        {"kind": f.kind, "label": f.label, "tagline": f.tagline, "description": f.description, "source": f.source, "url": f.url}
        for f in threat_intel.FEEDS
    ],
    "exposure_kinds": [
        {"key": k.key, "label": k.label, "help": k.help, "weight": k.weight, "tone": k.tone}
        for k in interest.KINDS
    ],
    "exposure_sources": {"labels": interest.SOURCE_LABELS, "help": interest.SOURCE_HELP},
    "exposure_bands": {"order": list(interest.BAND_ORDER), "labels": interest.BAND_LABELS, "floor": interest.BAND_FLOOR},
    "hygiene_checks": [
        {"key": c.key, "label": c.label, "help": c.help, "applies": c.applies, "fix": c.fix, "header": c.header, "group": c.group, "tone": c.tone}
        for c in hygiene.CHECKS
    ],
    "posture_checks": [
        {"key": c.key, "label": c.label, "help": c.help, "applies": c.applies, "fix": c.fix, "record": c.record, "group": c.group, "tone": c.tone}
        for c in domain_posture.CHECKS
    ],
    "correlation_kinds": [
        {"kind": k, "label": correlation.CORRELATION_KIND_LABELS[k], "help": correlation.CORRELATION_KIND_HELP[k], "default": k in correlation.CORRELATION_DEFAULT_KINDS}
        for k in correlation.CORRELATION_KIND_ORDER
    ],
    "target_relations": [
        {"kind": k, "label": relations.RELATION_LABELS[k], "help": relations.RELATION_HELP[k]}
        for k in relations.RELATION_ORDER
    ],
    "endpoint_sources": {"labels": endpoints.SOURCE_LABELS, "help": endpoints.SOURCE_HELP, "kind": endpoints.SOURCE_KIND},
    "endpoint_classes": endpoints.CLASS_LABELS,
    "endpoint_interest": endpoints.INTEREST_LABELS,
    "service_classes": ports.SERVICE_CLASS_LABELS,
    "port_sources": ports.PORT_SOURCE_LABELS,
    "sensitive_ports": list(ports.SENSITIVE_PORTS),
    "secret_detectors": [
        {"key": d.key, "label": d.label, "vendor": d.vendor, "group": d.group, "public": d.public}
        for d in secrets.DETECTORS
    ],
    "secret_groups": secrets.GROUP_LABELS,
    "secret_states": secrets.STATE_LABELS,
    "secret_sources": secrets.SOURCE_LABELS,
    "software_confidence": {"labels": software.CONFIDENCE_LABELS, "help": software.CONFIDENCE_HELP},
    "software_caveats": {"labels": software.CAVEAT_LABELS, "help": software.CAVEAT_HELP},
    "software_products": [
        {"key": p.key, "product": p.product, "vendor": p.vendor} for p in software.PRODUCTS
    ],
    "tripwire_templates": [
        {"key": t.key, "name": t.name, "dimension": t.dimension, "query": t.query, "fire_on": t.fire_on, "trigger": t.trigger}
        for t in tripwires.TEMPLATES
    ],
    "export": {
        "formats": list(exports.EXPORT_FORMATS),
        "max_rows": exports.MAX_EXPORT_ROWS,
        "retention_days": exports.RETENTION_DAYS,
        "max_running_per_project": exports.MAX_RUNNING_PER_PROJECT,
        "dimensions": list(surface.EXPORTABLE_DIMENSIONS),
    },
}

json.dump(
    {
        "generated_from": "rengine release/3.0.0 working tree, shared/definitions/asset_query.py imported in rengine-api-1",
        "grammar": grammar,
        "dimensions": dimensions,
        "vocabulary": vocabulary,
    },
    sys.stdout,
    indent=2,
    ensure_ascii=False,
    default=str,
)
sys.stdout.write("\n")
