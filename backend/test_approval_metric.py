import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def check_metric():
    async with streamable_http_client(
        "http://localhost:8001/mcp"
    ) as (
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
                    "expr": "filmops_recommendation_approved",
                    "queryType": "range",
                    "startTime": "now-1h",
                    "endTime": "now",
                    "stepSeconds": 60
                }
            )

            print(result.content[0].text)


asyncio.run(check_metric())