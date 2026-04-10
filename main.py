import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AGVAC", layout="wide")

# Estilos CSS actualizados
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; z-index: 100; }
    .about-box { 
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #e0e0e0;
        border-left: 6px solid #005b7f;
        margin-top: 20px;
        font-size: 14px;
        color: #333;
        line-height: 1.6;
    }
    .logo-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-bottom: 20px;
    }
    .login-footer-version { text-align: center; color: #9e9e9e; font-size: 12px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ARCHIVOS Y DATOS ---
DB_FILE = "datos_agvac.csv"
STOCK_FILE = "stock_agvac.csv"

# Enlaces de logos
URL_LOGO_AGVAC = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"
URL_LOGO_MRG = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG"

if 'lista_vacunas' not in st.session_state:
    st.session_state.lista_vacunas = {
        "Herpes Zoster": "#FF8C00", "Neumococo20": "#00008B", "ProQuad": "#808080",
        "VariVax": "#FF0000", "Priorix": "#A9A9A9", "Mpox": "#FFFF00",
        "GRIPE": "#ADD8E6", "VPH": "#AEC6CF", "HepB": "#9ACD32",
        "HepB Hemo": "#808000", "HepA": "#000080", "HepA+B": "#90EE90",
        "Meningitis ACW135Y": "#D3D3D3", "Meningitis B": "#800000",
        "Tetanos-Difteria": "#FF4500", "Boostrix": "#800080", "Hexa": "#7DF9FF",
        "Vivotif": "#77DD77", "Fiebre Tifoidea": "#00FF7F", "Fiebre Amarilla": "#CCFF00",
        "COVID": "#E6E6FA"
    }

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Semana", "Mes", "Año"]).to_csv(DB_FILE, index=False)
if not os.path.exists(STOCK_FILE):
    df_init = pd.DataFrame([{"Vacuna": v, "Cantidad": 25, "Minimo": 5} for v in st.session_state.lista_vacunas.keys()])
    df_init.to_csv(STOCK_FILE, index=False)

# --- BLOQUE CORPORATIVO "SOBRE AGVAC" ---
SOBRE_AGVAC_HTML = f"""
<div class="about-box">
    <div class="logo-container">
        <img src="{URL_LOGO_AGVAC}" width="80">
        <img src="{URL_LOGO_MRG}" width="80">
    </div>
    <h3 style="text-align:center;">Sobre AGVAC</h3>
    <p><b>AGVAC</b> es una solución tecnológica avanzada diseñada específicamente para optimizar la gestión de inventarios de vacunas en entornos sanitarios.</p>
    <p>Esta aplicación ha sido diseñada y desarrollada por <b>MRG Healthcare Applications</b>, un equipo multidisciplinar compuesto por profesionales del sector salud y expertos en ingeniería informática. Nuestro enfoque combina la experiencia clínica con soluciones de software robustas para crear herramientas que den respuesta a los desafíos reales de la sanidad moderna.</p>
    <p>A través de AGVAC, permitimos:</p>
    <ul>
        <li><b>Registro Automatizado:</b> Trazabilidad de cada dosis con actualización inmediata de existencias.</li>
        <li><b>Gestión de Stock Crítico:</b> Sistema de alertas inteligentes para prevenir el desabastecimiento.</li>
        <li><b>Análisis de Datos:</b> Visualización de métricas de actividad para una planificación estratégica eficiente.</li>
    </ul>
</div>
"""

# --- 3. CONTROL DE ACCESO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

def login():
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown(f'<div style="text-align:center; margin-top:50px;"><img src="{URL_LOGO_AGVAC}" width="180"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Acceso AGVAC</h2>", unsafe_allow_html=True)
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if usuario == "agvac" and password == "agvac":
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Credenciales incorrectas")
        
        st.markdown(SOBRE_AGVAC_HTML, unsafe_allow_html=True)
        st.markdown("<div class='login-footer-version'>MRGAGVAC2026.1.6.1</div>", unsafe_allow_html=True)

if not st.session_state.autenticado:
    login()
    st.stop()

# --- 4. INTERFAZ PRINCIPAL ---
if 'cesta' not in st.session_state: st.session_state.cesta = []

# Sidebar
st.sidebar.title("Menú AGVAC")
if st.sidebar.button("🔒 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

with st.sidebar.expander("ℹ️ Sobre AGVAC & MRG"):
    st.markdown(SOBRE_AGVAC_HTML, unsafe_allow_html=True)

st.sidebar.divider()
df_stock_sidebar = pd.read_csv(STOCK_FILE)
alertas = df_stock_sidebar[df_stock_sidebar['Cantidad'] <= df_stock_sidebar['Minimo']]
if not alertas.empty:
    st.sidebar.error("⚠️ ALERTAS DE STOCK")
    for _, fila in alertas.iterrows():
        st.sidebar.warning(f"{fila['Vacuna']}: {int(fila['Cantidad'])} unidades")

# Cabecera
col_izq, col_centro, col_der = st.columns([1, 4, 1])
with col_izq: st.image(URL_LOGO_MRG)
with col_centro: st.markdown("<h1 style='text-align: center; font-size: 50px;'>AGVAC</h1>", unsafe_allow_html=True)
with col_der: st.image(URL_LOGO_AGVAC)

tab_reg, tab_hist, tab_graf, tab_conf = st.tabs(["📝 Registro", "📋 Historial", "📊 Estadísticas", "⚙️ Stock y Catálogo"])

# --- CONTENIDO DE TABS ---
with tab_reg:
    col_s, col_c = st.columns(2)
    with col_s:
        st.subheader("🔍 Seleccionar Vacuna")
        seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()))
        if st.button("➕ Añadir"):
            if seleccion: st.session_state.cesta.append(seleccion); st.rerun()
    with col_c:
        st.subheader("📦 Cesta")
        for i, item in enumerate(st.session_state.cesta): st.write(f"{i+1}. {item}")
        if st.session_state.cesta and st.button("✅ GUARDAR Y DESCONTAR"):
            df_hist = pd.read_csv(DB_FILE)
            df_stock = pd.read_csv(STOCK_FILE)
            ahora = datetime.now()
            for item in st.session_state.cesta:
                nueva = {"Fecha": ahora.strftime("%Y-%m-%d %H:%M"), "Vacuna": item, "Semana": ahora.strftime("%U-%Y"), "Mes": ahora.strftime("%m-%Y"), "Año": ahora.strftime("%Y")}
                df_hist = pd.concat([df_hist, pd.DataFrame([nueva])], ignore_index=True)
                if item in df_stock['Vacuna'].values:
                    idx = df_stock.index[df_stock['Vacuna'] == item].tolist()[0]
                    df_stock.at[idx, 'Cantidad'] -= 1
            df_hist.to_csv(DB_FILE, index=False); df_stock.to_csv(STOCK_FILE, index=False)
            st.session_state.cesta = []; st.success("Registrado"); st.rerun()

with tab_hist:
    st.subheader("📋 Historial")
    df_v = pd.read_csv(DB_FILE)
    if not df_v.empty:
        df_d = df_v.iloc[::-1].copy()
        id_e = st.selectbox("Borrar registro (+1 stock):", options=df_d.index, format_func=lambda x: f"{df_d.loc[x, 'Fecha']} | {df_d.loc[x, 'Vacuna']}")
        if st.button("🗑️ Eliminar"):
            v_ret = df_v.loc[id_e, 'Vacuna']
            df_s = pd.read_csv(STOCK_FILE)
            if v_ret in df_s['Vacuna'].values:
                idx_s = df_s.index[df_s['Vacuna'] == v_ret].tolist()[0]
                df_s.at[idx_s, 'Cantidad'] += 1
                df_s.to_csv(STOCK_FILE, index=False)
            df_v.drop(id_e).to_csv(DB_FILE, index=False); st.rerun()
        st.dataframe(df_d, use_container_width=True)

with tab_graf:
    df_g = pd.read_csv(DB_FILE)
    if not df_g.empty:
        fig = px.pie(df_g['Vacuna'].value_counts().reset_index(), values='count', names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

with tab_conf:
    df_st = pd.read_csv(STOCK_FILE)
    st.dataframe(df_st, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        v_a = st.selectbox("Ajustar:", df_st['Vacuna'])
        n_a = st.number_input("Cantidad (+/-):", step=1)
        if st.button("Actualizar Stock"):
            idx = df_st.index[df_st['Vacuna'] == v_a].tolist()[0]
            df_st.at[idx, 'Cantidad'] += n_a
            df_st.to_csv(STOCK_FILE, index=False); st.rerun()
    with col2:
        n_v = st.text_input("Nueva Vacuna:")
        n_c = st.color_picker("Color:", "#005b7f")
        if st.button("Añadir al Sistema") and n_v:
            nueva = pd.DataFrame([{"Vacuna": n_v, "Cantidad": 25, "Minimo": 5}])
            pd.concat([df_st, nueva], ignore_index=True).to_csv(STOCK_FILE, index=False)
            st.session_state.lista_vacunas[n_v] = n_c; st.rerun()

st.markdown(f'<div class="footer">MRGAGVAC2026.1.6.1 | <img src="{URL_LOGO_MRG}" width="15"> MRG Healthcare Applications</div>', unsafe_allow_html=True)
