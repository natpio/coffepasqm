import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="SQM BI - Portal Zarządzania Kofeiną",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNKCJA ŁADOWANIA TŁA (BASE64) ---
def get_base64_of_bin_file(bin_file):
    try:
        if os.path.exists(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except:
        return None
    return None

# Przygotowanie tła ze zdjęcia sqm.jpg
img_path = 'sqm.jpg'
bin_str = get_base64_of_bin_file(img_path)

if bin_str:
    bg_img_style = f"""
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    """
else:
    bg_img_style = "background-color: #000000;"

# --- CUSTOM CSS (BIAŁE NAGŁÓWKI + CZARNY TEKST W POLACH) ---
st.markdown(f"""
    <style>
    .stApp {{
        {bg_img_style}
    }}
    
    /* Główny kontener treści */
    .stApp .block-container {{
        background-color: rgba(0, 0, 0, 0.88);
        padding: 3rem;
        border-radius: 20px;
        margin-top: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0px 10px 40px rgba(0,0,0,0.9);
    }}

    /* Białe nagłówki H1, H2, H3 */
    h1, h2, h3 {{
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 900 !important;
    }}
    
    /* Etykiety nad polami */
    label, .stMarkdown p {{
        color: #ffffff !important;
        font-weight: 600 !important;
    }}

    /* POPRAWKA: Czarna czcionka wewnątrz białych pól wpisywania */
    .stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ff4b4b !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}

    /* Stylizacja listy rozwijanej (Selectbox) */
    div[data-baseweb="select"] {{
        background-color: #ffffff !important;
        border-radius: 4px;
    }}
    
    div[data-baseweb="select"] * {{
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* Przycisk SQM Style */
    .stButton>button {{
        width: 100%;
        background-color: transparent;
        color: #ffffff !important;
        border: 2px solid #ff4b4b !important;
        font-weight: bold;
        height: 3.8em;
        text-transform: uppercase;
        transition: 0.4s;
        margin-top: 10px;
    }}
    
    .stButton>button:hover {{
        background-color: #ff4b4b !important;
        color: white !important;
        box-shadow: 0px 0px 30px rgba(255, 75, 75, 1);
    }}

    /* Komunikat o odmowie (Alert) */
    .stAlert {{
        background-color: rgba(50, 0, 0, 0.95) !important;
        border: 2px solid #ff4b4b !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- NAGŁÓWEK STRONY ---
col_logo, col_nav = st.columns([1, 4])
with col_logo:
    st.markdown("<h2 style='margin:0; color: white;'>SQM</h2>", unsafe_allow_html=True)
with col_nav:
    st.write("<p style='text-align: right; color: #999; font-size: 13px;'>O NAS &nbsp;&nbsp; REALIZACJE &nbsp;&nbsp; USŁUGI &nbsp;&nbsp; KONTAKT &nbsp;&nbsp; SQM ESPAÑA</p>", unsafe_allow_html=True)

st.title("SQM BI - Portal Zarządzania Kofeiną")
st.markdown("<p style='color: #ff4b4b; font-weight: bold; letter-spacing: 1px;'>LOGISTICS & MARGIN INTERLOCK SYSTEM v9.9.2</p>", unsafe_allow_html=True)
st.write("---")

# --- UKŁAD FORMULARZA I WYKRESU ---
c1, c2, c3 = st.columns([1, 1.3, 1.2])

with c1:
    st.markdown("### AUTORYZACJA")
    p_id = st.text_input("NUMER PROJEKTU SQM (5 CYFR):", max_chars=5, placeholder="np. 45210")
    l_name = st.text_input("NAZWISKO:", placeholder="Wpisz nazwisko")
    
    drink = st.selectbox("WYBIERZ ZASÓB:", [
        "Espresso (Wymagana marża >15%)", 
        "Double Espresso (Wymagana marża >28.5%)", 
        "Flat White (Tylko dla Zarządu)",
        "Woda z kranu (Standard)"
    ])
    
    st.write("")
    btn = st.button("WERYFIKUJ RENTOWNOŚĆ I WYDAJ KAWĘ")

with c2:
    st.markdown("### STRUKTURA KOSZTÓW")
    # Statyczne dane symulujące niski zysk
    labels = ['Transport', 'Magazyn', 'Ekipa', 'Sprzęt AV', 'Marża']
    values = [46, 17, 24, 12.2, 0.8] 
    colors = ['#111111', '#222222', '#333333', '#444444', '#ff4b4b']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
    fig.update_layout(
        showlegend=True,
        legend=dict(font=dict(color="white")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with c3:
    if btn:
        if not p_id or len(p_id) < 5 or not l_name:
            st.error("BŁĄD: Wprowadź poprawny numer projektu i nazwisko.")
        else:
            with st.status("POBIERANIE DANYCH Z SYSTEMU ERP...", expanded=True) as status:
                time.sleep(1.0)
                st.write(f"Analizowanie projektu #{p_id}...")
                time.sleep(1.5)
                st.write("Sprawdzanie kosztów naczep i slotów...")
                time.sleep(1.0)
                status.update(label="BŁĄD ANALIZY KOSZTÓW", state="error")
            
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 10px; background-color: rgba(40,0,0,0.9);">
                    <h2 style="color: #ff4b4b !important; margin-top:0; font-size: 22px;">❌ ODMOWA WYDANIA</h2>
                    <p style="color: white !important; font-size: 16px;">Użytkownik: <b>{l_name}</b></p>
                    <p style="font-size: 14px; color: #eee !important; line-height: 1.5;">
                        <b>Status:</b> Zasób <b>{drink}</b> jest zablokowany.<br>
                        Marża projektu (0.8%) nie pokrywa kosztu amortyzacji młynka.
                    </p>
                    <hr style="border-color: #555;">
                    <p style="font-size: 12px; color: #bbb !important;">
                        Logistyka zgłasza: Wykryto 115% przekroczenia budżetu na transport. 
                        Zaleca się spożycie wody w celu poprawy skupienia nad arkuszem kosztów.
                    </p>
                    <p style="color: #ff4b4b !important; font-weight: bold; font-size: 14px; margin-top: 15px;">
                        WSZYSTKO DLA FIRMY.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- DOLNY SLOGAN (ANGLIELSKI, BIAŁO-CZERWONY) ---
st.write("")
st.write("")
st.markdown("""
    <div style="margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px;">
        <h1 style="font-size: 80px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b !important;">MARGIN</span>.
        </h1>
        <h1 style="font-size: 80px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b !important;">COFFEE</span>.
        </h1>
        <h1 style="font-size: 80px; line-height: 0.85; color: #ff4b4b !important; margin: 0; font-weight: 900;">
            ALL FOR THE <span style="color: white !important;">COMPANY</span>.
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()
f1, f2 = st.columns(2)
with f1:
    st.markdown("<p style='color: #666; font-size: 11px;'>SQM Business Intelligence | Logistics Dept. Control | 2026-04-01</p>", unsafe_allow_html=True)
with f2:
    if st.toggle("Serwis (Zarząd)"):
        st.balloons()
        st.success(f"PRIMA APRILIS! Smacznej kawy {l_name}!")
