# Momentum v2.2 - Deployment Ready

## Purpose

This version prepares Momentum for clean online deployment.

## Added

- Stable `data/` folder
- SQLite moved to `data/momentum.db`
- `backups/` folder
- One-click database backup in Settings
- Database location shown in Settings
- Latest backup shown in Settings
- `.gitignore`
- `.streamlit/config.toml`
- Deployment checklist

## Preserved

- Premium dashboard
- Program Manager
- Program Editor
- Workout logging
- Workout editing
- Bodyweight Log
- Bodyweight Trend
- Personal Records
- Momentum Score
- Smart Progression
- Export / Backup

## Run

```powershell
py -m streamlit run app.py --server.port 8522
```
