import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            /* Sofi Health inspired luminous canvas with ambient gradient glows */
            .stApp {
                background: #fbfbfa !important;
                background-image: 
                    radial-gradient(circle at 10% 15%, rgba(199, 210, 254, 0.45) 0%, transparent 45%),
                    radial-gradient(circle at 90% 10%, rgba(224, 231, 255, 0.55) 0%, transparent 40%),
                    radial-gradient(circle at 50% 85%, rgba(243, 232, 255, 0.4) 0%, transparent 50%) !important;
                background-attachment: fixed !important;
                overflow-x: hidden !important;
            }

            /* Glassmorphic role selection cards with smooth entrance */
            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(24px) !important;
                -webkit-backdrop-filter: blur(24px) !important;
                padding: 3rem 2.2rem !important;
                border-radius: 2rem !important;
                border: 1px solid rgba(15, 23, 42, 0.07) !important;
                box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03) !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
                animation: fadeSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both !important;
                text-align: center !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-6px) !important;
                box-shadow: 0 30px 60px -20px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(15, 23, 42, 0.1) !important;
                background: rgba(255, 255, 255, 0.95) !important;
            }

            .stApp div[data-testid="stColumn"] img {
                animation: floatSlow 5s ease-in-out infinite !important;
                margin: 1.5rem auto !important;
                filter: drop-shadow(0 15px 25px rgba(0,0,0,0.08)) !important;
                transition: transform 0.4s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover img {
                transform: scale(1.06) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #fbfbfa !important;
                background-image: 
                    radial-gradient(circle at 100% 0%, rgba(224, 231, 255, 0.45) 0%, transparent 45%),
                    radial-gradient(circle at 0% 100%, rgba(243, 232, 255, 0.35) 0%, transparent 50%) !important;
                background-attachment: fixed !important;
            }

            /* Dashboard elevated containers */
            div[data-testid="stContainer"] {
                border-radius: 1.5rem !important;
                border: 1px solid rgba(15, 23, 42, 0.07) !important;
                background: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(16px) !important;
                box-shadow: 0 12px 30px -10px rgba(0,0,0,0.04) !important;
                animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

            /* Animations inspired by Sofi Health & GSAP smooth motion */
            @keyframes fadeSlideUp {
                0% {
                    opacity: 0;
                    transform: translateY(24px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes floatSlow {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-8px);
                }
            }

            @keyframes pulseGlow {
                0%, 100% {
                    opacity: 0.6;
                }
                50% {
                    opacity: 1;
                }
            }

            /* Hide Streamlit default header/footer chrome */
            #MainMenu, footer, header {
                visibility: hidden;
                display: none;
            }

            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 1100px !important;
                animation: fadeSlideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) both !important;
            }

            /* Sofi Health Editorial Lowercase Typography */
            h1, h2, h3, h4, p, span, div, button {
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
                letter-spacing: -0.025em !important;
            }

            h1 {
                font-weight: 800 !important;
                font-size: 3.4rem !important;
                line-height: 1.05 !important;
                color: #0b0f19 !important;
                letter-spacing: -0.045em !important;
                margin-bottom: 0.5rem !important;
            }

            h2 {
                font-weight: 700 !important;
                font-size: 2rem !important;
                line-height: 1.15 !important;
                color: #0b0f19 !important;
                letter-spacing: -0.035em !important;
                margin-bottom: 0.5rem !important;
            }

            h3 {
                font-weight: 600 !important;
                font-size: 1.35rem !important;
                color: #1e293b !important;
            }

            p {
                color: #475569 !important;
                font-size: 1.02rem !important;
                line-height: 1.6 !important;
            }

            /* Sofi Health Signature Obsidian Pill Buttons */
            button {
                border-radius: 9999px !important;
                background-color: #0a0a0c !important;
                color: #ffffff !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 12px 28px !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                letter-spacing: -0.01em !important;
                cursor: pointer !important;
            }

            button:hover {
                transform: translateY(-2px) scale(1.02) !important;
                background-color: #18181b !important;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
            }

            button:active {
                transform: translateY(0) scale(0.99) !important;
            }

            /* Secondary Pill Buttons (Refined Mauve Accent) */
            button[kind="secondary"] {
                border-radius: 9999px !important;
                background-color: #f1f5f9 !important;
                color: #0f172a !important;
                border: 1px solid rgba(15, 23, 42, 0.12) !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
            }

            button[kind="secondary"]:hover {
                background-color: #e2e8f0 !important;
                color: #000000 !important;
                transform: translateY(-2px) scale(1.02) !important;
            }

            /* Tertiary Pill Buttons */
            button[kind="tertiary"] {
                border-radius: 9999px !important;
                background-color: #ffffff !important;
                color: #475569 !important;
                border: 1px solid rgba(15, 23, 42, 0.1) !important;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
            }

            button[kind="tertiary"]:hover {
                background-color: #f8fafc !important;
                color: #0f172a !important;
                border-color: rgba(15, 23, 42, 0.2) !important;
            }

            /* Form Input Polish */
            input, select, textarea {
                border-radius: 14px !important;
                border: 1px solid rgba(15, 23, 42, 0.12) !important;
                background-color: #ffffff !important;
                padding: 12px 18px !important;
                font-size: 0.98rem !important;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
                color: #0f172a !important;
            }

            input:focus, select:focus, textarea:focus {
                border-color: #0a0a0c !important;
                box-shadow: 0 0 0 3px rgba(10, 10, 12, 0.08) !important;
                outline: none !important;
            }

            /* Streamlit Modal/Dialog Polish (Sofi style rounded glass) */
            div[data-testid="stModal"] > div {
                border-radius: 28px !important;
                border: 1px solid rgba(15, 23, 42, 0.08) !important;
                background: rgba(255, 255, 255, 0.96) !important;
                backdrop-filter: blur(28px) !important;
                box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.2) !important;
                padding: 2.2rem !important;
                animation: fadeSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both !important;
            }

            /* File Uploader & Camera Input Polish */
            div[data-testid="stFileUploader"] section {
                border-radius: 20px !important;
                border: 2px dashed rgba(15, 23, 42, 0.15) !important;
                background: rgba(255, 255, 255, 0.6) !important;
                transition: all 0.3s ease !important;
            }

            div[data-testid="stFileUploader"] section:hover {
                border-color: #0a0a0c !important;
                background: rgba(255, 255, 255, 0.95) !important;
            }

            div[data-testid="stCameraInput"] {
                border-radius: 22px !important;
                overflow: hidden !important;
                border: 1px solid rgba(15, 23, 42, 0.1) !important;
                box-shadow: 0 10px 30px -10px rgba(0,0,0,0.06) !important;
            }

            /* Dataframe / Table Polish */
            div[data-testid="stDataFrame"] {
                border-radius: 18px !important;
                overflow: hidden !important;
                border: 1px solid rgba(15, 23, 42, 0.08) !important;
                box-shadow: 0 8px 24px -10px rgba(0, 0, 0, 0.04) !important;
            }

            /* Refined Notification Pills */
            div[data-testid="stAlert"] {
                border-radius: 16px !important;
                border: 1px solid rgba(15, 23, 42, 0.08) !important;
                backdrop-filter: blur(12px) !important;
                padding: 14px 20px !important;
                font-weight: 500 !important;
            }

            /* Expander Polish */
            div[data-testid="stExpander"] {
                border-radius: 18px !important;
                border: 1px solid rgba(15, 23, 42, 0.08) !important;
                background: rgba(255, 255, 255, 0.75) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
                margin-bottom: 1.5rem !important;
            }

            /* Custom Sofi style footer ticker */
            .sofi-ticker {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 16px;
                margin-top: 3.5rem;
                padding-top: 1.5rem;
                border-top: 1px solid rgba(15, 23, 42, 0.07);
                color: #64748b;
                font-size: 0.88rem;
                letter-spacing: -0.01em;
                animation: fadeSlideUp 1s ease both;
                flex-wrap: wrap;
            }

            .sofi-ticker span {
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            .sofi-ticker-dot {
                width: 4px;
                height: 4px;
                background: #94a3b8;
                border-radius: 50%;
            }
        </style>
    """, unsafe_allow_html=True)