# FastMCP Endpoint Toolsets

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-3.x-orange.svg)
![Protocol: MCP](https://img.shields.io/badge/protocol-MCP-blue.svg)

**Stop shipping one giant MCP tool surface to every agent.**

> The missing FastMCP starter for URL-scoped native MCP toolsets: **one server, one port, many focused endpoints**.

`fastmcp-endpoint-toolsets` gives you a clean packaging pattern for tool-bloat-free MCP servers: keep your tools in one FastMCP server, but expose each tool group through its own native MCP URL.

```text
/mcp          -> all tools
/json/mcp     -> JSON tools only
/db/mcp       -> database tools only
/docs/mcp     -> documentation tools only
/text/mcp     -> text tools only
/math/mcp     -> math tools only
/time/mcp     -> time tools only
```

Point an agent at `/math/mcp` and it sees **only** the math tools. Point it at `/mcp` and it sees everything. Same process, same port -- and every URL is **native FastMCP Streamable HTTP**. No proxy. No gateway. No fleet of tiny servers. No custom REST wrapper.

## Why it matters

Once a server has 50+ tools, every agent gets all of them in its prompt -- context bloats, token cost climbs, and tool-selection accuracy drops. Endpoint Toolsets keep the deployment simple while keeping each agent's tool surface focused:

- **Focused context** -- each agent loads only its toolset, not your entire catalog.
- **One deploy** -- one server, one port, one container for all your tool code.
- **Zero extra infra** -- nothing to run or secure between the agent and your tools.
- **Add a tool in ~5 lines** -- drop a file in `tools/`, register it once, and a new endpoint appears.

## How it's different

Every row below is a valid pattern. This project fills the gap in the **bottom** one.

| Approach | Deploys / ports | Tool surface per agent | Extra moving parts |
|---|---|---|---|
| One big FastMCP server | 1 | **All** tools, always | None |
| FastMCP `mount()` / `import_server()` | 1 | All tools (name-prefixed) at **one** URL | None |
| Tag filtering per client | 1 | Filtered, but configured **client-side** | None |
| N separate MCP servers | **N** | Scoped | N processes / ports / containers |
| MCP gateway / proxy | 1+ | Scoped, routes to external servers | A gateway to run and secure |
| **Endpoint Toolsets (this repo)** | **1** | **Scoped, per URL, server-side** | **None** |

> Scoping here is per-endpoint **context isolation** -- each group is its own FastMCP instance with its own tool registry. Everything runs in one process.

## Quick start

```powershell
cd fastmcp_endpoint_toolsets
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

Open the dashboard at **http://127.0.0.1:8001**, or connect any MCP client:

```text
http://127.0.0.1:8001/mcp        # all tools
http://127.0.0.1:8001/json/mcp   # json only
http://127.0.0.1:8001/math/mcp   # math only
http://127.0.0.1:8001/text/mcp   # text only
http://127.0.0.1:8001/time/mcp   # time only
```

Prefer containers? One image, one port, every endpoint behind it:

```powershell
docker compose up --build
```

> **Podman:** `podman build` / `podman run` work unchanged. Its default OCI format ignores the `HEALTHCHECK` line -- add `--format docker` to `podman build` to keep it.

## Built-in dashboard

Dynamic UI to see existing tools!

`http://127.0.0.1:8001` serves a zero-dependency web UI that reads `/toolsets` live and shows every endpoint, its tools, and its tags at a glance -- the fastest way to confirm exactly what each agent will see.

```text
GET /          -> this dashboard
GET /health    -> health check
GET /toolsets  -> JSON discovery of every endpoint + its tools
```

## See it in MCP Inspector

Want proof the scoping is real? With the server running:

```powershell
npx @modelcontextprotocol/inspector
```

Set Transport to `Streamable HTTP`, connect to `http://127.0.0.1:8001/json/mcp`, and **List Tools** -- you'll see only the JSON tools. Switch the URL to `/math/mcp` and you'll see only math tools. Same server, same port -- a focused surface at every URL.
Full walkthrough in [USAGE.md](USAGE.md).

## Add a toolset

```python
# tools/docs_tools.py
from fastmcp import FastMCP

def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def docs_search(query: str) -> list[str]:
        """Search docs."""
        return [f"Result for {query}"]
```

```python
# registry.py -- add one entry to TOOLSETS
Toolset(name="docs", title="Docs Toolset",
        description="Documentation search tools.",
        tags=("docs", "search"), register=docs_tools.register),
```

Restart the server and `/docs/mcp` is live. Full guide in [USAGE.md](USAGE.md).

## What it is / isn't

**It is:** native endpoint toolsets from a single FastMCP server -- a clean base to fork, rename, and build your own MCP server on.

**It isn't:** an MCP proxy, an MCP gateway, a REST API in MCP clothing, or a bridge to external MCP servers. In-process, by design.

## Documentation

- [USAGE.md](USAGE.md) -- mental model, MCP Inspector, Docker, project layout, adding toolsets
- [CONTRIBUTING.md](CONTRIBUTING.md) -- dev setup, running tests, and how to contribute

## License

[MIT](LICENSE) -- fork it, rename it, ship it.

---

<sub>**Keywords:** FastMCP endpoint toolsets, MCP endpoint toolsets, scoped MCP endpoints, per-agent MCP tools, grouped MCP tools, one server one port MCP, multi endpoint MCP server, native MCP tool groups, reduce MCP tool context, FastMCP Streamable HTTP, MCP server template, tool-bloat-free MCP.</sub>
