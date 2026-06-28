# Usage

## The Mental Model

Endpoint Toolsets are simple:

```text
tools/json_tools.py  -> registered as json -> /json/mcp
tools/text_tools.py  -> registered as text -> /text/mcp
tools/math_tools.py  -> registered as math -> /math/mcp
tools/time_tools.py  -> registered as time -> /time/mcp
all registered tools -> /mcp
```

`server.py` mounts everything. `registry.py` decides what groups exist. `tools/` contains the actual tool code.

## Project Layout

```text
fastmcp_endpoint_toolsets/
|-- server.py              # read this first: one server, many MCP endpoints
|-- registry.py            # define endpoint toolsets here
|-- client.py              # smoke client that lists tools per endpoint
|-- Dockerfile             # one container, one port
|-- docker-compose.yml
|-- requirements.txt
|-- pyproject.toml
|-- LICENSE
|-- README.md
|-- USAGE.md
|-- CONTRIBUTING.md
|-- static/
|   `-- index.html         # local dashboard
|-- tools/
|   |-- json_tools.py
|   |-- text_tools.py
|   |-- math_tools.py
|   `-- time_tools.py
`-- tests/
    `-- test_endpoint_toolsets.py
```

## Run Locally

```powershell
python server.py
```

## List Toolsets

```text
GET http://127.0.0.1:8001/toolsets
```

## Test With The Included Client

```powershell
python client.py
```

Expected shape -- the aggregate endpoint exposes everything, each scoped endpoint only its own group:

```text
http://127.0.0.1:8001/mcp -> 8 tools: ...
http://127.0.0.1:8001/json/mcp -> 2 tools: json_pretty, json_shape
http://127.0.0.1:8001/text/mcp -> 2 tools: text_stats, text_keywords
http://127.0.0.1:8001/math/mcp -> 2 tools: math_summary, math_percent_change
http://127.0.0.1:8001/time/mcp -> 2 tools: time_utc_now, time_in_timezone
```

## Inspect Endpoints Visually

With the server running, start the official MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector
```

Then, in the Inspector UI:

1. Transport Type: `Streamable HTTP`.
2. URL: `http://127.0.0.1:8001/json/mcp` -> Connect -> List Tools (json tools only).
3. Change URL to another `/<toolset>/mcp` and reconnect to see a different surface.
4. Use `http://127.0.0.1:8001/mcp` to see every tool at once.

## Run In One Container

```powershell
docker compose up --build
```

Everything is served on a single port (`8001`); each toolset stays at its own URL.

## Add Your Own Group

1. Create a new file in `tools/`.
2. Define `register(mcp)`.
3. Add one `Toolset(...)` entry in `registry.py`.
4. Restart `python server.py`.

That is the whole pattern.
