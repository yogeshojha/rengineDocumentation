"""Write docs/reference/query/*.md from data/query-schema.json, with data/openapi.json and data/mcp-dimensions.json."""

from __future__ import annotations

import re

from gen_common import (DOCS, code, front_matter, gen_line, join_words, load, no_semicolons, sentence,
                        source_files, strip_source, table, write)

SCRIPT = "scripts/gen_query.py"
DATA = "query-schema.json"
OUT = DOCS / "reference" / "query"
PAGES = {
    "web_assets": "web-assets",
    "endpoints": "endpoints",
    "services": "services",
    "ips": "ips",
    "vulnerabilities": "vulnerabilities",
    "software": "software",
    "secrets": "secrets",
}
API = {
    "web_assets": "/api/v1/subdomains/search",
    "endpoints": "/api/v1/endpoints/search",
    "services": "/api/v1/ports/search",
    "ips": "/api/v1/ips/search",
    "vulnerabilities": "/api/v1/vulnerabilities/search",
    "software": "/api/v1/software/search",
    "secrets": "/api/v1/secrets/search",
}

NOTE_REWRITES = [
    (r"Declared enum; compiled as a substring match on (?:a port's|the) (.+?)\.", r"Values are matched as substrings of the \1."),
    (r"Declared enum; compiled as a substring match\.", "Values are matched as substrings."),
    (r"Declared enum \(':' '=' '!=' only\) and compiled as a string match on the port's service name\.", "Matched against the service name of the port. Operators `:`, `=` and `!=`."),
    (r"Declared text \(':' '=' '!=' only\); compiled as a substring match\.", "Matched as a substring."),
    (r"^Past-facing\.$", "A relative age counts back from now."),
    (r"^Decimal\.$", "Decimal value."),
    (r"compiled as a substring match", "matched as a substring"),
]


def note_text(raw: str | None) -> str:
    text = strip_source(raw)
    for pattern, repl in NOTE_REWRITES:
        text = re.sub(pattern, repl, text)
    return no_semicolons(text) if text else ""


def field_id(name: str) -> str:
    return "f-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def flag_id(name: str) -> str:
    return "is-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def chip(q: str) -> str:
    return code(q) + "{ .rn-q }"


def stage_link(stage: str, prefix: str = "../stages/") -> str:
    return f"[`{stage}`]({prefix}{stage}.md)"


