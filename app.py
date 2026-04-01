import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# --- KONFIGURACJA UI ---
st.set_page_config(
    page_title="SQM LOGISTICS BI - Margin & Coffee Controller",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLIZACJA DARK MODE / TECH ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stAlert { border-left: 5px solid #ff4b4b; background-color: #1c1f26; }
    .stButton>button { 
        width: 100%; height: 4em; background-color: #ff4b4b; color: white; 
        font-weight: bold; border-radius: 10px; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff2b2b; transform: scale(1.02); }
    [data-testid="stMetricValue"] { color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.sqm.pl/wp-content/uploads/2021/03/logo-sqm-white.png", width=150) # Link poglądowy
    st.status("System: ONLINE", state="complete")
    st.divider()
    st.write("Operator: Logistyka Transportowa")
    st.write("Lokalizacja: Magazyn / Biuro")

# --- NAGŁÓWEK ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📊 SQM Margin-to-Caffeine Interlock")
    st.subheader("System Zarządzania Zasobami Krytycznymi v9.9.2")
with col_h2:
    st.metric(label="Dostępna Kofeina (Biuro)", value="0.0 mg", delta="-100%")

st.divider()

# --- INPUTY ---
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    project_id = st.text_input("Numer Projektu SQM (5 cyfr):", max_chars=5, help="Wprowadź ID z systemu transportowego")

with col_in2:
    employee_id = st.text_input("ID Pracownika (Karta):", type="password")

with col_in3:
    drink_type = st.selectbox("Rodzaj zasobu:", [
        "Woda (Darmowa)",
        "Espresso (Low-Margin Mode)",
        "Double Espresso (High-Margin Only)",
        "Cappuccino (Admin Rights Required)",
        "Napój Energetyczny (Tylko Załadunki Nocne)"
    ])

# --- LOGIKA GŁÓWNA ---
if st.button("AUTORYZUJ DOSTĘP DO EKSPRESU"):
    if not project_id or len(project_id) < 5:
        st.error("BŁĄD: Niepoprawny format numeru projektu. System ERP SQM nie odpowiada.")
    else:
        # Faza 1: Symulacja obliczeń
        with st.status("Analizowanie rentowności projektu...", expanded=True) as status:
            st.write("Pobieranie kosztów naczep i slotów...")
            time.sleep(1.0)
            st.write(f"Weryfikacja planowania przestrzeni dla projektu #{project_id}...")
            time.sleep(1.2)
            st.write("Obliczanie kosztów amortyzacji sprzętu AV na m2...")
            time.sleep(0.8)
            
            # Generowanie fałszywych danych do wykresu
            chart_data = pd.DataFrame({
                'Kategoria': ['Transport', 'Magazyn', 'Montaż', 'Sprzęt', 'Marża Realna'],
                'Koszty': [random_val := np.random.randint(30, 50), 20, 15, 20, 100 - (random_val + 55)]
            })
            
            st.write("Generowanie raportu rentowności...")
            time.sleep(1.0)
            status.update(label="ANALIZA ZAKOŃCZONA: BRAK UPRAWNIEŃ", state="error")

        # Faza 2: Wizualizacja porażki
        st.divider()
        c1, c2 = st.columns([2, 1])

        with c1:
            fig = go.Figure(data=[go.Pie(labels=chart_data['Kategoria'], values=chart_data['Koszty'], hole=.3)])
            fig.update_layout(title_text="Struktura kosztów projektu", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.error("### ODMOWA: NISKA MARŻA")
            st.metric(label="Aktualna Marża Operacyjna", value=f"{chart_data['Koszty'].iloc[-1]}%", delta="-12.5%")
            st.write(f"""
            **Powód blokady:**
            Zasób **{drink_type}** wymaga marży na poziomie minimum **28%**. 
            Projekt **#{project_id}** wykazuje deficyt z powodu błędnie zaplanowanych slotów rozładunkowych.
            """)
            
        st.warning("🚨 UWAGA: Próba nieautoryzowanego parzenia kawy zostanie odjęta od diety delegacyjnej.")

# --- FOOTER / EASTER EGG ---
st.divider()
st.caption("Terminal ID: SQM-WH-001 | Protokół: 1-APRIL-2026")

if st.toggle("System Override (Technik Serwisu)"):
    st.balloons()
    st.success("PRIMA APRILIS! Marża to tylko liczba, a kawa to paliwo. Miłej pracy w SQM! 🤡")
