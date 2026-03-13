# should-i-watch-the-game

Minimal Python notifier that checks if a team won and emails a "you should watch" alert every 4 hours.

## Features (v1)
- Leagues: **NHL**, **Bundesliga**.
- Modular providers (`winwatch/providers/*`) for easy league expansion.
- SMTP email notification.
- Docker + local Python + AWS Lambda run modes.

## Quick start
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Fill `.env` values.
3. Run with Docker:
   ```bash
   docker compose up -d --build
   ```

### Local Unix run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
set -a && source .env && set +a
python -m winwatch.main
```

## AWS Lambda mode
Use handler: `winwatch.lambda_handler.handler`

- The core logic is unchanged (`run_once` / providers / notifier) and reused by Lambda.
- When running in Lambda, config loading checks `LAMBDA_*` env vars first, then falls back to base env names.
- Schedule with EventBridge: `rate(4 hours)`.

## How it works
```mermaid
flowchart TD
    A[Trigger] --> B{Runtime}
    B -->|EC2/K8s/Container| C[run_forever sleep 4h]
    B -->|Lambda + EventBridge| D[run_once every 4h]
    C --> E[Load env config]
    D --> E
    E --> F{League provider}
    F -->|NHL| G[Call NHL score API]
    F -->|Bundesliga| H[Call OpenLigaDB API]
    G --> I[Latest completed game]
    H --> I
    I --> J{Team won?}
    J -->|No| K[Exit or sleep]
    J -->|Yes| L[Send SMTP email]
    L --> K
```

## Extension points
- Add a new league provider implementing `LeagueProvider.latest_result`.
- Add qualifiers (OT, playoffs) inside provider payload parsing or a future rule engine.
- Add frontend + SMS as independent modules calling the same service layer.

## Notes
- Current Bundesliga lookup scans recent matchdays and returns the latest finished match found for the target team.
- For cloud use, run the same container on any scheduler (ECS, Kubernetes CronJob, VPS with Docker), or run Lambda on EventBridge.
