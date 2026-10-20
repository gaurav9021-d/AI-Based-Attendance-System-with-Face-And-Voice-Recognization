import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.database.config import is_supabase_configured


def home_screen():
    style_background_home()
    style_base_layout()

    header_home()

    # Refined Minimalist Status Pill
    if is_supabase_configured:
        st.markdown("""
            <div style="display:flex; justify-content:center; margin-bottom:2rem;">
                <div style="background:rgba(255,255,255,0.9); border:1px solid rgba(16, 185, 129, 0.3); border-radius:9999px; padding:6px 18px; font-size:0.85rem; font-weight:600; color:#065f46; display:inline-flex; align-items:center; gap:8px; box-shadow:0 4px 12px rgba(16, 185, 129, 0.08);">
                    <span style="width:7px; height:7px; background:#10b981; border-radius:50%; box-shadow:0 0 8px #10b981;"></span>
                    <span>cloud database synchronized</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="display:flex; justify-content:center; margin-bottom:2rem;">
                <div style="background:rgba(255,255,255,0.9); border:1px solid rgba(15, 23, 42, 0.09); border-radius:9999px; padding:6px 18px; font-size:0.85rem; font-weight:600; color:#334155; display:inline-flex; align-items:center; gap:8px; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
                    <span style="width:7px; height:7px; background:#10b981; border-radius:50%; box-shadow:0 0 8px #10b981;"></span>
                    <span>local database ready & fully functional</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Sofi Health inspired split cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="margin-bottom:0.2rem;">
                <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748b;">attendee</span>
                <h2 style="font-size:2.2rem; font-weight:800; color:#0b0f19; margin:4px 0 6px 0; letter-spacing:-0.04em;">i'm a student</h2>
                <p style="font-size:0.92rem; color:#64748b; margin:0 0 0.8rem 0;">instant faceid check-in & enrolled courses</p>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=140)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button('enter student portal →', type='primary', key='btn_student_portal', width='stretch'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
            <div style="margin-bottom:0.2rem;">
                <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748b;">instructor</span>
                <h2 style="font-size:2.2rem; font-weight:800; color:#0b0f19; margin:4px 0 6px 0; letter-spacing:-0.04em;">i'm an educator</h2>
                <p style="font-size:0.92rem; color:#64748b; margin:0 0 0.8rem 0;">ai roll call, qr codes & attendance logs</p>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=155)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button('enter teacher portal →', type='primary', key='btn_teacher_portal', width='stretch'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # Sofi Health editorial footer ticker
    st.markdown("""
        <div class="sofi-ticker">
            <span>neural face recognition</span>
            <span class="sofi-ticker-dot"></span>
            <span>ambient voice diarization</span>
            <span class="sofi-ticker-dot"></span>
            <span>instant qr enrollment</span>
            <span class="sofi-ticker-dot"></span>
            <span>zero manual roll calls</span>
        </div>
    """, unsafe_allow_html=True)