"""Write reference/cli.md, installer.md, configuration.md and tool-versions.md from data/repo.json and data/env-notes.json."""

from __future__ import annotations

import re

from gen_common import DOCS, code, front_matter, gen_line, load, sentence, table, upper_first, write

SCRIPT = "scripts/gen_ops.py"

# What each command runs, read from deploy/rengine.
CLI_NOTES = {
    "start": ("`docker compose up -d`", ""),
    "stop": ("`docker compose down`. Containers and the network are removed, volumes are kept.", ""),
    "restart": ("`docker compose down`, then `docker compose up -d`", ""),
    "status": ("`docker compose ps`, then a request to `<PUBLIC_ORIGIN>/api/v1/health/health`",
               "`API answering at <origin>`, or `The API did not respond. Check that the api service is running.`"),
    "logs": ("`docker compose logs -f --tail 200`, for every service or the named ones", ""),
    "scale": ("Writes `WORKER_SCANS_REPLICAS=<n>` to `.env`, then `docker compose up -d worker-scans`", "`error: usage: rengine scale <n>`"),
    "update": ("Downloads the release, pulls its images, saves a database snapshot, stops the services that hold a database connection, "
               "replaces the compose file, the CLI and the backup script, and starts the stack",
               "`Already on <tag>.`, `Updated to <tag>.`, `Running scans: <n>. Stages in flight run again after the update.`"),
    "backup": ("`scripts/backup.sh dump`, into `./backups` or the directory given", ""),
    "restore": ("`scripts/backup.sh restore <archive>`", "`error: usage: rengine restore <archive>`"),
    "uninstall": ("Asks for confirmation, then `docker compose down --volumes --remove-orphans` and removes the `rengine` link",
                  "`Containers and data volumes are removed. Backups and .env stay in <dir>.`"),
    "version": ("Prints `RENGINE_TAG` from `.env`", ""),
}
CLI_PAGES = {
    "update": ("Update and roll back", "../pentesters/update.md"),
    "backup": ("Back up and restore", "../pentesters/backup.md"),
    "restore": ("Back up and restore", "../pentesters/backup.md"),
    "uninstall": ("Uninstall reNgine", "../pentesters/uninstall.md"),
    "status": ("Troubleshooting", "../pentesters/troubleshooting.md"),
    "logs": ("Troubleshooting", "../pentesters/troubleshooting.md"),
    "scale": ("Troubleshooting", "../pentesters/troubleshooting.md"),
}


def cli_page(repo: dict) -> str:
    cli = repo["cli"]
    out = front_matter("rengine CLI", "Use the `rengine` command on your server to start and stop reNgine, check its health, read its logs, "
                       f"update it, and back it up or restore it. This page lists all {len(cli['commands'])} commands and what each one runs.",
                       ["deploy/rengine", "scripts/backup.sh"], SCRIPT, layout="reference")
    out += gen_line(["repo.json"], SCRIPT)
    out += ("The installer puts the command in `bin/rengine` inside the install directory and links it into `/usr/local/bin` or `~/.local/bin`. "
            "It runs Docker Compose in the install directory and needs the `.env` file that the installer wrote. "
            "If root owns the install directory, run it with `sudo`. "
            "When a command fails, it prints `error: <message>` and exits with status 1.\n\n")
    out += "Run `rengine` with no command, or `rengine help`, to print this summary:\n\n"
    out += "```text\n" + cli["help"] + "\n```\n\n"
    out += "## Commands\n\n"
    out += "Each command, with a link to its details below.\n\n"
    rows = []
    for c in cli["commands"]:
        usage = f"rengine {c['name']}" + (f" {c['args']}" if c["args"] else "")
        opts = "".join(f" {code(o['flag'])}: {o['description']}." for o in c["options"])
        rows.append([f"[{code(usage)}](#{c['name']})", sentence(upper_first(c["description"])) + opts])
    out += table(["Command", "What it does"], rows)
    for c in cli["commands"]:
        usage = f"rengine {c['name']}" + (f" {c['args']}" if c["args"] else "")
        out += f"## {c['name']} {{ #{c['name']} }}\n\n"
        out += f"```bash\n{usage}\n```\n\n"
        out += sentence(upper_first(c["description"])) + "\n\n"
        runs, msgs = CLI_NOTES.get(c["name"], ("", ""))
        if runs:
            out += f"Runs\n:   {sentence(runs)}\n\n"
        for o in c["options"]:
            out += f"`{o['flag']}`\n:   {sentence(upper_first(o['description']))}\n\n"
        if msgs:
            out += f"What it prints\n:   {msgs}\n\n"
        if c["name"] in CLI_PAGES:
            label, link = CLI_PAGES[c["name"]]
            out += f"Guide\n:   [{label}]({link})\n\n"
    return out


