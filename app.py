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
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Sprawdzenie czy plik istnieje i przygotowanie stylu tła
img_path = 'sqm.jpg'
if os.path.exists(img_path):
    bin_str = get_base64_of_bin_file(img_path)
    bg_img_style = f"""
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    """
else:
    bg_img_style = "background-color: #0e1117;" # Fallback na ciemny kolor

# --- CUSTOM CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        {bg_img_style}
    }}
    
    /* Kontener treści z silnym rozmyciem tła dla efektu premium */
    .stApp .block-container {{
        background-color: rgba(0, 0, 0, 0.82);
        padding: 3rem;
        border-radius: 20px;
        margin-top: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    h1, h2, h3 {{
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    .stTextInput input {{
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }}

    /* Przycisk SQM Style */
    .stButton>button {{
        width: 100%;
        background-color: transparent;
        color: #ffffff;
        border: 2px solid #ff4b4b;
        font-weight: bold;
        height: 3.5em;
        text-transform: uppercase;
        transition: 0.4s;
    }}
    
    .stButton>button:hover {{
        background-color: #ff4b4b;
        color: white;
        box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.6);
    }}

    .stAlert {{
        background-color: #1a0000;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }}

    .footer-text {{
        font-size: 10px;
        color: #666;
        text-align: center;
        margin-top: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    st.markdown("<h2 style='margin:0;'>SQM</h2>", unsafe_allow_html=True)
with col_r:
    st.write("<p style='text-align: right; color: #888; font-size: 13px;'>ABOUT &nbsp;&nbsp; WORKS &nbsp;&nbsp; SERVICES &nbsp;&nbsp; CONTACT &nbsp;&nbsp; SQM ESPAÑA</p>", unsafe_allow_html=True)

st.title("SQM BI - Coffee Margin Portal")
st.write("<p style='color: #ff4b4b; font-weight: bold;'>LOGISTICS & MARGIN INTERLOCK SYSTEM v9.9.2</p>", unsafe_allow_html=True)
st.write("---")

# --- MAIN COLUMNS ---
c1, c2, c3 = st.columns([1, 1.3, 1.2])

with c1:
    st.write("### SYSTEM AUTH")
    p_id = st.text_input("SQM PROJECT ID (5 DIGITS):", max_chars=5, placeholder="e.g., 48291")
    l_name = st.text_input("NAZWISKO:", placeholder="Kowalski")
    
    drink = st.selectbox("SELECT RESOURCE:", [
        "Espresso (Min. Margin 15%)", 
        "Double Espresso (Min. Margin 28%)", 
        "Flat White (Exec. Only)",
        "Water (Standard)"
    ])
    
    st.write("")
    btn = st.button("VERIFY MARGIN & START BREWING")

with c2:
    st.write("### PROJECT RENTABILITY")
    labels = ['Transport', 'Warehouse', 'Staff', 'AV Gear', 'Margin']
    values = [45, 18, 25, 11.5, 0.5] # 0.5% marży - czyste zło
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
                st.write("Calculating trailer slot costs...")
                time.sleep(0.8)
                status.update(label="ANALYSIS FAILED", state="error")
            
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 5px; background-color: rgba(26,0,0,0.9);">
                    <h2 style="color: #ff4b4b; margin-top:0; font-size: 20px;">❌ ACCESS DENIED</h2>
                    <p style="color: white;">Użytkownik: <b>{l_name}</b></p>
                    <p style="font-size: 13px; color: #ccc;">
                        <b>Reason:</b> Resource <b>{drink}</b> is locked. Current project margin (0.5%) is below threshold.
                    </p>
                    <hr style="border-color: #444;">
                    <p style="font-size: 12px; color: #999;">
                        Logistics Audit: Excessive unloading hours and trailer space underutilization detected.
                    </p>
                    <p style="color: #ff4b4b; font-weight: bold; font-size: 13px; margin-top: 10px;">
                        ZALECENIE: Pij wodę. Wszystko dla firmy.
                    </p>
                </div>
            """, unsafe_allow_html=True)

# --- FOOTER SLOGAN ---
st.write("")
st.write("")
st.markdown("""
    <div style="margin-top: 40px;">
        <h1 style="font-size: 75px; line-height: 0.85; color: white; margin: 0; font-weight: 900; opacity: 0.9;">
            NO <span style="color: #ff4b4b;">MARGIN</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: white; margin: 0; font-weight: 900; opacity: 0.9;">
            NO <span style="color: #ff4b4b;">CAFFEINE</span>.
        </h1>
        <h1 style="font-size: 75px; line-height: 0.85; color: #ff4b4b; margin: 0; font-weight: 900; opacity: 0.9;">
            ALL FOR THE <span style="color: white;">COMPANY</span>.
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("<p style='color: #666; font-size: 11px;'>SQM Internal BI System | Automated Coffee Control | 2026-04-01</p>", unsafe_allow_html=True)
with f_col2:
    if st.toggle("Override (Admin)"):
        st.balloons()
        st.success(f"PRIMA APRILIS! Smacznej kawy {l_name}!")
