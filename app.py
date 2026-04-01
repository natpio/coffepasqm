import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# --- 1. KONFIGURACJA BEZPIECZEŃSTWA I STRONY ---
st.set_page_config(
    page_title="SQM BI - System Kontroli Zasobów",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ukrycie standardowych elementów Streamlit dla zachowania profesjonalnego wyglądu
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. MECHANIZM AUTORYZACJI GITHUB-SAFE ---
# Na GitHubie w pliku .streamlit/secrets.toml ustawiasz: 
# ACCESS_KEY = "twoje_haslo"
# IMG_NAME = "sqm.jpg"

def check_password():
    """Zwraca True, jeśli użytkownik podał poprawne hasło dostępu do systemu."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("SQM BUSINESS INTELLIGENCE")
        password = st.text_input("KLUCZ DOSTĘPU DO SYSTEMU LOGISTYKI:", type="password")
        if st.button("AUTORYZUJ"):
            # Używamy st.secrets dla bezpieczeństwa (nie widać hasła w kodzie)
            try:
                if password == st.secrets["ACCESS_KEY"]:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("NIEAUTORYZOWANA PRÓBA DOSTĘPU. INCYDENT ZAPISANO.")
            except:
                # Fallback jeśli nie skonfigurowano secrets
                if password == "SQM2026": 
                    st.session_state["authenticated"] = True
                    st.rerun()
        return False
    return True

if check_password():
    # --- 3. ŁADOWANIE TŁA (ZABEZPIECZONE) ---
    def get_base64_of_bin_file(bin_file):
        try:
            if os.path.exists(bin_file):
                with open(bin_file, 'rb') as f:
                    data = f.read()
                return base64.b64encode(data).decode()
        except Exception:
            return None
        return None

    # Pobieranie nazwy obrazu z sekretów lub domyślnej
    img_name = st.secrets.get("IMG_NAME", "sqm.jpg")
    bin_str = get_base64_of_bin_file(img_name)

    if bin_str:
        bg_img_style = f"""
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        """
    else:
        bg_img_style = "background-color: #050505;"

    # --- 4. CUSTOM CSS (STRICT SQM STYLE) ---
    st.markdown(f"""
        <style>
        .stApp {{
            {bg_img_style}
        }}
        
        .stApp .block-container {{
            background-color: rgba(0, 0, 0, 0.92);
            padding: 3rem;
            border-radius: 15px;
            margin-top: 30px;
            border: 1px solid rgba(255, 75, 75, 0.2);
            box-shadow: 0px 20px 60px rgba(0,0,0,1);
        }}

        h1, h2, h3 {{
            color: #ffffff !important;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 900 !important;
        }}
        
        label, .stMarkdown p {{
            color: #cccccc !important;
            font-weight: 400 !important;
            text-transform: uppercase;
            font-size: 0.85rem;
        }}

        .stTextInput input {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #ff4b4b !important;
            font-weight: bold !important;
        }}

        div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 2px solid #ff4b4b !important;
        }}
        
        div[data-baseweb="select"] * {{
            color: #000000 !important;
            font-weight: bold !important;
        }}

        .stButton>button {{
            width: 100%;
            background-color: transparent;
            color: #ffffff !important;
            border: 2px solid #ff4b4b !important;
            font-weight: 900;
            height: 4em;
            text-transform: uppercase;
            transition: all 0.4s ease;
        }}
        
        .stButton>button:hover {{
            background-color: #ff4b4b !important;
            color: white !important;
            box-shadow: 0px 0px 40px rgba(255, 75, 75, 0.6);
        }}

        .stAlert {{
            background-color: rgba(60, 0, 0, 0.9) !important;
            border: 1px solid #ff4b4b !important;
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # --- 5. INTERFEJS GŁÓWNY ---
    col_logo, col_nav = st.columns([1, 4])
    with col_logo:
        st.markdown("<h2 style='margin:0; color: white;'>SQM</h2>", unsafe_allow_html=True)
    with col_nav:
        st.write("<p style='text-align: right; color: #555; font-size: 13px; letter-spacing: 1px;'>LOGISTICS CONTROL &bull; MARGIN PROTECTION &bull; INTERNAL USE ONLY</p>", unsafe_allow_html=True)

    st.title("PORTAL ZARZĄDZANIA KOFEINĄ")
    st.markdown("<p style='color: #ff4b4b; font-weight: bold; letter-spacing: 2px; margin-top: -15px;'>ANALIZA RENTOWNOŚCI PROJEKTU v9.9.2</p>", unsafe_allow_html=True)
    st.write("---")

    # UKŁAD
    c1, c2, c3 = st.columns([1, 1.2, 1.2])

    with c1:
        st.markdown("### AUTORYZACJA")
        p_id = st.text_input("NR PROJEKTU (5 CYFR):", max_chars=5, placeholder="4XXXX")
        l_name = st.text_input("NAZWISKO PRACOWNIKA:", placeholder="KOWALSKI")
        
        drink = st.selectbox("ZASÓB DO WYDANIA:", [
            "Espresso (Próg: >15%)", 
            "Double Espresso (Próg: >28.5%)", 
            "Flat White (Zarząd / VIP)",
            "Woda (Standard)"
        ])
        
        st.write("")
        btn = st.button("WERYFIKUJ RENTOWNOŚĆ")

    with c2:
        st.markdown("### REALNA STRUKTURA KOSZTÓW")
        # Dane odzwierciedlające Twoją pracę w logistyce (transport/naczepy)
        labels = ['Transport & Slot-in', 'Przestoje (Demurrage)', 'Ekipa Techniczna', 'Sprzęt AV', 'ZYSK (MARŻA)']
        values = [52, 18, 15, 14.2, 0.8] 
        colors = ['#0a0a0a', '#1a1a1a', '#2a2a2a', '#3a3a3a', '#ff4b4b']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
        fig.update_layout(
            showlegend=True,
            legend=dict(font=dict(color="white")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0, l=0, r=0),
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        if btn:
            if not p_id or len(p_id) < 5 or not l_name:
                st.error("BŁĄD: NIEKOMPLETNE DANE AUTORYZACYJNE.")
            else:
                with st.status("POBIERANIE DANYCH Z SYSTEMU ERP...", expanded=True) as status:
                    time.sleep(0.8)
                    st.write(f"Analizowanie projektu SQM #{p_id}...")
                    time.sleep(1.2)
                    st.write("Weryfikacja slotów rozładunkowych i czasu pracy naczep...")
                    time.sleep(0.7)
                    status.update(label="KRYTYCZNIE NISKA RENTOWNOŚĆ", state="error")
                
                st.markdown(f"""
                    <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 10px; background-color: rgba(30,0,0,0.95); box-shadow: 0 0 30px rgba(255,75,75,0.3);">
                        <h2 style="color: #ff4b4b !important; margin-top:0; font-size: 24px;">❌ ODMOWA WYDANIA</h2>
                        <p style="color: white !important; font-size: 16px;">Użytkownik: <b>{l_name.upper()}</b></p>
                        <p style="font-size: 14px; color: #ddd !important; line-height: 1.6;">
                            <b>Status:</b> Zasób <b>{drink}</b> zablokowany.<br>
                            Obecna marża (0.8%) nie pokrywa kosztów logistycznych (przekroczenie budżetu na transport o 115%).
                        </p>
                        <hr style="border-color: #444;">
                        <p style="font-size: 11px; color: #888 !important; font-style: italic;">
                            System wykrył nieplanowane przestoje naczep. Proszę wrócić do optymalizacji slotów transportowych przed ponowną próbą.
                        </p>
                        <p style="color: #ff4b4b !important; font-weight: 900; font-size: 16px; margin-top: 15px; text-align: center; letter-spacing: 2px;">
                            WSZYSTKO DLA FIRMY.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    # --- 6. STOPKA ---
    st.markdown("""
        <div style="margin-top: 60px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 40px;">
            <h1 style="font-size: clamp(40px, 8vw, 90px); line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
                NO <span style="color: #ff4b4b !important;">MARGIN</span>.
            </h1>
            <h1 style="font-size: clamp(40px, 8vw, 90px); line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
                NO <span style="color: #ff4b4b !important;">COFFEE</span>.
            </h1>
            <h1 style="font-size: clamp(40px, 8vw, 90px); line-height: 0.85; color: #ff4b4b !important; margin: 0; font-weight: 900;">
                ALL FOR THE <span style="color: white !important;">COMPANY</span>.
            </h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("<p style='color: #444; font-size: 11px;'>&copy; 2026 SQM Multimedia Solutions | Logistics Department Security Protocol</p>", unsafe_allow_html=True)
    with f2:
        if st.toggle("TRYB SERWISOWY (DLA ZARZĄDU)"):
            st.balloons()
            st.success(f"Dobrej kawy, {l_name}! System odblokowany.")
