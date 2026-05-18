# Up-Mate

Keep your mate up to date. This project was born out of a period of time when I was dealing with severe headaches and 

## Overview

Up-Mate lets you and your circle of friends or family easily check in with each other. Share how you're doing, your current pain level, notes about what you're up to, and stay connected without the overhead of long messages or calls.

## Features

- **Quick Status Updates** – Share your current status with just a few clicks
- **Pain Level Tracking** – Report how you're feeling on a scale
- **Group Notifications** – Get notified when someone in your circle updates their status

:warning: Authentication not implemented :warning:
Since the purpose of this is to share information between close mates, and that this is best run in a homelab (where it is not accessible to the broader internet), there is no authentication implemented.

## Tech Stack

- **Backend**: Python/Flask
- **Notifications**: (optional) [ntfy](https://ntfy.sh)
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose
- **Server**: uWSGI with Nginx proxy
- **Frontend**: HTML/Bootstrap

## Quick Start

### Prerequisites

- Docker & Docker Compose
- `.env` file configured (see `.env.example` for examples)

### Running Locally

```bash
cd hosting
docker compose up
```

The app will be available at `http://localhost:9090` (or your configured `BACKEND_PORT`).

## Configuration

Configure via environment variables in `.env`:

- `DOMAIN` – Domain name for containers
- `BACKEND_PORT` – Port to expose backend on (default: 9090)
- Database and user credentials (set in `docker-compose.yml` env_file)

## Status Message Format

Each status update includes:

- **user** – Username
- **pain_level** – Numeric pain level (0–10)
- **notes** – Optional notes about what you're up to
- **color_level** – Visual indicator level (0–?)

## Development

To work on the backend locally:

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
poetry install
python -m up_mate_backend
```
