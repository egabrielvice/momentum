# Momentum

Momentum is a private training operating system built for long-term workout tracking, progressive overload, analytics, and personal training history.

## Current Structure

- `App/` — stable daily app
- `Data/` — lifetime database and backups
- `Development/` — experimental development work
- `Releases/` — stable milestone snapshots
- `Docs/` — documentation
- `Assets/` — future images, icons, and design files

## Run Momentum

```powershell
cd "C:\Users\escar\OneDrive\Apps\Momentum\App"
py -m streamlit run app.py --server.port 8550

# Password

Default local development password:

```text
momentum
```

If deploying publicly in the future, set the `APP_PASSWORD` secret instead of using the default password.