def dimension_page(dim: dict, schema: dict, api_paths: set, mcp_dims: set) -> str:
    page = PAGES[dim["id"]]
    srcs = source_files(dim.get("registry_source", ""), dim.get("flags_source", ""), dim.get("row_source", ""),
                        dim.get("sort", {}).get("source", ""))
    label = dim["label"]
    has_groups = API[dim["id"]] + "/groups" in api_paths
    verbs = "search, group and sort" if has_groups else "search and sort"
    desc = (f"Everything you can {verbs} in the {label.lower()} dimension, with example queries. "
            f"Keep this page open while you write a query on {dim['noun_plural']}.")
    out = front_matter(f"{label}", desc, srcs or ["shared/definitions/asset_query.py"], SCRIPT,
                       layout="reference", nav_order=list(PAGES).index(dim["id"]))
    out += gen_line([DATA, "openapi.json", "mcp-dimensions.json"], SCRIPT)

    flag_field = next((f for f in dim["fields"] if f["type"] == "flag"), None)
    prefixes = ["is:"] + ([a + ":" for a in flag_field["aliases"]] if flag_field else [])

    where = ["in the query bar of the table", f"in the HTTP API with `POST {API[dim['id']]}`"]
    if dim["id"] in mcp_dims:
        where.append("from an MCP client with the tool `query_assets`")
    out += (f"Each row in the {label} dimension is {dim['row'][0].lower() + dim['row'][1:]} "
            f"You search these rows {join_words(where)}. "
            "For the syntax that works in every dimension, see [Query language](index.md).\n\n")

    out += "## About this dimension\n\n"
    out += "The basics: what a row is, which stages fill the dimension, and where you search it.\n\n"
    rows = [
        ["One row is", sentence(dim["row"])],
        ["Singular and plural", f"{dim['noun']}, {dim['noun_plural']}"],
        ["Identified by", code(dim["identity"])],
        ["Stages that add rows", ", ".join(stage_link(s) for s in dim["producing_stages"]) or "None"],
        ["Stages that cover it", ", ".join(stage_link(s) for s in dim["covering_stages"]) or "None"],
        ["Free-text fields", ", ".join(code(f) for f in dim["free_text_fields"]) or "None"],
        ["Flag prefixes", ", ".join(code(p) for p in prefixes)],
        ["Search API", code("POST " + API[dim["id"]])],
        ["Query bar placeholder", chip(dim["ui_placeholder_hint"])],
    ]
    out += table(["Property", "Value"], rows)
    out += ("Coverage tells you whether an empty table means that nothing was found or that nothing was looked for. "
            "A dimension is covered for a target when a covering stage succeeded in a run, or when a run wrote rows to it. "
            "Without coverage, the dimension reads **Not scanned**, which is not the same as zero rows.\n\n")

    out += "## Fields\n\n"
    out += ("Fields are the properties you search on, written `field:value`. An alias works the same as the field name. "
            "Select a field to see its operators, its values and an example.\n\n")
    rows = []
    for f in dim["fields"]:
        name = f"[{code(f['name'])}](#{field_id(f['name'])})"
        rows.append([name, ", ".join(code(a) for a in f["aliases"]), f["type"], f["group"], f["description"]])
    out += table(["Field", "Aliases", "Type", "Group", "Description"], rows)

    out += "## Flags\n\n"
    first = dim["flags"][0]["name"] if dim["flags"] else ""
    out += (f"Flags are yes-or-no properties of a row. Write them with {join_words([code(p) for p in prefixes], 'or')}"
            + (f", for example {chip('is:' + first)}" if first else "") + ".\n\n")
    rows = [[f"[{code('is:' + fl['name'])}](#{flag_id(fl['name'])})", fl["description"]] for fl in dim["flags"]]
    out += table(["Flag", "Description"], rows)

    if dim.get("group_by"):
        out += "## Group keys\n\n"
        if has_groups:
            out += ("Group the rows by one of these keys to count how many rows share each value. "
                    "Use the **Group by** menu of the table, or the `groups` search operation of the HTTP API.\n\n")
        else:
            out += (f"These group keys are defined for {dim['noun_plural']}. "
                    "The table of this dimension has no group menu, and the HTTP API has no `groups` operation for it.\n\n")
        out += table(["Key", "Label", "Groups"], [[code(g["key"]), g["label"], g["description"]] for g in dim["group_by"]])

    sort = dim.get("sort") or {}
    if sort:
        out += "## Sort\n\n"
        out += "The keys you can sort by, and the order you get when you do not choose one.\n\n"
        api, ui = sort.get("api_default", {}), sort.get("ui_default", {})
        out += table(["Property", "Value"], [
            ["Sort keys", ", ".join(code(k) for k in sort.get("keys", []))],
            ["API default", f"{code(api.get('sort'))} {api.get('order', '')}" if api else ""],
            ["Interface default", f"{code(ui.get('sort'))} {ui.get('order', '')}" if ui else ""],
            ["Tie-break", no_semicolons(sort.get("tiebreak", ""))],
        ])

    out += "## Columns\n\n"
    ui = dim.get("ui_columns") or {}
    out += ("The table always starts with its leading columns. "
            + ("You choose which optional columns to show. " if ui.get("optional") else "")
            + "An export of this dimension writes the export columns.\n\n")
    out += table(["Set", "Columns"], [
        ["Leading columns", ", ".join(f"**{c}**" for c in ui.get("lead", []))],
        ["Optional columns", ", ".join(f"**{c}**" for c in ui.get("optional", []))],
        ["Shown by default", ", ".join(f"**{c}**" for c in ui.get("default_visible", []))],
        ["Export columns", ", ".join(code(c) for c in dim.get("export_columns", []))],
    ])

    if dim.get("examples"):
        out += "## Examples\n\n"
        out += "Start from one of these queries and adjust it to your target.\n\n"
        groups: dict[str, list] = {}
        for ex in dim["examples"]:
            groups.setdefault(ex.get("group") or "Other", []).append(ex)
        for group in dim.get("example_groups") or list(groups):
            if group not in groups:
                continue
            out += f"### {group}\n\n"
            out += table(["Query", "Finds"], [[chip(ex["query"]), ex["description"]] for ex in groups[group]])

    out += "## Field reference\n\n"
    out += "Each field in detail: its type, the operators it accepts, its values and an example.\n\n"
    for f in dim["fields"]:
        out += f"### {f['name']} {{ #{field_id(f['name'])} }}\n\n"
        out += sentence(f["description"]) + "\n\n"
        facts = [("Type", f"`{f['type']}`" + (f", unit `{f['unit']}`" if f.get("unit") else "")), ("Group", f["group"])]
        if f["aliases"]:
            facts.append(("Aliases", ", ".join(code(a) for a in f["aliases"])))
        facts.append(("Operators", " ".join(code(o) for o in f["operators"])))
        if f["values"]:
            if f["type"] == "flag":
                facts.append(("Values", ", ".join(f"[{code(v)}](#{flag_id(v)})" for v in f["values"])))
            else:
                facts.append(("Values", ", ".join(code(v) for v in f["values"])))
        if f.get("example"):
            facts.append(("Example", chip(f["example"])))
        if f.get("free_text"):
            facts.append(("Free text", "Yes. A bare word searches this field"))
        if f.get("sub_field"):
            facts.append(("Sub-fields", code(f["sub_field"])))
        note = note_text(f.get("note"))
        if note:
            facts.append(("Matching", note))
        for k, v in facts:
            out += f"{k}\n:   {v}\n\n"

    out += "## Flag reference\n\n"
    out += "Each flag in detail, with the rule a row must meet to match it.\n\n"
    for fl in dim["flags"]:
        out += f"### is:{fl['name']} {{ #{flag_id(fl['name'])} }}\n\n"
        out += f"{sentence(fl['description'])}\n\n"
        out += f"Written as\n:   {', '.join(code(p + fl['name']) for p in prefixes)}\n\n"
        if fl.get("rule"):
            out += f"Matches when\n:   {sentence(no_semicolons(fl['rule']).rstrip('.'))}\n\n"
    return out


