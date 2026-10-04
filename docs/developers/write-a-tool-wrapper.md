---
title: Write a tool wrapper
description: Wrap a command-line tool so a stage or a toolbox tool can run it. Your wrapper builds the tool's command line, runs the binary in the worker image and turns its output into records reNgine can store.
layout: pane
sources:
  - tools/runner/executor.py
  - tools/runner/models.py
  - tools/runner/abort.py
  - tools/runner/fieldmap.py
  - tools/cdncheck/client.py
  - tools/cdncheck/__init__.py
  - tools/ffuf/client.py
  - tools/ffuf/parser.py
  - tools/pyproject.toml
  - worker/Dockerfile
  - stages/cdn_check/stage.py
  - shared/definitions/tools.py
  - shared/services/orchestrator/tracking.py
  - api/app/services/scan_engine/validation.py
  - tests/pipeline/test_content_discovery.py
  - tests/pipeline/test_tool_header_flags.py
  - tests/pipeline/test_tool_args_precedence.py
  - tests/pipeline/test_tool_abort.py
revised: 2026-10-03
---

Write a wrapper when you want reNgine to run a tool it does not run yet. The wrapper is the only place that knows the tool's flags and output format, so the stage that calls it deals with plain records.

`tools/` is installed into the api and worker images as the dependency-only project `rengine-tools`. The tool binaries exist only in the worker image, under `/usr/local/bin`, and the api image has none. So a wrapper that shells out is called from a stage or from a queued [toolbox tool](write-a-toolbox-tool.md), both of which run on the worker.

These are the files you work with:

| Path | Content |
|---|---|
| `tools/<tool>/client.py` | The client class: builds the arguments and runs the binary |
| `tools/<tool>/parser.py` | One function that turns one output record into a plain `dict`, or `None` |
| `tools/<tool>/models.py`, `service.py` | Typed results and a higher-level service class, where a tool needs them (`dnsx`, `ripestat`, `whois`, `viewdns`) |
| `tools/<tool>/__init__.py` | Re-exports the client and its error |
| `tools/runner/executor.py` | `CLIToolRunner`, `merge_extra_args`, `failure_excerpt`, `tool_path` |
| `tools/runner/models.py` | `OutputFormat`, `ToolResult`, `StreamOutcome`, the `CommandRecorder` protocol |
| `tools/runner/abort.py` | `StageAbortedError` and the abort check bound to the running stage |
| `tools/runner/fieldmap.py` | `F` and `parse_record`, a declarative record-to-field map |
| `tools/data/` | Bundled wordlists: `content.txt`, `subdomains.txt`, `vhosts.txt` |

Not every wrapper runs a binary. `crtsh`, `ripestat`, `whois` and `viewdns` are HTTP clients, and `banner` opens raw sockets and speaks SOCKS5 and HTTP CONNECT itself (`tools/banner/proxy.py`).

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Wrap a binary

The pane follows `cdncheck` from the Dockerfile to the stage that calls it, with the `ffuf` parser as the parsing example.

