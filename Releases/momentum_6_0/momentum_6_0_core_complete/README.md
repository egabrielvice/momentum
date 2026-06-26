# Momentum 6.0 - Core Complete

## Status
Core training app complete.

## Included
- Premium dashboard
- Sidebar visual upgrade
- Workout experience polish
- Progress Hub polish
- Analytics polish
- Program Manager and Program Editor preserved
- Export / Backup preserved
- Login preserved
- Database compatibility helpers included

## Excluded Intentionally
- Health / macros / nutrition module
- AI coach

These should be added later as separate modules.

## Replace These Files
- app.py
- database.py

## Keep Existing
- data/
- backups/
- .streamlit/

## Run Locally
```powershell
cd "C:\Users\escar\OneDrive\Apps\Momentum\Development\momentum_dev"
py -m streamlit run app.py --server.port 8560
```

## After Testing
If every page works:
1. Upload `app.py` and `database.py` to GitHub.
2. Let Streamlit redeploy.
3. Copy `momentum_dev` into Releases as `momentum_6_0`.
