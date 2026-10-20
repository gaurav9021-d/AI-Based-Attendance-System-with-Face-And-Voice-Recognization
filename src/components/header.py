import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:1.2rem; margin-top:0.2rem; text-align:center;">
            <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(255, 255, 255, 0.85); border:1px solid rgba(15, 23, 42, 0.08); padding:5px 16px; border-radius:9999px; margin-bottom:0.8rem; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <span style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981;"></span>
                <span style="font-size:0.82rem; font-weight:600; color:#334155; letter-spacing:-0.01em;">intelligent vision & voice roll call</span>
            </div>
            <div style="display:flex; align-items:center; gap:14px;">
                <img src='{logo_url}' style='height:64px; border-radius:16px; filter:drop-shadow(0 6px 14px rgba(0,0,0,0.08));' />
                <h1 style='font-size:3.6rem; font-weight:800; letter-spacing:-0.05em; color:#0b0f19; margin:0; line-height:1;'>snapclass</h1>
            </div>
            <p style="font-size:1.05rem; color:#64748b; max-width:520px; margin-top:0.6rem; margin-bottom:0; font-weight:400; line-height:1.45;">
                seamless biometric attendance for modern classrooms—powered by real-time neural vision and voice recognition
            </p>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:1rem;">
            <img src='{logo_url}' style='height:52px; border-radius:14px; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.06));' />
            <div>
                <h2 style='font-size:1.85rem; font-weight:800; letter-spacing:-0.04em; color:#0b0f19; margin:0; line-height:1;'>snapclass</h2>
                <span style="font-size:0.82rem; font-weight:500; color:#64748b; letter-spacing:-0.01em;">ai attendance workspace</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
