"""MkDocs hook for rengine.wiki: reference counts, page metadata, Markdown copies, llms.txt and llms-full.txt."""

from __future__ import annotations

import html
import json
import logging
import posixpath
import re
from pathlib import Path

from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs.hooks.rengine")

STATE: dict = {"pages": {}, "md_paths": {}, "nav": None}

REQUIRED_META = ("title", "description", "sources", "revised")
COUNT_TOKEN = re.compile(r"\{\{\s*counts\.([a-z_]+)\s*\}\}")
INDEX_TOKEN = re.compile(r"^\{\{\s*section_index\s*\}\}\s*$", re.M)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


# ---------- counts ----------


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compute_counts(data: Path) -> dict:
    schema = _load_json(data / "query-schema.json")
    stages = _load_json(data / "stages.json")
    mcp = _load_json(data / "mcp-tools.json")
    openapi = _load_json(data / "openapi.json")
    repo = _load_json(data / "repo.json")
    chat = _load_json(data / "chat-commands.json")
    methods = {"get", "post", "put", "patch", "delete"}
    return {
        "query_dimensions": len(schema["dimensions"]),
        "query_fields": sum(len(d["fields"]) for d in schema["dimensions"]),
        "query_flags": sum(len(d["flags"]) for d in schema["dimensions"]),
        "stages": len(stages["stages"]),
        "steps": len(stages["execution_steps"]),
        "mcp_tools": len(mcp["tools"]),
        "mcp_capabilities": len(mcp["capabilities"]),
        "api_paths": len(openapi["paths"]),
        "api_operations": sum(1 for p in openapi["paths"].values() for m in p if m in methods),
        "api_tags": len({t for p in openapi["paths"].values() for m, op in p.items() if m in methods for t in op.get("tags", [])}),
        "cli_commands": len(repo["cli"]["commands"]),
        "installer_flags": sum(len(g["items"]) for g in repo["installer"]["groups"] if g["title"] != "Environment"),
        "env_variables": repo["env"]["count"],
        "chat_commands": len(chat),
        "pinned_tools": len(repo["tools"]["tools"]),
    }


# ---------- nav ----------


def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        for line in text[4:end].splitlines():
            m = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if m:
                meta[m.group(1)] = m.group(2).strip().strip('"')
    return meta


def _expand(entry, docs: Path):
    if isinstance(entry, list):
        return [_expand(e, docs) for e in entry]
    if isinstance(entry, dict):
        return {k: _expand(v, docs) for k, v in entry.items()}
    if isinstance(entry, str) and entry.endswith("/") and "://" not in entry:
        folder = docs / entry
        files = sorted(p for p in folder.glob("*.md") if p.name != "index.md")
        ordered = sorted(files, key=lambda p: (float(_front_matter(p).get("nav_order", 1e9)), p.stem))
        items = []
        if (folder / "index.md").exists():
            items.append(entry + "index.md")
        items += [entry + p.name for p in ordered]
        return items
    return entry


def on_config(config, **kwargs):
    root = Path(config.config_file_path).parent
    config.extra["counts"] = compute_counts(root / "data")
    config["nav"] = _expand(config["nav"], Path(config.docs_dir))
    STATE["pages"] = {}
    STATE["site_url"] = config.site_url.rstrip("/") + "/"
    return config


def on_files(files, config, **kwargs):
    STATE["md_paths"] = {}
    STATE["urls"] = {}
    for f in files.documentation_pages():
        url = f.url.rstrip("/")
        STATE["md_paths"][f.src_uri] = (url + ".md") if url not in ("", ".") else "index.md"
        STATE["urls"][f.src_uri] = f.url
    return files


def _href(src: str, link: str) -> str:
    if link not in STATE["urls"]:
        log.warning(f"{src}: front matter links to '{link}', which is not a page")
        return link
    return STATE["urls"][link] or "."


def on_nav(nav, config, files, **kwargs):
    STATE["nav"] = nav
    return nav


# ---------- page ----------


