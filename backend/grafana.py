import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def get_delay():
    url = "http://localhost:8001/mcp"

    async with streamable_http_client(url) as (
        read_stream,
        write_stream
    ):
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "query_prometheus",
                {
                    "datasourceUid": "grafanacloud-prom",
                    "expr": "filmops_schedule_delay_minutes",
                    "queryType": "range",
                    "startTime": "now-24h",
                    "endTime": "now",
                    "stepSeconds": 60
                }
            )

            text = result.content[0].text
            data = json.loads(text)

            values = data["data"][0]["values"]
            latest = values[-1][1]

            return int(float(latest))