1. **Pin the binary.** Add the tool to `worker/Dockerfile` at a fixed version: a `go install <module>@<version>` line in the `gotools` stage, a release archive checked against a SHA-256 per architecture, or a pinned `pip install`. The build copies the binaries to `/usr/local/bin`. <span class="rn-ref" data-tab="Dockerfile">Shown in the pane</span>
2. **Rebuild the worker image.** Build `worker-default` and recreate the containers. Every worker container runs the image that build produces. <span class="rn-ref" data-tab="Dockerfile">Shown in the pane</span>
3. **Read the flags in the image.** Take every flag and its value format from the tool's own help inside the worker image, and its exit codes from a run there. Measure each flag, and never assume one: the same flag name takes different values in different tools. <span class="rn-ref" data-tab="Dockerfile">Shown in the pane</span>
4. **Write the client.** Create `CLIToolRunner(<binary>, default_timeout=...)` in the constructor, and raise the tool's own error on `ToolNotFoundError`. Build the arguments in a method and call `run` or `stream_json`. Pass `recorder`, `tool` and `extra_args` through, so the command shows in the run's command log and the engine's tool args reach the tool. <span class="rn-ref" data-tab="Client">Shown in the pane</span>
5. **Write the parser.** Write one function that handles one record. It checks each type, bounds each string and returns `None` for anything that is not a result, so the stage only ever sees well-formed records. <span class="rn-ref" data-tab="Parser">Shown in the pane</span>
6. **Call it from a stage.** Pass the stage's recorder, the engine's tool args, the proxy, the headers and the transport. Turn the tool's error into a warning and a `partial` result, so a missing or failing tool shows up in the run instead of passing as an empty success. <span class="rn-ref" data-tab="Stage call">Shown in the pane</span>
7. **Let engines pass tool args.** To let an engine add its own flags for your tool, add a `ToolSpec` to `SCAN_TOOLS` in `shared/definitions/tools.py`. List the flags tool args may not set in `DENIED_FLAGS` in the same file. <span class="rn-ref" data-tab="Stage call">Shown in the pane</span>
8. **Test the parser.** Feed it recorded output, and the shapes it must drop. <span class="rn-ref" data-tab="Test">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Tool wrapper</b><span>tools/cdncheck/</span></div>

/// tab | Dockerfile
<div class="rn-pane-label">worker/Dockerfile, gotools stage</div>

```dockerfile
RUN --mount=type=cache,target=/cache/build --mount=type=cache,target=/cache/mod \
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@v2.6.1 \
    && go install -v github.com/projectdiscovery/httpx/cmd/httpx@v1.12.0 \
    && go install -v github.com/projectdiscovery/cdncheck/cmd/cdncheck@v1.3.0
```

<div class="rn-pane-label">worker/Dockerfile, development stage</div>

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    ... \
    && python3 -m pip install --no-cache-dir --break-system-packages wafw00f==2.4.2

COPY --from=gotools /out/bin/ /usr/local/bin/
```

<div class="rn-pane-label">rebuild, then read the flags</div>

```bash
docker compose build worker-default
docker compose up -d
docker compose exec worker-scans cdncheck -h
```
///

/// tab | Client
<div class="rn-pane-label">tools/cdncheck/client.py</div>

```python
from tools.runner import CLIToolRunner, OutputFormat, ToolNotFoundError
from tools.runner.models import CommandRecorder

CDNCHECK_BINARY = "cdncheck"
DEFAULT_TIMEOUT = 120


class CdncheckError(Exception):
    """cdncheck is not installed or failed."""


class CdncheckClient:
    def __init__(
        self,
        *,
        recorder: CommandRecorder | None = None,
        extra_args: list[str] | None = None,
    ) -> None:
        self.recorder = recorder
        self.extra_args = extra_args or []
        try:
            self._runner = CLIToolRunner(
                CDNCHECK_BINARY, default_timeout=DEFAULT_TIMEOUT
            )
        except ToolNotFoundError as e:
            raise CdncheckError(str(e)) from e

    def check(self, ips: list[str]) -> dict[str, dict]:
        if not ips:
            return {}
        result = self._runner.run(
            args=["-resp"],
            input_data=ips,
            use_stdin=True,
            use_output_file=False,
            output_format=OutputFormat.JSONL,
            json_flag="-jsonl",
            silent=True,
            silent_flag="-silent",
            recorder=self.recorder,
            tool=CDNCHECK_BINARY,
            extra_args=self.extra_args,
        )
        if not result.success and not result.json_records:
            raise CdncheckError(result.error or "cdncheck failed")
        out: dict[str, dict] = {}
        for rec in result.json_records:
            ...
        return out