def _inline_html(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append("<code>" + html.escape(part[1:-1]) + "</code>")
        else:
            esc = html.escape(part, quote=False)
            esc = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", esc)
            out.append(esc)
    return "".join(out)


def _source_link(base: str, path: str, docs_base: str = "") -> dict:
    if path.startswith("docs:") and docs_base:
        file = path[5:]
        return {"path": path, "href": docs_base + file}
    m = re.match(r"^(.*?)(?::(\d+)(?:-(\d+))?)?$", path)
    file, start, end = m.group(1), m.group(2), m.group(3)
    kind = "tree" if file.endswith("/") or "." not in file.rsplit("/", 1)[-1] else "blob"
    href = base.replace("/blob/", f"/{kind}/") + file.rstrip("/")
    if start:
        href += f"#L{start}" + (f"-L{end}" if end else "")
    return {"path": path, "href": href}


def on_page_markdown(markdown, page: Page, config, files, **kwargs):
    meta = page.meta
    src = page.file.src_uri
    for key in REQUIRED_META:
        if not meta.get(key):
            log.warning(f"{src}: front matter has no '{key}'")
    for block in re.findall(r'<div class="rn-ui\b.*?(?=^///|\Z)', markdown, re.S | re.M):
        inner = block.split("\n", 1)[1] if "\n" in block else ""
        if re.search(r"<(?:p|div|ul|ol|li|table|h\d)[\s>]", inner):
            log.warning(f"{src}: an interface recreation holds a block element; use spans inside div.rn-ui")
        if 'aria-label="' not in block.split("\n", 1)[0]:
            log.warning(f"{src}: an interface recreation has no aria-label")
    if re.search(r"^# \S", _strip_fences(markdown), re.M):
        log.warning(f"{src}: the page body has an H1; the title comes from front matter")
    sources = meta.get("sources") or []
    if isinstance(sources, str):
        sources = [sources]
    meta["source_links"] = [_source_link(config.extra["source_base"], s, config.extra.get("docs_source_base", "")) for s in sources]
    if meta.get("description"):
        meta["description_md"] = str(meta["description"]).strip()
        meta["description_html"] = _inline_html(meta["description_md"])
        meta["description"] = re.sub(r"[`*]", "", meta["description_md"])
    md_path = STATE["md_paths"].get(src, "index.md")
    meta["md_url"] = md_path
    if meta.get("layout") == "pane":
        hide = list(meta.get("hide") or [])
        if "toc" not in hide:
            hide.append("toc")
        meta["hide"] = hide

    counts = config.extra["counts"]

    def count(m):
        key = m.group(1)
        if key not in counts:
            log.warning(f"{src}: unknown count '{key}'")
            return m.group(0)
        return f"{counts[key]:,}"

    markdown = COUNT_TOKEN.sub(count, markdown)
    if INDEX_TOKEN.search(markdown):
        markdown = INDEX_TOKEN.sub(lambda m: _section_index(page), markdown)
    for key in ("audiences", "capabilities", "reference", "run", "layers", "tour"):
        for item in meta.get(key) or []:
            if item.get("link"):
                item["href"] = _href(src, item["link"])
            if item.get("text"):
                item["text"] = COUNT_TOKEN.sub(count, str(item["text"]))
                item["text_html"] = _inline_html(item["text"])
            for point in item.get("points") or []:
                point["text"] = COUNT_TOKEN.sub(count, str(point["text"]))
                point["text_html"] = _inline_html(point["text"])
    for key in ("run_text", "layers_text", "tour_text"):
        if meta.get(key):
            meta[key + "_html"] = _inline_html(str(meta[key]))
    for key in ("capabilities_link", "install_link", "burp_link"):
        if meta.get(key):
            meta[key.replace("_link", "_href")] = _href(src, meta[key])
    STATE["pages"][src] = {
        "title": meta.get("title") or page.title,
        "description": meta.get("description_md", ""),
        "md_path": md_path,
        "markdown": markdown,
        "meta": {k: meta.get(k) for k in ("sources", "revised", "generated", "audiences", "capabilities", "install", "endpoint", "run_title", "run_text", "run", "layers_title", "layers_text", "layers", "tour_title", "tour_text", "tour")},
    }
    return markdown


def _description(page: Page) -> str:
    import yaml

    text = Path(page.file.abs_src_path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ""
    try:
        meta = yaml.safe_load(text.split("---", 2)[1]) or {}
    except yaml.YAMLError:
        log.warning(f"{page.file.src_uri}: front matter does not parse")
        return ""
    return str(meta.get("description") or "").strip()


def _section_index(page: Page) -> str:
    section = page.parent
    if section is None:
        return ""
    out = []
    loose = []
    for item in section.children:
        if isinstance(item, Page):
            if item is not page:
                loose.append(item)
            continue
        if isinstance(item, Section):
            out.append(f"## {item.title}\n")
            out.append("| Page | Covers |\n|---|---|")
            for child in item.children:
                pages = [child] if isinstance(child, Page) else [c for c in child.children if isinstance(c, Page)][:1]
                for pg in pages:
                    rel = posixpath.relpath(pg.file.src_uri, posixpath.dirname(page.file.src_uri))
                    title = pg.title if isinstance(child, Page) else child.title
                    out.append(f"| [{title}]({rel}) | {_description(pg)} |")
            out.append("")
    if loose:
        out.insert(0, "| Page | Covers |\n|---|---|\n" + "\n".join(
            f"| [{pg.title}]({posixpath.relpath(pg.file.src_uri, posixpath.dirname(page.file.src_uri))}) | {_description(pg)} |" for pg in loose) + "\n")
    return "\n".join(out)


def on_page_context(context, page, config, nav, **kwargs):
    ancestors = [a.title for a in reversed(page.ancestors) if isinstance(a, Section)]
    page.meta["crumbs"] = ancestors
    return context


# ---------- Markdown copies ----------


def _strip_fences(text: str) -> str:
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append("")
            continue
        if m:
            fence = m.group(1)
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


KEY_NAMES = {"ctrl": "Ctrl", "cmd": "Cmd", "shift": "Shift", "alt": "Alt", "enter": "Enter", "esc": "Esc",
             "tab": "Tab", "space": "Space", "up": "Up", "down": "Down", "left": "Left", "right": "Right",
             "backspace": "Backspace", "page-up": "PageUp", "page-down": "PageDown", "home": "Home", "end": "End"}

ATTR_LIST = re.compile(r"\s*\{:?\s*(?:[.#][\w-]+|[\w-]+=(?:\"[^\"]*\"|'[^']*'|[^\s}]+))(?:\s+(?:[.#][\w-]+|[\w-]+=(?:\"[^\"]*\"|'[^']*'|[^\s}]+)))*\s*\}")
INLINE_TAGS = re.compile(r"</?(?:span|small|b|i|em|strong|abbr|sup|sub|u|mark)\b[^>]*>")


def _keys(m) -> str:
    return "`" + "+".join(KEY_NAMES.get(k, k.upper() if len(k) == 1 else k) for k in m.group(1).split("+")) + "`"


def _inline_clean(line: str) -> str:
    parts = re.split(r"(`+[^`]*`+)", line)
    out = []
    for part in parts:
        if part.startswith("`"):
            out.append(part)
            continue
        part = re.sub(r'<span class="rn-ref"[^>]*>.*?</span>', "", part)
        part = re.sub(r"<kbd>(.*?)</kbd>", r"`\1`", part)
        part = re.sub(r"<code>(.*?)</code>", lambda m: "`" + html.unescape(m.group(1)).replace("|", "\\|") + "`", part)
        part = re.sub(r"\+\+([\w+-]+)\+\+", _keys, part)
        part = re.sub(r"<br\s*/?>", " ", part)
        part = INLINE_TAGS.sub("", part)
        part = ATTR_LIST.sub("", part)
        out.append(part)
    return "".join(out)


def _abs_link(target: str, page_src: str) -> str:
    if re.match(r"^[a-z]+:", target) or target.startswith("#"):
        return target
    path, _, frag = target.partition("#")
    if not path:
        return target
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(page_src), path))
    md = STATE["md_paths"].get(resolved)
    if md is None and not path.endswith(".md"):
        return STATE["site_url"] + resolved + (("#" + frag) if frag else "")
    if md is None:
        return target
    return STATE["site_url"] + md + (("#" + frag) if frag else "")


