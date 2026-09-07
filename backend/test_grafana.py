import asyncio

from backend.grafana import get_delay


delay = asyncio.run(get_delay())

print("Grafana delay:", delay)