"""
Session persistence across browser refreshes using URL query parameters.

Strategy:
  - On login  : write  ?role=teacher&uid=2  into the URL (st.query_params).
  - On load   : if session_state is empty but query params carry a valid
                role+uid, re-fetch the user from the DB and restore state.
  - On logout : clear the query params.

This is entirely server-side — no JavaScript required.
"""

import streamlit as st


# ── Write ──────────────────────────────────────────────────────────────────────

def save_session(role: str, user_id: int):
    """Persist login to URL query params."""
    st.query_params["role"] = role
    st.query_params["uid"]  = str(user_id)


def clear_session():
    """Remove session from URL query params."""
    st.query_params.clear()


# ── Restore ────────────────────────────────────────────────────────────────────

def restore_session():
    """
    Call once at the top of app.py before routing.
    If session_state has no active login but the URL carries valid params,
    re-fetches the user from the DB and restores the session.
    """
    # Already logged in — nothing to do.
    if st.session_state.get("login_type"):
        return

    role    = st.query_params.get("role", "")
    uid_str = st.query_params.get("uid",  "")

    if not role or not uid_str:
        return

    try:
        user_id = int(uid_str)
    except ValueError:
        clear_session()
        return

    if role == "teacher":
        _restore_teacher(user_id)
    elif role == "student":
        _restore_student(user_id)
    else:
        clear_session()


def _restore_teacher(teacher_id: int):
    from src.database.config import supabase
    try:
        res = supabase.table("teachers").select("*").eq("teacher_id", teacher_id).execute()
        if res.data:
            teacher = res.data[0]
            st.session_state["login_type"]   = "teacher"
            st.session_state["teacher_data"] = teacher
            st.session_state["is_logged_in"] = True
            st.session_state["user_role"]    = "teacher"
            st.rerun()
        else:
            clear_session()
    except Exception:
        clear_session()


def _restore_student(student_id: int):
    from src.database.config import supabase
    try:
        res = supabase.table("students").select("*").eq("student_id", student_id).execute()
        if res.data:
            student = res.data[0]
            st.session_state["login_type"]   = "student"
            st.session_state["student_data"] = student
            st.session_state["is_logged_in"] = True
            st.session_state["user_role"]    = "student"
            st.rerun()
        else:
            clear_session()
    except Exception:
        clear_session()
