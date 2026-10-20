import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="
            background: #ffffff; 
            border: 1px solid rgba(15, 23, 42, 0.08); 
            border-radius: 24px; 
            padding: 26px 28px; 
            margin-bottom: 22px; 
            box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.04);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        ">
            <div style="position:absolute; top:0; left:0; width:5px; height:100%; background:linear-gradient(180deg, #6366f1 0%, #a855f7 100%);"></div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:8px;">
                <h3 style="margin:0; color:#0f172a; font-size:1.35rem; font-weight:700; letter-spacing:-0.03em;">{name}</h3>
                <span style="background:#0f172a; color:#ffffff; font-size:0.75rem; font-weight:700; padding:4px 10px; border-radius:9999px; letter-spacing:0.02em;">SECTION {section}</span>
            </div>
            <p style="color:#64748b; font-size:0.9rem; margin:0 0 16px 0; font-weight:500;">
                Course Code : <span style="background:#f1f5f9; color:#0f172a; padding:3px 8px; border-radius:8px; font-family:monospace; font-weight:600;">{code}</span>
            </p>
    """

    if stats:
        html += """
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
        """
        for icon, label, value in stats:
            html += f"""
                <div style="
                    background: #f8fafc; 
                    border: 1px solid rgba(15, 23, 42, 0.06); 
                    padding: 6px 14px; 
                    border-radius: 9999px; 
                    font-size: 0.85rem; 
                    color: #334155; 
                    display: inline-flex; 
                    align-items: center; 
                    gap: 6px;
                ">
                    <span>{icon}</span> 
                    <span style="font-weight:700; color:#0f172a;">{value}</span> 
                    <span style="color:#64748b;">{label}</span>
                </div>
            """
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