def grammar_page(schema: dict) -> str:
    g = schema["grammar"]
    srcs = list(g["source"].values())
    out = front_matter(
        "Query language",
        "How to write a reNgine query: fields and operators, connectors, lists, ranges, regular expressions, dates and free text. "
        "Come here when a query does not find what you expect, or when you need an exact limit or error message.",
        srcs, SCRIPT, layout="reference")
    out += gen_line([DATA], SCRIPT)
    out += ("You write queries in three places: the query bar of every result table, "
            "the `q` field of the search operations of the HTTP API, and the `query` argument of the MCP tool `query_assets`. "
            "The grammar is the same in all three. For a guided introduction, see [Query the attack surface](../../pentesters/query.md).\n\n")

    out += "## Dimensions\n\n"
    out += ("A dimension is one of the seven result types, and each has its own fields and flags. "
            "Open a dimension to see what you can search in it.\n\n")
    rows = []
    for dim in schema["dimensions"]:
        rows.append([f"[{dim['label']}]({PAGES[dim['id']]}.md)", sentence(dim["row"]), len(dim["fields"]), len(dim["flags"]), code("POST " + API[dim["id"]])])
    out += table(["Dimension", "One row", "Fields", "Flags", "Search API"], rows)

    out += "## Terms\n\n"
    out += ("A query is a list of terms. A term is `field<operator>value`, a flag such as `is:live`, or a bare word. "
            "When you put two terms side by side, a row must match both. These examples show the common shapes of a query.\n\n")
    out += table(["Query", "Matches"], [
        [code("status:200") + "{ .rn-q }", "Rows whose status equals 200"],
        [code("tech:nginx is:live") + "{ .rn-q }", "Live rows whose technology contains nginx"],
        [code("is:live and (status:403 or status:401)") + "{ .rn-q }", "Live rows answering 403 or 401"],
        [code('title:"sign in"') + "{ .rn-q }", "Rows whose title contains the phrase sign in"],
        [code("tech:[nginx,apache]") + "{ .rn-q }", "Rows whose technology contains either value"],
        [code("status:200..399") + "{ .rn-q }", "Rows with a status in the inclusive range"],
        [code("not is:cdn") + "{ .rn-q }", "Rows that are not served through a CDN"],
        [code("jenkins") + "{ .rn-q }", "Rows where any free-text field contains jenkins"],
    ])

    out += "## Operators\n\n"
    out += "The operator decides how reNgine compares a field with your value.\n\n"
    out += table(["Operator", "Meaning"], [[code(o["symbol"]), o["description"]] for o in g["operators"]])
    out += "### Operators by type\n\n"
    out += ("Not every operator works on every field. Find the type of a field on its dimension page, "
            "then check here which operators it accepts and how they match.\n\n")
    out += table(["Type", "Operators", "Matching"], [
        [code(t), " ".join(code(o) for o in ops),
         sentence(no_semicolons(g["match_semantics"].get(t, "")).rstrip(".")).replace("See grammar.dates.", "See [Dates](#dates).")]
        for t, ops in g["operators_by_type"].items()])
    out += ("Text fields compare without regard to case. `!=` also matches rows that have no value. "
            "A field that holds a list of values matches when any element matches, so `:` finds a substring in any element.\n\n")

    out += "## Connectors\n\n"
    out += "Connectors combine terms. Use them to require both terms, to accept either term, to exclude rows, or to group parts of a query.\n\n"
    def symbols(text: str) -> str:
        text = re.sub(r"(?<=\s)([-!])(?=\s)", lambda m: code(m.group(1)), text)
        return re.sub(r"\b(is:live and \(status:403 or status:401\)|tech:\[nginx,apache\]|status:200\.\.399)", lambda m: code(m.group(1)) + "{ .rn-q }", text)

    out += table(["Syntax", "Meaning"], [[code(c["symbol"]), symbols(c["description"])] for c in g["connectors"]])
    out += "These spellings mean the same, so write whichever you prefer.\n\n"
    out += table(["Word", "Same as"], [[code(k), code(v)] for k, v in g["connector_words"].items()])
    def prec(p: str) -> str:
        head, _, rest = p.partition(" (")
        words = " or ".join(code(w.strip()) for w in head.split(" / "))
        return words + (f" ({rest}" if rest else "")

    out += ("When a query mixes connectors, reNgine applies them in this order, tightest first: "
            + ", then ".join(prec(p) for p in g["precedence"]) + ". Use parentheses to group terms another way.\n\n")
    out += ("To exclude rows, write " + join_words([code(n.split(" (")[0]) for n in g["negation"]], "or")
            + ". `!=` and `!~` are operators, not negation.\n\n")

    out += "## Values\n\n"
    out += "How to write the value part of a term.\n\n"
    out += table(["Topic", "Rule"], [
        ["Quoting", g["quoting"]],
        ["Lists", sentence(no_semicolons(g["lists"]).rstrip("."))],
        ["Ranges", sentence(g["ranges"])],
        ["Wildcards", g["wildcards"]],
        ["Status classes", "Status fields also accept " + ", ".join(code(v) for v in g["status_classes"]["values"]) + "."],
        ["Presence words", "True: " + ", ".join(code(w) for w in g["presence_words"]["true"]) + ". False: " + ", ".join(code(w) for w in g["presence_words"]["false"]) + "."],
        ["Case", "Field names, connectors, flags and values are case-insensitive. `=` on a list-valued field compares one element exactly."],
    ])

    out += "### Units\n\n"
    out += ("Size and time fields accept a unit after the number, for example "
            + code("size:>1mb") + "{ .rn-q } or " + code("time:>500ms") + "{ .rn-q } on web assets.\n\n")
    out += table(["Kind", "Units"], [
        ["Bytes", ", ".join(f"{code(k)} = {v:,}" for k, v in g["units"]["bytes"].items())],
        ["Duration", ", ".join(f"{code(k)} = {v:g} s" for k, v in g["units"]["duration_seconds"].items())],
    ])

    d = g["dates"]
    out += "### Dates\n\n"
    out += ("Date fields take a relative age, an absolute date or a word. "
            "For example, " + code("discovered:<7d") + "{ .rn-q } finds web assets recorded in the last 7 days.\n\n")
    out += table(["Form", "Meaning"], [
        ["Relative age", "A number and a unit: " + ", ".join(code(u) for u in d["relative_units_seconds"]) + f". {sentence(no_semicolons(d['past_fields']))}"],
        ["Future-facing", sentence(d["future_fields"])],
        ["Absolute", ", ".join(code(f) for f in d["absolute_formats"][:3]) + f" and ISO 8601. {sentence(d['absolute'])}"],
        ["Words", ", ".join(code(w) for w in d["words"]) + ", both the current instant"],
        ["Time zone", sentence(d["timezone"])],
    ])

    r = g["regex"]
    out += "### Regular expressions\n\n"
    out += (f"Use `~` and `!~` when a substring is not precise enough. They take a PostgreSQL regular expression, "
            f"match it without regard to case, and work on string fields only. A pattern can be up to {r['max_length']} characters, "
            "and reNgine checks that it is valid before it runs. Put quotes around a pattern that contains whitespace, `(` or `)`.\n\n")

    ft = g["free_text"]
    out += "## Free text\n\n"
    out += ("When you do not know which field holds a value, type the value on its own. "
            "reNgine matches a bare word or a quoted phrase with `:` against every free-text field of the dimension, "
            "and a row matches when any of those fields does. Each dimension page lists its free-text fields. "
            f"A query can hold up to {ft['max_terms']} free-text words. "
            "If you write `name:value` and `name` is not a field, reNgine reads it as one free-text word, "
            "and the query bar shows **\"name\" is not a field, searched as text**.\n\n")

    lim = g["limits"]
    out += "## Limits\n\n"
    out += "Every query runs within these limits. Check them when a query is refused or a count stops at the cap.\n\n"
    out += table(["Limit", "Value"], [
        ["Query length", f"{lim['max_query_length']:,} characters"],
        ["Terms and connectors", f"{lim['max_query_nodes']} parts"],
        ["Free-text words", str(lim["max_free_terms"])],
        ["Regular expression length", f"{lim['max_regex_length']} characters"],
        ["Largest number", f"{lim['max_number']:,}"],
        ["Count cap", f"{lim['count_cap']:,} rows. A count at the cap is reported with `total_capped: true`."],
        ["Groups returned", str(lim["max_groups"])],
        ["Statement timeout", lim["statement_timeout"]],
        ["Queries in one count request", str(lim["count_request_max_queries"])],
    ])

    e = g["errors"]
    out += "## Errors\n\n"
    out += ("When reNgine cannot read a query, it tells you what is wrong and where. "
            "Over the HTTP API you get HTTP 200 with an `error` object and no rows. "
            "The object holds `message`, `hint`, and the `start` and `end` offsets of the problem in the query, with `end` exclusive. "
            "In the interface, the query bar underlines that part of the query. "
            "Look up a message below to see the hint that comes with it.\n\n")
    rows = []
    for msg in e["parser_messages"]:
        m, _, h = msg.partition(" / ")
        rows.append([m, h])
    out += table(["Message", "Hint"], rows)
    out += "### Database errors\n\n"
    out += ("A query can be valid and still fail in the database, for example when the search times out. "
            "You then see one of these messages.\n\n")
    out += table(["SQLSTATE", "Message", "Hint"], [[code(k), v[0], v[1] or ""] for k, v in e["database_messages"].items()])
    return out


def main() -> None:
    schema = load(DATA)
    api_paths = set(load("openapi.json")["paths"])
    mcp_dims = set(load("mcp-dimensions.json")["dimension_keys"])
    changed = 0
    changed += write(OUT / "index.md", grammar_page(schema))
    for dim in schema["dimensions"]:
        changed += write(OUT / f"{PAGES[dim['id']]}.md", dimension_page(dim, schema, api_paths, mcp_dims))
    print(f"gen_query: {len(schema['dimensions']) + 1} pages, {changed} changed")


if __name__ == "__main__":
    main()
