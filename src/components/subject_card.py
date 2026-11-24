import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    with st.container(border=True):
        # Header row: name + section badge
        h_col, badge_col = st.columns([4, 1], vertical_alignment='center')
        with h_col:
            st.markdown(
                f"<h3 style='margin:0; color:#0f172a; font-size:1.2rem; font-weight:700; "
                f"letter-spacing:-0.02em;'>{name}</h3>",
                unsafe_allow_html=True,
            )
        with badge_col:
            st.markdown(
                f"<div style='text-align:right;'>"
                f"<span style='background:#0f172a; color:#fff; font-size:0.7rem; font-weight:700; "
                f"padding:3px 8px; border-radius:9999px; letter-spacing:0.04em;'>SECTION {section}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Course code
        st.markdown(
            f"<p style='color:#64748b; font-size:0.88rem; margin:4px 0 10px 0; font-weight:500;'>"
            f"Course Code: "
            f"<code style='background:#f1f5f9; color:#0f172a; padding:2px 6px; border-radius:6px; "
            f"font-weight:600;'>{code}</code></p>",
            unsafe_allow_html=True,
        )

        # Stats pills
        if stats:
            pill_parts = []
            for icon, label, value in stats:
                pill_parts.append(
                    f"<span style='background:#f8fafc; border:1px solid rgba(15,23,42,0.08); "
                    f"padding:4px 12px; border-radius:9999px; font-size:0.82rem; color:#334155; "
                    f"display:inline-flex; align-items:center; gap:5px; margin-right:6px;'>"
                    f"{icon} <b style='color:#0f172a;'>{value}</b> {label}</span>"
                )
            st.markdown(
                "<div style='margin-bottom:8px;'>" + "".join(pill_parts) + "</div>",
                unsafe_allow_html=True,
            )

        # Footer button(s) rendered via callback
        if footer_callback:
            footer_callback()
