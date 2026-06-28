import asyncio

from registry import TOOLSETS, create_all_server, create_group_servers, toolset_metadata
from server import app, get_tool_names
from starlette.testclient import TestClient


async def tool_names(mcp):
    return set(await get_tool_names(mcp))


def test_toolsets_define_scoped_endpoints():
    assert [toolset.name for toolset in TOOLSETS] == ["json", "text", "math", "time"]
    assert [toolset.endpoint for toolset in TOOLSETS] == [
        "/json/mcp",
        "/text/mcp",
        "/math/mcp",
        "/time/mcp",
    ]


def test_each_group_has_only_its_tools():
    groups = create_group_servers()

    assert asyncio.run(tool_names(groups["json"])) == {"json_pretty", "json_shape"}
    assert asyncio.run(tool_names(groups["text"])) == {"text_stats", "text_keywords"}
    assert asyncio.run(tool_names(groups["math"])) == {"math_summary", "math_percent_change"}
    assert asyncio.run(tool_names(groups["time"])) == {"time_utc_now", "time_in_timezone"}


def test_all_endpoint_contains_every_tool():
    assert asyncio.run(tool_names(create_all_server())) == {
        "json_pretty",
        "json_shape",
        "text_stats",
        "text_keywords",
        "math_summary",
        "math_percent_change",
        "time_utc_now",
        "time_in_timezone",
    }


def test_discovery_api_matches_registry():
    client = TestClient(app)
    response = client.get("/toolsets")

    assert response.status_code == 200
    data = response.json()
    assert data["all"]["endpoint"] == "/mcp"
    assert len(data["all"]["tools"]) == 8
    assert [item["endpoint"] for item in data["toolsets"]] == [item["endpoint"] for item in toolset_metadata()]

