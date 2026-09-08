FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c '\
GRAFANA_URL="$GRAFANA_STACK_URL" \
GRAFANA_SERVICE_ACCOUNT_TOKEN="$GRAFANA_SERVICE_TOKEN" \
uvx mcp-grafana \
--transport streamable-http \
--address 0.0.0.0:8001 \
--disable-write & \
uvicorn backend.main:app \
--host 0.0.0.0 \
--port ${PORT:-8000}'