def installer_page(repo: dict) -> str:
    inst = repo["installer"]
    flags = [i for g in inst["groups"] if g["title"] != "Environment" for i in g["items"]]
    env_vars = [i for g in inst["groups"] if g["title"] == "Environment" for i in g["items"]]
    out = front_matter("Installer flags",
                       "Every option of `install.sh`, the script that installs reNgine. Use it when you install without the guided questions, "
                       f"for example from a provisioning script. It covers {len(flags)} flags and "
                       + ("the one environment variable the installer reads." if len(env_vars) == 1
                          else f"the {len(env_vars)} environment variables the installer reads."),
                       ["install.sh", "README.md"], SCRIPT, layout="reference")
    out += gen_line(["repo.json"], SCRIPT)
    out += ("Run the installer without flags and it asks you for each setting. "
            "Give it a reachability flag and it runs without asking, which suits automated installs. "
            "For a walkthrough, see [Install reNgine](../pentesters/install.md).\n\n")
    out += "Run `install.sh --help` to print this summary:\n\n"
    out += "```text\n" + inst["help"] + "\n```\n\n"
    mem, disk = inst.get("memory_gb"), inst.get("disk_gb")
    if mem and disk:
        out += (f"The installer checks the host first. It stops if the host has less than {mem['minimum']} GB of memory "
                f"or {disk['minimum']} GB of free disk. The recommended size is {mem['recommended']} GB of memory and {disk['recommended']} GB of disk. "
                "`--force` skips these checks.\n\n")
    for g in inst["groups"]:
        title = g["title"].replace(", one of", "")
        out += f"## {title}\n\n"
        if g["title"].endswith("one of"):
            out += ("Reachability decides how people reach your instance: on a public domain, on the address of the server, "
                    "or only from the machine itself. Pick one of these flags.\n\n")
        elif title == "Options":
            out += "These set the ports, the first administrator, the install directory, the release and the other details of an install.\n\n"
        elif title == "Environment":
            out += "The installer also reads this from the environment.\n\n"
        rows = []
        for i in g["items"]:
            desc = i["description"] or ("Email of the first administrator" if i["flag"] == "--admin-email" else "")
            parts = []
            for part in desc.split("\n"):
                part = re.sub(r"(?<![\w`])(--[a-z][\w-]*|[a-z0-9.-]+/[\w./-]+|127\.0\.0\.1|443)(?![\w`])", lambda m: code(m.group(1)), part)
                part = upper_first(part.strip())
                parts.append(part + "." if part and part[-1] not in ".:!?)" else part)
            rows.append([code(i["flag"] + (" " + i["arg"] if i["arg"] else "")), " ".join(parts)])
        out += table(["Flag" if title != "Environment" else "Variable", "What it does"], rows)
    return out


