# Momentum

Momentum is a private training operating system built for long-term workout tracking, progressive overload, analytics, and personal training history.

## Current Structure

- `App/` — stable daily app
- `Data/` — lifetime database and backups
- `Development/` — experimental development work
- `Releases/` — stable milestone snapshots
- `Docs/` — documentation

## Run Momentum

```powershell
cd App
py -m streamlit run app.py
```

## Authentication

Momentum uses the `APP_PASSWORD` secret for authentication when deployed.

For local development, configure the password through environment variables or Streamlit secrets rather than hardcoding credentials.
