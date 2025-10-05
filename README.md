# Simple Flask Wiki

This is a minimal wiki built with Flask and SQLite.  
Features:
- View pages
- Edit/create pages (anyone can edit)
- SQLite database (wiki.db) auto-created on first run
- Ready to deploy on Render (render.yaml included)

To run locally:
```
pip install -r requirements.txt
python app.py
```

On Render, it will use the $PORT environment variable.
