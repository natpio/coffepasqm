import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SQM BI - Coffee Margin Portal",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNCTION TO LOAD BACKGROUND IMAGE ---
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

# --- CUSTOM CSS (WHITE HEADERS & CONTRAST) ---
st.markdown(f"""
    <style>
    .stApp {{
        {bg_img_style}
    }}
    
    /* Kontener główny - ciemniejszy dla lepszego kontrastu białych liter */
    .stApp .block-container {{
        background-color: rgba(0, 0, 0, 0.85);
        padding: 3rem;
        border-radius: 20px;
        margin-top: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }}

    /* Nagłówki - wymuszenie białego koloru */
    h1, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 800 !important;
    }}
    
    /* Teksty pomocnicze i labele */
    .stMarkdown p, label, .stSelectbox label, .stTextInput label {{
        color: #ffffff !important;
        font-weight: 600 !important;
    }}

    /* Stylizacja pól wprowadzania */
    .stTextInput input {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #444 !important;
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
        box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.8);
    }}

    /* Komunikat o braku marży */
    .stAlert {{
        background-color: rgba(50, 0, 0, 0.9) !important;
        border: 1px solid #ff4b4b !important;
    }}
    
    .stAlert p {{
        color: #ff4b4b !important;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    st.markdown("<h2 style='margin:0; color: white;'>SQM</h2>", unsafe_allow_html=True)
with col_r:
    st.write("<p style='text-align: right; color: #bbb; font-size: 13px;'>ABOUT &nbsp;&nbsp; WORKS &nbsp;&nbsp; SERVICES &nbsp;&nbsp; CONTACT &nbsp;&nbsp; SQM ESPAÑA</p>", unsafe_allow_html=True)

st.title("SQM BI - Coffee Margin Portal")
st.markdown("<p style='color: #ff4b4b; font-weight: bold; letter-spacing: 1px;'>LOGISTICS & MARGIN INTERLOCK SYSTEM v9.9.2</p>", unsafe_allow_html=True)
st.write("---")

# --- MAIN COLUMNS ---
c1, c2, c3 = st.columns([1, 1.3, 1.2])

with c1:
    st.markdown("### SYSTEM AUTH")
    p_id = st.text_input("SQM PROJECT ID (5 DIGITS):", max_chars=5, placeholder="np. 48291")
    l_name = st.text_input("NAZWISKO:", placeholder="Twoje nazwisko")
    
    drink = st.selectbox("SELECT RESOURCE:", [
        "Espresso (Min. Margin 15%)", 
        "Double Espresso (Min. Margin 28%)", 
        "Flat White (Exec. Only)",
        "Water (Standard)"
    ])
    
    st.write("")
    btn = st.button("VERIFY MARGIN & START BREWING")

with c2:
    st.markdown("### PROJECT RENTABILITY")
    labels = ['Transport', 'Warehouse', 'Staff', 'AV Gear', 'Margin']
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
            st.error("ERROR: Provide full project ID and surname.")
        else:
            with st.status("FETCHING DATA FROM SQM ERP...", expanded=True) as status:
                time.sleep(1.0)
                st.write(f"Analyzing project #{p_id}...")
                time.sleep(1.2)
                st.write("Checking logistics costs...")
                time.sleep(0.8)
                status.update(label="ANALYSIS FAILED", state="error")
            
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 5px; background-color: rgba(40,0,0,0.95); box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.3);">
                    <h2 style="color: #ff4b4b !important; margin-top:0; font-size: 20px;">❌ ACCESS DENIED</h2>
                    <p style="color: white !important;">Użytkownik: <b>{l_name}</b></p>
                    <p style="font-size: 13px; color: #eee !important;">
                        <b>Reason:</b> Resource <b>{drink}</b> is locked. Current project margin (0.5%) is below threshold.
                    </p>
                    <hr style="border-color: #555;">
                    <p style="font-size: 12px; color: #bbb !important;">
                        Logistics Audit: Excessive unloading hours and trailer space underutilization detected.
                    </p>
                    <p style="color: #ff4b4b !important; font-weight: bold; font-size: 13px; margin-top: 10px;">
                        ZALECENIE: Pij wodę. Wszystko dla firmy.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- FOOTER SLOGAN (WHITE & RED) ---
st.write("")
st.write("")
st.markdown("""
    <div style="margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 30px;">
        <h1 style="font-size: 75px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b !important;">MARGIN</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: white !important; margin: 0; font-weight: 900;">
            NO <span style="color: #ff4b4b !important;">CAFFEINE</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: #ff4b4b !important; margin: 0; font-weight: 900;">
            ALL FOR THE <span style="color: white !important;">COMPANY</span>.
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #888; font-size: 11px;'>SQM Internal BI System | Automated Coffee Control | 2026-04-01</p>", unsafe_allow_html=True)
with f_col2:
    if st.toggle("Override (Admin)"):
        st.balloons()
        st.success(f"PRIMA APRILIS! Smacznej kawy {l_name}!")
