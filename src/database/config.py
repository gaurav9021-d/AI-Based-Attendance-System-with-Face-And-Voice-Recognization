import streamlit as st
from supabase import create_client, Client
import tomllib
from pathlib import Path

supabase: Client = None
is_supabase_configured = False

url = ""
key = ""

# 1. Try reading from st.secrets safely
try:
    if hasattr(st, "secrets") and "SUPABASE_URL" in st.secrets:
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
except Exception:
    pass

# 2. Try reading directly from secrets.toml files in project hierarchy
if not url or not key:
    search_dirs = [
        Path.cwd(),
        Path.cwd() / ".streamlit",
        Path(__file__).resolve().parent.parent.parent,
        Path(__file__).resolve().parent.parent.parent / ".streamlit",
        Path(__file__).resolve().parent.parent.parent.parent,
        Path(__file__).resolve().parent.parent.parent.parent / ".streamlit",
    ]
    for directory in search_dirs:
        for filename in ["secrets.toml", ".streamlit/secrets.toml"]:
            candidate = directory / filename
            if candidate.is_file():
                try:
                    with open(candidate, "rb") as f:
                        data = tomllib.load(f)
                        u = data.get("SUPABASE_URL", "")
                        k = data.get("SUPABASE_KEY", "")
                        if u and k:
                            url, key = u, k
                            break
                except Exception:
                    pass
        if url and key:
            break

from src.database.sqlite_db import SQLiteClient, init_sqlite_db

init_sqlite_db()

if url and key and "your-project" not in url and "placeholder" not in url:
    try:
        supabase = create_client(url, key)
        # Verify connection
        supabase.table("teachers").select("teacher_id").limit(1).execute()
        is_supabase_configured = True
    except Exception:
        supabase = SQLiteClient()
        is_supabase_configured = False
else:
    supabase = SQLiteClient()
    is_supabase_configured = False