```

<div class="rn-pane-label">tools/ffuf/client.py, a streaming call</div>

```python
with self._runner.stream_json(
    args=args,
    json_flag="-json",
    silent=True,
    silent_flag="-s",
    timeout=budget + _BUDGET_SLACK,
    recorder=self.recorder,
    tool=FFUF_BINARY,
    extra_args=self.extra_args,
) as stream:
    yield stream
```
///

/// tab | Parser
<div class="rn-pane-label">tools/ffuf/parser.py</div>

```python
from typing import Any

_MAX_URL = 2000


def parse_ffuf_record(record: dict[str, Any]) -> dict[str, Any] | None:
    """One ffuf NDJSON hit."""
    url = record.get("url")
    status = record.get("status")
    if not isinstance(url, str) or not url or len(url) > _MAX_URL:
        return None
    if not isinstance(status, int):
        return None
    redirect = record.get("redirectlocation") or None
    return {
        "url": url,
        "status_code": status,
        "content_length": _number(record.get("length")),
        "words": _number(record.get("words")),
        "lines": _number(record.get("lines")),
        "content_type": (record.get("content-type") or None),
        "redirect_location": redirect if isinstance(redirect, str) else None,
        "host": record.get("host") or None,
    }


def _number(value) -> int | None:
    return value if isinstance(value, int) else None
```
///

/// tab | Stage call
<div class="rn-pane-label">stages/cdn_check/stage.py</div>

```python
try:
    data = CdncheckClient(
        recorder=self.ctx.recorder,
        extra_args=self.ctx.resolved.tool_args("cdncheck"),
    ).check(ips[:_MAX_IPS])
except CdncheckError as exc:
    logger.warning("cdncheck unavailable, skipping CDN attribution")
    return StageResult(
        counts={"addresses": len(ips)},
        warnings=[str(exc)],
        partial=True,
    )
```

<div class="rn-pane-label">shared/definitions/tools.py</div>

```python
SCAN_TOOLS: tuple[ToolSpec, ...] = (
    ...
    ToolSpec(
        name="cdncheck",
        label="cdncheck",
        phase="CDN Attribution",
        example="-resp",
    ),
)

DENIED_FLAGS: dict[str, frozenset[str]] = {
    ...
    "cdncheck": frozenset({"o", "output"}),
}
```
///

/// tab | Test
<div class="rn-pane-label">tests/pipeline/test_content_discovery.py, shortened</div>

```python
import pytest

from tools.ffuf.parser import parse_ffuf_record

pytestmark = pytest.mark.pipeline


def _hit(**over) -> dict:
    return {
        "url": "https://a.example.com/admin",
        "status": 302,
        "length": 358,
        "redirectlocation": "https://a.example.com/login",
        "host": "a.example.com",
        **over,
    }


def test_a_hit_becomes_an_observation():
    parsed = parse_ffuf_record(_hit())
    assert parsed["status_code"] == 302
    assert parsed["redirect_location"] == "https://a.example.com/login"


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"url": "https://a.example.com/x"},
        {"url": "https://a.example.com/x", "status": "200"},
        {"url": "x" * 3000, "status": 200},
    ],
)
def test_anything_that_is_not_a_hit_is_dropped(record: dict):
    assert parse_ffuf_record(record) is None