def configuration_page(repo: dict, notes: dict) -> str:
    env = repo["env"]
    out = front_matter(
        "Configuration variables",
        f"The {env['count']} variables of `.env.example`, plus the ones an installed instance adds, with what each one does "
        "and the value the installer writes. Use it when you tune an instance or troubleshoot one.",
        [".env.example", "shared/config.py", "api/app/config.py", "install.sh", "docker-compose.prod.yml"], SCRIPT, layout="reference")
    out += gen_line(["repo.json", "env-notes.json"], SCRIPT)
    out += ("Your instance reads its settings from `.env` and `api.env` in the install directory. The installer writes both files. "
            "`.env.example` in the repository is the template for the development stack. "
            "After you change a value, run `rengine restart` so that the services pick it up.\n\n")
    out += ("!!! danger \"SECRET_KEY\"\n    `SECRET_KEY` encrypts the credentials, tokens and two-factor secrets that reNgine stores. "
            "Your backup archives contain it. If you replace it, reNgine can no longer read the stored secrets or the two-factor secrets.\n\n")
    out += ("Each section below follows a section of `.env.example`. **Example value** is the value in `.env.example`, "
            "**Installer** is the value the installer writes, and **Effect** is what the variable changes.\n\n")
    v = notes["variables"]
    for sec in env["sections"]:
        title = sec["title"].split(",")[0].split(":")[0]
        out += f"## {title}\n\n"
        if sec["title"] != title:
            note = upper_first(sec["title"][len(title):].lstrip(",: "))
            note = re.sub(r": (docker [^`]+)$", lambda m: f": `{m.group(1)}`", note)
            out += sentence(note) + "\n\n"
        rows = []
        for var in sec["variables"]:
            n = v.get(var["name"], {})
            rows.append([f"{code(var['name'])}", code(var["default"]) if var["default"] else "Empty", n.get("installer", ""), n.get("note", sentence(upper_first(var["comment"])) if var["comment"] else "")])
        out += table(["Variable", "Example value", "Installer", "Effect"], rows)
    out += "## Variables outside .env.example\n\n"
    out += "An installed instance also uses these variables, which `.env.example` does not list.\n\n"
    out += table(["Variable", "Where", "Effect"], [[code(e["name"]), e["where"], e["note"]] for e in notes["extra"]])
    missing = [var["name"] for sec in env["sections"] for var in sec["variables"] if var["name"] not in v]
    if missing:
        raise SystemExit(f"gen_ops: env-notes.json has no note for {missing}")
    return out


def tools_page(repo: dict) -> str:
    t = repo["tools"]
    out = front_matter("Pinned tool versions",
                       "The exact version of every scanning tool, runtime and base image in reNgine 3.0.0. "
                       "Use it to find out which version of a tool ran your scan, or to check a tool against a known issue.",
                       ["worker/Dockerfile", "api/Dockerfile", "frontend/Dockerfile", "docker-compose.prod.yml"], SCRIPT, layout="reference")
    out += gen_line(["repo.json"], SCRIPT)
    out += ("Each version is pinned in a Dockerfile or in the compose file, so every install of 3.0.0 runs the same scanning tools.\n\n")
    out += "## Scanning tools\n\n"
    out += "The scanning tools in the worker image, each built or installed at the version below.\n\n"
    rows = [[code(x["name"]), code(x["version"]), code(x["module"]) if x["kind"] == "go" else x["module"], x["source"]] for x in t["tools"] if x["kind"] != "build"]
    out += table(["Tool", "Version", "Source", "Pinned in"], rows)
    out += "## Build toolchain\n\n"
    out += "The toolchain the worker image uses to build the scanning tools.\n\n"
    out += table(["Tool", "Version", "Pinned in"], [[x["name"], code(x["version"]), x["source"]] for x in t["tools"] if x["kind"] == "build"])
    if t.get("apt_packages"):
        out += ("## System packages\n\nThe images also install these packages from the Debian archive of their base image. "
                "They are not pinned, so you get the version the archive holds when the image is built: "
                + ", ".join(code(p) for p in t["apt_packages"]) + ".\n\n")
    out += "## Base images\n\n"
    out += "The images that each reNgine image is built on, and the images that the compose file runs directly.\n\n"
    out += table(["Image", "File", "Stage"], [[code(i["image"]), i["file"], i["stage"]] for i in t["images"]])
    return out


def main() -> None:
    repo = load("repo.json")
    notes = load("env-notes.json")
    ref = DOCS / "reference"
    changed = 0
    changed += write(ref / "cli.md", cli_page(repo))
    changed += write(ref / "installer.md", installer_page(repo))
    changed += write(ref / "configuration.md", configuration_page(repo, notes))
    changed += write(ref / "tool-versions.md", tools_page(repo))
    print(f"gen_ops: 4 pages, {changed} changed")


if __name__ == "__main__":
    main()
