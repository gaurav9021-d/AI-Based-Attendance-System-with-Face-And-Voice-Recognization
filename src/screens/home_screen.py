import streamlit as st
from src.components.header import header_home

from src.ui.base_layout import style_base_layout, style_background_home
from src.database.config import is_supabase_configured

def home_screen():


    header_home()
    style_background_home()
    style_base_layout()

    if is_supabase_configured:
        st.success("🟢 **Connected to Supabase Cloud Database**")
    else:
        st.info("🟢 **Local Database Ready**: All features (Teacher & Student registration, Face AI Attendance, Subjects) are fully functional offline! Default Teacher: **teacher** / **password123**")
        with st.expander("☁️ **Connect to Supabase Cloud (Optional)**", expanded=False):
            st.markdown("""
            To sync with Supabase Cloud instead of local database:
            1. Create a project at **[supabase.com](https://supabase.com)**.
            2. Run `supabase_schema.sql` in the **Supabase SQL Editor**.
            3. Paste your credentials into `.streamlit/secrets.toml`:
            ```toml
            SUPABASE_URL = "https://your-project.supabase.co"
            SUPABASE_KEY = "your-anon-key"
            ```
            """)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()