def clean_markdown(text: str, page_src: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    fence = None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if fence:
            out.append(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            i += 1
            continue
        if m:
            fence = m.group(1)
            out.append(line)
            i += 1
            continue
        stripped = line.strip()
        if re.match(r"^<!--.*-->$", stripped):
            i += 1
            continue
        # interface recreation: replaced by its aria-label
        if re.match(r'^<div class="rn-ui\b', stripped):
            label = re.search(r'aria-label="([^"]*)"', stripped)
            depth = 0
            while i < len(lines):
                depth += len(re.findall(r"<div\b", lines[i])) - len(re.findall(r"</div>", lines[i]))
                i += 1
                if depth <= 0:
                    break
            if label:
                out.append(f"*Interface: {html.unescape(label.group(1))}*")
                out.append("")
            continue
        m_lbl = re.match(r'^<(?:div|p) class="rn-pane-(?:label|note)">(.*?)</(?:div|p)>$', stripped)
        if m_lbl:
            out.append(f"*{html.unescape(re.sub(r'<[^>]+>', '', m_lbl.group(1)))}*")
            out.append("")
            i += 1
            continue
        m_ep = re.match(r'^<div class="rn-ep"><span[^>]*>(\w+)</span>(.*?)</div>$', stripped)
        if m_ep:
            out.append(f"`{m_ep.group(1)} {m_ep.group(2).strip()}`")
            i += 1
            continue
        if re.match(r"^</?div\b[^>]*>$", stripped) or re.match(r"^<div\b[^>]*></div>$", stripped):
            i += 1
            continue
        if re.match(r'^<div class="rn-pane-head"', stripped):
            title = re.sub(r"<[^>]+>", " ", stripped)
            title = re.sub(r"\s+", " ", title).strip()
            if title:
                out.append(f"**{title}**")
            i += 1
            continue
        m_tab = re.match(r"^/// tab \| (.+)$", stripped)
        if m_tab:
            out.append(f"**{m_tab.group(1).strip()}**")
            out.append("")
            i += 1
            continue
        if stripped == "///":
            i += 1
            continue
        m_ad = re.match(r'^!!! (note|warning|danger)(?: "([^"]*)")?\s*$', stripped)
        if m_ad:
            kind, title = m_ad.group(1), m_ad.group(2)
            body = []
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith("    ")):
                body.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            while body and not body[-1].strip():
                body.pop()
            out.append(f"> **{title or kind.capitalize()}**")
            out.append(">")
            for b in body:
                b = re.sub(r"\]\(([^)\s]+)\)", lambda mm: "](" + _abs_link(mm.group(1), page_src) + ")", _inline_clean(b))
                out.append(("> " + b).rstrip())
            out.append("")
            continue
        line = _inline_clean(line)
        line = re.sub(r"\]\(([^)\s]+)\)", lambda mm: "](" + _abs_link(mm.group(1), page_src) + ")", line)
        out.append(line.rstrip())
        i += 1
    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result).strip() + "\n"
    return result