```
///

</div>
</div>

## CLIToolRunner.run

Use `run` when the tool finishes and you read its whole output at the end. It runs the binary once, waits for it and returns a `ToolResult`. These are the parameters you can pass:

| Parameter | Default | Effect |
|---|---|---|
| `args` | `None` | The client's own arguments |
| `input_data` | `None` | A list of lines or a string. Written to a temporary file and passed with `input_flag`, or sent on stdin with `use_stdin=True`. |
| `input_flag` | `-l` | The flag that names the input file |
| `use_stdin` | `False` | Send `input_data` on stdin |
| `use_output_file` | `True` | Pass a temporary file with `output_flag` and read the output from it. Falls back to stdout when the file is empty. |
| `output_flag` | `-o` | The flag that names the output file |
| `output_format` | `OutputFormat.PLAIN` | `PLAIN` returns `output_lines`. `JSONL` returns `json_records` and appends `json_flag`. |
| `json_flag` | `-json` | Appended only with `OutputFormat.JSONL` |
| `silent`, `silent_flag` | `True`, `-silent` | Append the silent flag |
| `timeout` | the runner's `default_timeout` | Seconds before the process is killed |
| `env` | `None` | Variables added to the environment |
| `recorder`, `tool` | the runner's | The command log and the tool name recorded with the command |
| `extra_args` | the runner's | Engine tool args, merged by `merge_extra_args` |
| `should_stop` | the stage's abort check | Polled every 2 seconds while the tool runs |

Use `stream_json` instead when you want to handle records while the tool is still running, so a stage can write results as they come. It takes the same input, JSON, silent, timeout, environment, recorder and tool arguments, plus `idle_timeout` and `stderr_sink`. It yields a `StreamOutcome` whose `records` iterator reads stdout one JSON object per line. After the block, the outcome holds `return_code`, `timed_out`, `stopped`, `record_count` and `stderr`.

`run` returns a `ToolResult` with these fields:

| `ToolResult` field | Content |
|---|---|
| `success` | The exit code is 0 |
| `exit_code` | The exit code, `-1` on a timeout |
| `stdout`, `stderr` | The raw output |
| `output_lines` | Non-empty lines, for `PLAIN` |
| `json_records` | Parsed objects, for `JSONL`. Lines that are not JSON objects are skipped. |
| `duration_seconds` | Wall time |
| `command` | The command line |
| `error` | The failure message, or `None` |
| `timed_out` | The process was killed at `timeout`. Output written before the kill is parsed. |

## What the runner does for you

The runner handles the parts every tool needs, so your client does not have to: finding the binary, cleaning the environment, stopping the process and logging the command.

| Behaviour | Detail |
|---|---|
| Binary lookup | `/usr/local/bin` first, then `PATH`, when the runner is created |
| Environment | The worker's environment without `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, `FLOWER_PASSWORD` and `REDIS_PASSWORD` |
| Process | Started in its own session. On a timeout or a halt the whole process group is killed. |
| Halt | When the scan is paused or cancelled the tool is killed and `StageAbortedError` is raised |
| Decoding | stdout and stderr are decoded with `errors="replace"` |
| Logging | The command is logged with credentials masked |
| Command log | With a recorder, each command is recorded on the run with its tool name, masked command line, return code, output up to 200,000 characters, error and duration, and `command_started` and `command_finished` are emitted |

When something goes wrong, the runner raises or returns one of these messages:

| Message | Raised or returned when |
|---|---|
| `Binary '<binary>' not found in PATH. Install it in the worker image.` | `ToolNotFoundError`, when the runner is created |
| `<binary> exited with code <n>: <excerpt>` | `ToolResult.error`, on a non-zero exit |
| `<binary> timed out after <n> seconds` | `ToolResult.error`, on a timeout |
| `<binary> stopped: the scan was halted` | Recorded on the command when the scan is halted |
| `Unexpected error running <binary>: <error>` | `ToolExecutionError`, on any other failure |

The excerpt in the exit message is built to show the actual error. It is taken from stderr, or from stdout up to 2,000 characters when stderr yields none: lines tagged `FTL` or `FATAL` first, then `ERR` or `ERROR`, then lines that read as errors, otherwise the last three lines. Banner lines and JSON lines are removed, and the excerpt is cut at 500 characters.

## Tool args

Tool args let an administrator add flags for one tool in a scan engine. An engine stores them per tool in `tool_options`. `ResolvedScanConfig.tool_args(<tool>)` splits them as shell arguments and returns an empty list when they name a denied flag. `merge_extra_args` then drops every flag the client already set, under either spelling when the client passes an alias map such as `HTTPX_ALIASES`, and the runner's input, output, JSON and silent flags. Tool args add flags and never restate one.

