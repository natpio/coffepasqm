import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="SQM BI - Portal Kawowy",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNKCJA ŁADOWANIA TŁA ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Przygotowanie tła
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
    bg_img_style = "background-color: #0e1117;"

# --- CUSTOM CSS (BIAŁE NAGŁÓWKI + CZYTELNE POLA WPISYWANIA) ---
st.markdown(f"""
    <style>
    .stApp {{
        {bg_img_style}
    }}
    
    /* Kontener główny - wysoki kontrast */
    .stApp .block-container {{
        background-color: rgba(0, 0, 0, 0.88);
        padding: 3rem;
        border-radius: 20px;
        margin-top: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0px 10px 40px rgba(0,0,0,0.8);
    }}

    /* Białe nagłówki */
    h1, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 800 !important;
    }}
    
    /* Napisy przy polach (Label) */
    label, .stMarkdown p {{
        color: #ffffff !important;
        font-weight: 600 !important;
    }}

    /* POPRAWKA: Czarna czcionka w białych polach wpisywania */
    .stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ff4b4b !important;
        font-weight: bold !important;
    }}

    /* Stylizacja listy rozwijanej */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}

    /* Przycisk SQM Style */
    .stButton>button {{
        width: 100%;
        background-color: transparent;
        color: #ffffff !important;
        border: 2px solid #ff4b4b !important;
        font-weight: bold;
        height: 3.5em;
        text-transform: uppercase;
        transition: 0.4s;
    }}
    
    .stButton>button:hover {{
        background-color: #ff4b4b !important;
        color: white !important;
        box-shadow: 0px 0px 25px rgba(255, 75, 75, 0.9);
    }}

    /* Stylizacja komunikatów błędów */
    .stAlert {{
        background-color: rgba(60, 0, 0, 0.95) !important;
        border: 2px solid #ff4b4b !important;
    }}
    
    .stAlert p {{
        color: #ffffff !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- NAGŁÓWEK ---
col_l, col_r = st.columns([1, 4])
with col_l:
    st.markdown("<h2 style='margin:0; color: white;'>SQM</h2>", unsafe_allow_html=True)
with col_r:
    st.write("<p style='text-align: right; color: #bbb; font-size: 13px;'>O NAS &nbsp;&nbsp; REALIZACJE &nbsp;&nbsp; USŁUGI &nbsp;&nbsp; KONTAKT &nbsp;&nbsp; SQM HISZPANIA</p>", unsafe_allow_html=True)

st.title("SQM BI - Portal Zarządzania Kofeiną")
st.markdown("<p style='color: #ff4b4b; font-weight: bold; letter-spacing: 1px;'>SYSTEM INTEGRACJI LOGISTYKI Z MARŻĄ v9.9.2</p>", unsafe_allow_html=True)
st.write("---")

# --- GŁÓWNY UKŁAD ---
c1, c2, c3 = st.columns([1, 1.3, 1.2])

with c1:
    st.markdown("### AUTORYZACJA SYSTEMU")
    p_id = st.text_input("NUMER PROJEKTU SQM (5 CYFR):", max_chars=5, placeholder="np. 48291")
    l_name = st.text_input("NAZWISKO:", placeholder="Wpisz swoje nazwisko")
    
    drink = st.selectbox("WYBIERZ ZASÓB:", [
        "Espresso (Wymagana marża >15%)", 
        "Double Espresso (Wymagana marża >28%)", 
        "Flat White (Tylko dla Zarządu)",
        "Woda z kranu (Dostępna dla każdego projektu)"
    ])
    
    st.write("")
    btn = st.button("WERYFIKUJ MARŻĘ I URUCHOM EKSPRES")

with c2:
    st.markdown("### RENTOWNOŚĆ PROJEKTU")
    labels = ['Transport', 'Magazyn', 'Obsługa', 'Sprzęt AV', 'Marża']
    values = [45, 18, 25, 11.5, 0.5] 
    colors = ['#111', '#222', '#333', '#444', '#ff4b4b']

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
            st.error("BŁĄD: Podaj pełny 5-cyfrowy ID projektu oraz nazwisko.")
        else:
            with st.status("POBIERANIE DANYCH Z ERP SQM...", expanded=True) as status:
                time.sleep(1.0)
                st.write(f"Analiza rentowności projektu #{p_id}...")
                time.sleep(1.2)
                st.write("Weryfikacja kosztów logistycznych i slotów...")
                time.sleep(0.8)
                status.update(label="ANALIZA ZAKOŃCZONA NIEPOWODZENIEM", state="error")
            
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 10px; background-color: rgba(40,0,0,0.95);">
                    <h2 style="color: #ff4b4b !important; margin-top:0; font-size: 20px;">❌ ODMOWA DOSTĘPU</h2>
                    <p style="color: white !important;">Użytkownik: <b>{l_name}</b></p>
                    <p style="font-size: 13px; color: #eee !important;">
                        <b>Powód:</b> Zasób <b>{drink}</b> jest zablokowany. Aktualna marża projektu (0.5%) jest poniżej progu kofeinowego.
                    </p>
                    <hr style="border-color: #555;">
                    <p style="font-size: 12px; color: #bbb !important;">
                        Audyt logistyczny: Wykryto nadmiarowe godziny rozładunku i niewykorzystaną przestrzeń na naczepie.
                    </p>
                    <p style="color: #ff4b4b !important; font-weight: bold; font-size: 14px; margin-top: 10px;">
                        ZALECENIE: Pij wodę. Wszystko dla firmy.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- DOLNY SLOGAN ---
st.write("")
st.write("")
st.markdown("""
    <div style="margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 30px;">
        <h1 style="font-size: 75px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            BRAK <span style="color: #ff4b4b !important;">MARŻY</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            BRAK <span style="color: #ff4b4b !important;">KAWY</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: #ff4b4b !important; margin: 0; font-weight: 900;">
            WSZYSTKO DLA <span style="color: white !important;">FIRMY</span>.
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #888; font-size: 11px;'>Wewnętrzny System BI SQM | Automatyczna Kontrola Wydatków | 2026-04-01</p>", unsafe_allow_html=True)
with f_col2:
    if st.toggle("Tryb Serwisowy (Admin)"):
        st.balloons()
        st.success(f"PRIMA APRILIS! Smacznej kawy {l_name}! To tylko żart :)")
