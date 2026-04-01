import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="SQM BI - Coffee Margin Portal",
    page_icon="☕",
    layout="wide"
)

# --- CUSTOM SQM DARK STYLE CSS ---
st.markdown("""
    <style>
    /* Główny background i czcionki */
    .stApp {
        background-color: #000000;
        color: #ffffff;
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

    /* Czerwony przycisk akcji w stylu SQM */
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

    /* Panel błędu / Access Denied */
    .stAlert {
        background-color: #1a0505;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }

    /* Footer text */
    .footer-text {
        font-size: 10px;
        color: #444;
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_nav = st.columns([1, 4])
with col_logo:
    st.write("### SQM") # Tutaj można wstawić logo obrazkowe jeśli masz URL
with col_nav:
    st.write("<p style='text-align: right; color: #666;'>ABOUT &nbsp;&nbsp; WORKS &nbsp;&nbsp; SERVICES &nbsp;&nbsp; CONTACT</p>", unsafe_allow_html=True)

st.title("SQM BI - Coffee Margin Portal")
st.write("---")

# --- MAIN LAYOUT ---
col1, col2, col3 = st.columns([1, 1.5, 1.2])

with col1:
    st.write("### AUTORYZACJA")
    project_id = st.text_input("SQM PROJECT ID (5 DIGITS):", max_chars=5, placeholder="e.g., 45102")
    last_name = st.text_input("NAZWISKO:", placeholder="Kowalski")
    
    st.write("")
    auth_button = st.button("CHECK MARGIN & AUTHORIZE COFFEE")

with col2:
    st.write("### PROJECT COST STRUCTURE")
    # Generowanie "smutnego" wykresu marży
    labels = ['Transport', 'Warehousing', 'Staff', 'Equipment', 'Margin']
    values = [45, 15, 25, 14.2, 0.8] # Marża 0.8% - dramat PM-a
    colors = ['#222', '#333', '#444', '#555', '#ff4b4b']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    if auth_button:
        if not project_id or len(project_id) < 5 or not last_name:
            st.warning("PLEASE FILL ALL FIELDS.")
        else:
            with st.spinner("CONNECTING TO SQM ERP..."):
                time.sleep(2)
            
            # KOMUNIKAT FINALNY
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #ff4b4b; margin-top:0;">❌ ACCESS DENIED</h2>
                    <p><b>REASON:</b><br>Project Margin below Caffeine-Tolerance Threshold (Requires >28.5%).</p>
                    <hr style="border-color: #333;">
                    <p style="font-size: 0.9em; line-height: 1.6;">
                        <b>Financial Data:</b><br>
                        Project #{project_id}<br>
                        Estimated Transport Overage: 115%<br>
                        Staff Hours: 130%<br>
                        Current Project Margin: <b>0.8%</b>
                    </p>
                    <p style="color: #ff4b4b; font-weight: bold; font-size: 0.8em;">
                        Suggested Action: Drink water or submit a budget revision.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- BACKGROUND SLOGAN (Style jak na zdjęciu) ---
st.write("")
st.write("")
st.markdown("""
    <h1 style="font-size: 60px; opacity: 0.1; line-height: 0.8;">
    ONE PARTNER.<br>CRAFT AND EXCELLENCE.<br>ONE STEP AHEAD.
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p class='footer-text'>SQM Business Intelligence. All caffeine usage is monitored by Logistics Department.</p>", unsafe_allow_html=True)

# Easter Egg dla Ciebie
if st.toggle("Service Mode"):
    st.balloons()
    st.success(f"Cześć {last_name}! To tylko żart Prima Aprilis. Miłego dnia w SQM!")