def _header(info: dict, version: str) -> str:
    meta = info["meta"]
    lines = [f"# {info['title']}", ""]
    if meta.get("endpoint"):
        lines += [f"`{meta['endpoint']}`", ""]
    if info["description"]:
        lines += [f"> {info['description']}", ""]
    facts = [f"Applies to reNgine {version}."]
    if meta.get("sources"):
        srcs = meta["sources"] if isinstance(meta["sources"], list) else [meta["sources"]]
        facts.append("Sources: " + ", ".join(f"`{s}`" for s in srcs) + ".")
    if meta.get("generated"):
        facts.append(f"Generated by `{meta['generated']}`.")
    if meta.get("revised"):
        facts.append(f"Revised {meta['revised']}.")
    lines += [" ".join(facts), ""]
    return "\n".join(lines) + "\n"


def _home_markdown(info: dict, config) -> str:
    meta = info["meta"]
    site = STATE["site_url"]
    out = []
    for row in meta.get("audiences") or []:
        out.append(f"- [{row['title']}]({site}{STATE['md_paths'].get(row['link'], row['link'])}): {row['text']}")
    for title_key, text_key, key in (("run_title", "run_text", "run"), ("layers_title", "layers_text", "layers"), ("tour_title", "tour_text", "tour")):
        items = meta.get(key) or []
        if not items:
            continue
        out += ["", f"## {meta.get(title_key)}", ""]
        if meta.get(text_key):
            out += [meta[text_key], ""]
        for item in items:
            out.append(f"- [{item['title']}]({site}{STATE['md_paths'].get(item['link'], item['link'])}): {item['text']}")
            for point in item.get("points") or []:
                out.append(f"  - {point['text']}")
    caps = meta.get("capabilities") or []
    if caps:
        out += ["", "## Capabilities", ""]
        for cap in caps:
            out.append(f"- [{cap['title']}]({site}{STATE['md_paths'].get(cap['link'], cap['link'])}): {cap['text']}")
    if meta.get("install"):
        out += ["", "## Install", "", "```bash", meta["install"], "```"]
    body = "\n".join(out)
    return body + "\n\n" + clean_markdown(info["markdown"], "index.md")


