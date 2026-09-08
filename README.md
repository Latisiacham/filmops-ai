# 🎬 FilmOps AI

## The AI Production Control Room

FilmOps AI is an agentic production-control platform designed to help film crews detect production risks, understand their impact, and respond before those problems become costly delays.

When an incident occurs, FilmOps combines production data, Grafana observability, Google ADK agents, and Gemini reasoning to provide the production team with an actionable recovery recommendation.

> **Detect → Investigate → Recommend → Approve → Observe**

---

## 🎯 The Problem

Film productions are complex environments where equipment failures, crew availability, scheduling conflicts, and unexpected delays can quickly become expensive.

Production teams often need to manually gather information from multiple sources before deciding how to respond.

FilmOps AI creates a centralized AI-powered control room that connects those signals and helps production teams make faster operational decisions.

---

## 💡 How FilmOps AI Works

FilmOps monitors production information such as:

- Scene status
- Equipment availability
- Crew attendance
- Production incidents
- Schedule delays
- Recovery-plan approvals

When an incident is detected, specialized logic investigates its impact.

For example:

```text
Camera 03 goes offline
        ↓
Scene 18 — Night Chase is affected
        ↓
Schedule delay detected
        ↓
Production context sent to Google ADK agent
        ↓
Gemini generates a recovery recommendation
        ↓
Production team reviews recommendation
        ↓
Recommendation approved
        ↓
Approval metric sent to Grafana Cloud
```

---

## 🤖 AI Production Director

FilmOps includes an **AI Production Director** implemented using the Google Agent Development Kit (ADK).

The agent receives production context including:

- Equipment failures
- Available equipment
- Affected scenes
- Schedule delays

It uses Gemini to reason about the incident and recommend a short, practical recovery action.

The application also includes an in-memory recommendation cache to avoid unnecessary repeated AI requests for the same incident.

If the AI service is temporarily unavailable, FilmOps falls back gracefully instead of taking down the production dashboard.

---

## 📊 Grafana Cloud + Grafana MCP

Grafana is part of the FilmOps runtime architecture rather than being used only as a visualization layer.

FilmOps sends production telemetry to **Grafana Cloud** using OpenTelemetry-compatible metrics.

Example metrics include:

```text
filmops_schedule_delay_minutes
filmops_recommendation_approved
```

FilmOps also integrates the official **Grafana MCP server (`mcp-grafana`)**.

The backend queries Grafana Cloud Prometheus data through Grafana MCP and uses the returned production signal inside the application workflow.

For example:

```text
Grafana Cloud
      ↓
Grafana MCP
      ↓
FilmOps Backend
      ↓
Schedule Analysis
      ↓
AI Production Director
```

When a production manager approves an AI recovery plan, FilmOps sends an approval metric back to Grafana Cloud.

This creates an observable loop between production signals, AI decision-making, and human action.

---

## 🧠 Agent Workflow

FilmOps separates production reasoning into focused components.

### Equipment Agent

Detects offline production equipment and identifies available alternatives.

### Schedule Agent

Determines which scene is affected and evaluates the current schedule delay.

### AI Production Director

Combines the equipment and scheduling context and uses Google ADK + Gemini to recommend a recovery action.

This creates the workflow:

```text
Production Data
      ↓
Equipment Analysis
      ↓
Schedule Analysis
      ↓
Google ADK Agent
      ↓
Gemini
      ↓
Recovery Recommendation
      ↓
Human Approval
```

---

## 🏗️ Architecture

```text
                    FILMOPS AI
                        │
                        ▼
                Web Dashboard
                        │
                        ▼
                 FastAPI Backend
                  │           │
                  │           │
                  ▼           ▼
          Production Agents   Grafana MCP
                  │                │
                  ▼                ▼
             Google ADK       Grafana Cloud
                  │          Prometheus / OTLP
                  ▼                ▲
               Gemini              │
                  │                │
                  ▼                │
          AI Recommendation        │
                  │                │
                  ▼                │
           Human Approval ─────────┘
```

---

## 🛠️ Technology Stack

### AI

- Google Agent Development Kit (ADK)
- Gemini
- Google Gen AI SDK

### Backend

- Python
- FastAPI
- Uvicorn

### Observability

- Grafana Cloud
- Grafana MCP (`mcp-grafana`)
- Prometheus
- OpenTelemetry metrics

### Frontend

- HTML
- CSS
- JavaScript

### Deployment

- Docker
- Render

---

## 🎥 Demo Scenario

The FilmOps demo simulates a film production during **Day 12 — Night Shoot**.

The system detects:

```text
Camera 03 Failure
```

FilmOps determines that the failure affects:

```text
Scene 18 — Night Chase
```

and that production has accumulated:

```text
45 minutes of schedule delay
```

The AI Production Director analyzes the available equipment and production impact and recommends a recovery strategy.

The production manager can then select:

```text
Approve Recommendation
```

FilmOps records that decision as:

```text
filmops_recommendation_approved = 1
```

in Grafana Cloud.

---

## 🚀 Running FilmOps Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd filmops-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_key
GRAFANA_STACK_URL=your_grafana_stack_url
GRAFANA_SERVICE_TOKEN=your_service_account_token
GRAFANA_URL=your_otlp_metrics_endpoint
GRAFANA_USER=your_otlp_instance_id
GRAFANA_TOKEN=your_otlp_token
```

Never commit the `.env` file.

### 5. Start Grafana MCP

```bash
set -a
source .env
set +a

GRAFANA_URL="$GRAFANA_STACK_URL" \
GRAFANA_SERVICE_ACCOUNT_TOKEN="$GRAFANA_SERVICE_TOKEN" \
uvx mcp-grafana \
--transport streamable-http \
--address localhost:8001 \
--disable-write
```

### 6. Start FilmOps

In another terminal:

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🐳 Docker

FilmOps can also run as a Docker container.

Build:

```bash
docker build -t filmops-ai .
```

Run:

```bash
docker run --rm \
  --env-file .env \
  -p 8000:8000 \
  -p 8001:8001 \
  filmops-ai
```

Then open:

```text
http://127.0.0.1:8000
```

---

## 🔐 Security

Sensitive credentials are supplied through environment variables and are excluded from Git and Docker build context.

The Grafana MCP runtime is started with:

```text
--disable-write
```

to restrict MCP operations to read-only access.

The repository does not contain API keys, Grafana tokens, or service-account credentials.

---

## 🛡️ Resilience

FilmOps is designed so that individual external-service failures do not take down the production dashboard.

The application includes:

- Gemini/ADK recommendation fallback
- AI recommendation caching
- Grafana query fallback
- Human approval before recovery actions
- Read-only Grafana MCP access

---

## 🌟 Future Development

Future versions of FilmOps could support:

- Multiple simultaneous production incidents
- Live equipment telemetry
- Crew scheduling integrations
- Production budget impact prediction
- Call-sheet analysis
- Location and weather risk monitoring
- Multi-agent coordination
- Automated production reports
- Historical incident analysis

---

## 🏆 Hackathon

FilmOps AI was built for the **Google Cloud Agentic Cinema Hackathon — Grafana Labs Challenge**.

The project demonstrates how agentic AI and production observability can work together to help film crews make faster, more informed operational decisions.

---

## 📄 License

This project is open source. See the `LICENSE` file for details.