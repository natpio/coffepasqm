import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="SQM BI - Coffee Margin Portal",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM SQM DARK STYLE CSS + BACKGROUND IMAGE ---
st.markdown("""
    <style>
    /* Zdjęcie tła na całą aplikację */
    .stApp {
        background-image: url('sqm.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }

    /* Przezroczyste kontenery dla lepszej czytelności tekstu */
    .stApp .block-container {
        background-color: rgba(0, 0, 0, 0.7); /* Czarne, półprzezroczyste tło pod tekstem */
        padding: 2rem;
        border-radius: 10px;
    }
    
    /* Stylizacja nagłówków */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Wygląd inputów */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    /* Przycisk akcji w stylu SQM (czarny z czerwoną ramką) */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #ff4b4b;
        font-weight: bold;
        height: 3.5em;
        text-transform: uppercase;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
        box-shadow: 0px 0px 15px #ff4b4b;
    }

    /* Stylizacja komunikatu błędu */
    .stAlert {
        background-color: #1a0505;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }

    /* Stopka */
    .footer-text {
        font-size: 10px;
        color: #888;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_nav = st.columns([1, 4])
with col_logo:
    # Stylizowany tekst zamiast logo (jeśli nie masz pliku)
    st.markdown("<h2 style='margin:0;'>SQM</h2>", unsafe_allow_html=True)
with col_nav:
    st.write("<p style='text-align: right; color: #aaa; font-size: 12px;'>ABOUT &nbsp;&nbsp; WORKS &nbsp;&nbsp; SERVICES &nbsp;&nbsp; CONTACT &nbsp;&nbsp; SQM ESPAÑA</p>", unsafe_allow_html=True)

st.title("SQM BI - Coffee Margin Portal")
st.write("<p style='color: #ccc;'>Wydział Logistyki i Planowania Transportu</p>", unsafe_allow_html=True)
st.write("---")

# --- MAIN LAYOUT ---
col1, col2, col3 = st.columns([1, 1.3, 1.2])

with col1:
    st.write("### LOGIN & VERIFY")
    project_id = st.text_input("SQM PROJECT ID (5 DIGITS):", max_chars=5, placeholder="e.g., 45102")
    last_name = st.text_input("NAZWISKO:", placeholder="Kowalski")
    
    drink_type = st.selectbox("CHOOSE RESOURCE:", [
        "Espresso (Requires Margin >15%)", 
        "Double Espresso (Requires Margin >28%)", 
        "Flat White (Admin Only)",
        "Water (Free for All Projects)"
    ])
    
    st.write("")
    auth_button = st.button("CHECK MARGIN & AUTHORIZE COFFEE")

with col2:
    st.write("### PROJECT COST STRUCTURE")
    # Generowanie danych wykresu - marża celowo zaniżona
    labels = ['Transport', 'Warehousing', 'Staffing', 'AV Equipment', 'Margin']
    values = [42, 18, 26, 13.2, 0.8] 
    colors = ['#1a1a1a', '#2a2a2a', '#3a3a3a', '#4a4a4a', '#ff4b4b']

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

with col3:
    if auth_button:
        if not project_id or len(project_id) < 5 or not last_name:
            st.error("MISSING DATA: Please provide 5-digit Project ID and Surname.")
        else:
            with st.status("POBIERANIE DANYCH Z ERP...", expanded=True) as status:
                time.sleep(1.2)
                st.write(f"Sprawdzanie marży dla projektu #{project_id}...")
                time.sleep(1.0)
                st.write("Analiza slotów rozładunkowych i czasu pracy...")
                time.sleep(1.5)
                status.update(label="ANALIZA ZAKOŃCZONA", state="error")
            
            # --- FINAL REJECTION MESSAGE ---
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 5px; background-color: #1a0000;">
                    <h2 style="color: #ff4b4b; margin-top:0;">❌ ACCESS DENIED</h2>
                    <p style="color: white; font-weight: bold;">Użytkownik: {last_name}</p>
                    <p style="font-size: 0.9em; color: #ccc;">
                        <b>Reason:</b> Project Margin (0.8%) is below the Caffeine-Tolerance Threshold (Requires 28.5% for {drink_type}).
                    </p>
                    <hr style="border-color: #333;">
                    <p style="font-size: 0.85em; color: #aaa;">
                        Financial Audit detected <b>115% Transport Overage</b>. 
                        Coffee resources are temporarily locked for this project.
                    </p>
                    <p style="color: #ff4b4b; font-weight: bold; font-size: 0.8em; margin-bottom: 0;">
                        ZALECENIE: Pij wodę i planuj lepiej naczepy.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- BACKGROUND SLOGAN (PRANK EDITION) ---
st.write("")
st.write("")
st.write("")
st.markdown("""
    <div style="margin-top: 60px;">
        <h1 style="font-size: 70px; line-height: 0.85; color: white; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b;">MARGIN</span>.
        </h1>
        <h1 style="font-size: 70px; line-height: 0.85; color: white; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b;">CAFFEINE</span>.
        </h1>
        <h1 style="font-size: 70px; line-height: 0.85; color: #ff4b4b; margin: 0; font-weight: 900;">
            ALL FOR THE <span style="color: white;">COMPANY</span>.
        </h1>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("<p style='color: #aaa; font-size: 11px;'>SQM Business Intelligence System v9.9.2 | 2026-04-01</p>", unsafe_allow_html=True)
with col_f2:
    if st.toggle("Service Override"):
        st.balloons()
        st.toast("PRIMA APRILIS! 🤡 Kawa jest na koszt firmy!", icon="🎉")
        st.success("Wykryto tryb administratora. Smacznej kawy!")
