# Contributing

Thanks for taking a look. This repo is intentionally small — it is a **starter pattern**, not a framework.

## What belongs here

- Improvements to the endpoint-toolset packaging pattern itself.
- Generic, dependency-light starter toolsets (text, json, math, time, etc.).
- Docs, Docker, MCP Inspector, and developer-experience improvements.

## What does not belong here

- External MCP proxying / gateway behavior (this is in-process only, by design).

## Local setup

```powershell
cd fastmcp_endpoint_toolsets
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

## Adding a toolset

1. Create `tools/<name>_tools.py` with a `register(mcp)` function.
2. Add one `Toolset(...)` entry to `registry.py`.
3. Add a test to `tests/`.
4. Run `pytest` and `python client.py` against a running server.

## Pull requests

- Keep changes focused and the diff small.
- Update `README.md` / `USAGE.md` if behavior changes.
- Make sure `pytest` passes.