reNgine refuses tool args with one of these messages:

| Message | Cause |
|---|---|
| `'<tool>' does not take custom arguments. Tools that do: <tools>.` | The tool has no `ToolSpec` in `SCAN_TOOLS` |
| `<tool> options may not exceed 1000 characters.` | The argument string is longer than `MAX_TOOL_OPTION_LEN` |
| `<tool> options carry a masked value. Enter the value again.` | The string holds a masked value |
| `<tool> options are not valid shell arguments: <error>` | The string does not split as shell arguments |
| `<tool> does not take <flag>.` | The string names a flag in `DENIED_FLAGS` |
| `Tool arguments require administrator access.` | A user who is not an administrator changes them |

## Measured flags

Check this table before you pass a flag to one of these tools. Each row was read from the tool in the worker image, and several of them differ from what the flag name suggests. [Pinned tool versions](../reference/tool-versions.md) lists the versions.

| Tool | Behaviour |
|---|---|
| naabu, dnsx | `-timeout` takes a Go duration such as `3s`, not milliseconds |
| httpx, katana, nuclei, tlsx, subfinder, urlfinder | `-timeout` takes integer seconds |
| urlfinder | Has no `-t`. Passing one exits with code 2. |
| amass v4 | Prints a relationship graph, not a list of host names. `enum -passive` does not exit early. Not in the default tool set. |
| httpx | The stream probe is bounded by idle time, `timeout=0` with `idle_timeout`, the same rule as dnsx |
| dnsx | Answers every `-axfr` query with an object. A transfer carries `chain` entries with `all` records. Not rate limited by any stage. |
| tlsx | Writes its records and does not exit. Bounded by a budget. `-proxy` takes socks5 only, as a full URL. |
| ffuf | One process per site. In `-json` mode `input.FUZZ` is base64. The word is read off `url`. |
| nuclei | `-silent` is not passed. `-dast` loads only fuzzing templates, and without it none load. An `-input-mode` other than `list` turns `-dast` on. |
| dalfox v3 | A release binary. Reads URLs on stdin with `--input-type pipe`. Exits 1 when it reports findings and 2 on an error. `--format jsonl` ends with a `findings_count` line. |
| alterx | Reads seeds on stdin. `-l <file>` answers `no input found`. |
| julius | Ignores `-f` without a positional target. Targets go on stdin with `-`. Has no proxy flag and reads `HTTPS_PROXY`. |
| naabu | `-proxy` takes socks5 only, as `host:port`, with `-proxy-auth user:pass`. `-passive` is an HTTPS call to Shodan and follows the proxy environment. |
| wafw00f | Takes headers as a file, `-H <path>`, one `Name: Value` per line, and drops a header whose value holds a colon. Has no rate flag and no thread flag. |

The flag that sends a custom header differs per tool, so each client holds its own as `HEADER_FLAG`. `tests/pipeline/test_tool_header_flags.py` pins the measured values.

| Client | `HEADER_FLAG` |
|---|---|
| httpx, nuclei | `-header` |
| katana | `-headers` |
| ffuf, julius | `-H` |
| dalfox | `--headers` |

## Tests

These tests cover the runner and the existing wrappers. Add a parser test like them for your tool.

| Test | Covers |
|---|---|
| `tests/pipeline/test_tool_args_precedence.py` | `merge_extra_args` drops restated flags, both spellings and the reserved flags |
| `tests/pipeline/test_tool_header_flags.py` | Each client emits the header flag its tool defines |
| `tests/pipeline/test_tool_abort.py` | Exit codes, stdin, timeouts and the kill on halt |
| `tests/pipeline/test_content_discovery.py`, `test_dalfox.py`, `test_zone_transfer.py` | Parsers fed recorded output |

To run your wrapper as part of a scan, see [Write a stage](write-a-stage.md).