def _walk(items, trail):
    for item in items:
        if isinstance(item, Section):
            yield from _walk(item.children, trail + [item.title])
        elif isinstance(item, Page):
            yield trail, item


def on_post_build(config, **kwargs):
    site = Path(config.site_dir)
    version = config.extra["rengine_version"]
    rendered: dict[str, str] = {}
    for src, info in STATE["pages"].items():
        if src == "index.md":
            body = _home_markdown(info, config)
        else:
            body = clean_markdown(info["markdown"], src)
        text = _header(info, version) + body
        rendered[src] = text
        dest = site / info["md_path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")

    base = STATE["site_url"]
    head = [
        f"# {config.site_name}",
        "",
        f"> {config.site_description.strip()}",
        "",
        f"reNgine {version}. Each page is available as Markdown at its URL with `.md` in place of the trailing slash, "
        f"for example {base}pentesters/install.md. The full text of every page is at {base}llms-full.txt.",
        "",
    ]
    groups: dict[str, list] = {}
    order: list[str] = []
    seen = set()
    for trail, page in _walk(STATE["nav"].items if STATE["nav"] else [], []):
        src = page.file.src_uri
        if src in seen or src not in STATE["pages"]:
            continue
        seen.add(src)
        key = ": ".join(trail[:2]) if trail else "Home"
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(src)
    index = list(head)
    full = list(head)
    if "index.md" in STATE["pages"] and "index.md" not in seen:
        home = STATE["pages"]["index.md"]
        index += ["## Home", "", f"- [{home['title']}]({base}index.md): {home['description']}", ""]
        full += ["", "---", "", f"<!-- {base}index.md -->", "", rendered["index.md"].strip(), ""]
    for key in order:
        index += [f"## {key}", ""]
        for src in groups[key]:
            info = STATE["pages"][src]
            desc = f": {info['description']}" if info["description"] else ""
            index.append(f"- [{info['title']}]({base}{info['md_path']}){desc}")
            full += ["", "---", "", f"<!-- {base}{info['md_path']} -->", "", rendered[src].strip(), ""]
        index.append("")
    for old, new in (config.extra.get("redirects") or {}).items():
        dest = site / old / "index.html"
        if dest.exists():
            log.warning(f"redirect {old} would replace a page")
            continue
        depth = len([p for p in old.strip("/").split("/") if p])
        rel = "../" * depth + new
        target = STATE["site_url"] + new
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>Moved</title><link rel=\"canonical\" href=\"{target}\">"
            f"<meta http-equiv=\"refresh\" content=\"0; url={rel}\"><meta name=\"robots\" content=\"noindex\"></head>"
            f"<body><a href=\"{rel}\">{target}</a></body></html>\n", encoding="utf-8")
    root = Path(config.config_file_path).parent
    api_dir = site / "developers" / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    (api_dir / "openapi.json").write_text((root / "data" / "openapi.json").read_text(encoding="utf-8"), encoding="utf-8")
    for src_file in sorted((root / "agent-files").rglob("*.md")):
        dest = site / "agent-files" / src_file.relative_to(root / "agent-files")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src_file.read_text(encoding="utf-8"), encoding="utf-8")
    (site / "llms.txt").write_text("\n".join(index).rstrip() + "\n", encoding="utf-8")
    (site / "llms-full.txt").write_text("\n".join(full).rstrip() + "\n", encoding="utf-8")
    log.info(f"rengine hook: {len(rendered)} Markdown pages, llms.txt with {len(seen)} entries")
