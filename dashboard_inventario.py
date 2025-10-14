import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===========================
# CONFIGURACIÓN DE PÁGINA
# ===========================
st.set_page_config(
    page_title="Dashboard Inventario - Pesca Industrial",
    page_icon="🐟",
    layout="wide"
)

# ===========================
# CSS DARK MODE PREMIUM
# ===========================
st.markdown("""
    <style>
    /* Fondo oscuro principal */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0a0e27 100%);
    }
    
    /* Banner oscuro con gradiente premium */
    .banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.6),
            0 0 80px rgba(6, 214, 160, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(6, 214, 160, 0.2);
    }
    
    /* Animación de brillo en el banner */
    .banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 214, 160, 0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .banner h1 {
    color: #06D6A0;
    font-size: 3.2rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 
        0 0 25px rgba(6, 214, 160, 0.6),
        0 0 40px rgba(6, 214, 160, 0.4),
        0 6px 20px rgba(0,0,0,0.7),
        0 3px 10px rgba(0,0,0,0.5);
    position: relative;
    z-index: 1;
    letter-spacing: 2px;
}

    
    .banner p {
        color: #e0e0e0;
        font-size: 1.3rem;
        margin: 0.8rem 0 0 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
        font-weight: 300;
    }
    
    /* Tarjetas KPI OSCURAS con brillo */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            0 0 20px rgba(6, 214, 160, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(6, 214, 160, 0.2);
        border-left: 4px solid #06D6A0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-height: 190px;
    }
    
    /* Efecto de brillo neón */
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(6, 214, 160, 0.1),
            transparent
        );
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .metric-card:hover::before {
        animation: shine 0.8s ease-in-out;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.7),
            0 0 40px rgba(6, 214, 160, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-left-color: #00ffcc;
        border-left-width: 5px;
    }
    
    /* Números grandes con gradiente neón */
    .big-number {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #06D6A0 0%, #00ffcc 50%, #0891b2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 18px 0;
        filter: drop-shadow(0 0 15px rgba(6, 214, 160, 0.4));
        letter-spacing: 1px;
    }
    
    /* Etiquetas con estilo oscuro */
    .metric-label {
        font-size: 1rem;
        font-weight: 700;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Delta con color verde neón */
    .metric-delta {
        font-size: 0.95rem;
        font-weight: 600;
        color: #06D6A0;
        display: flex;
        align-items: center;
        gap: 5px;
        text-shadow: 0 0 10px rgba(6, 214, 160, 0.3);
    }
    
    /* Títulos de sección oscuros */
    h2 {
        color: #06D6A0;
        font-weight: 900;
        font-size: 2.4rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        text-shadow: 
            0 0 20px rgba(6, 214, 160, 0.5),
            2px 2px 10px rgba(0, 0, 0, 0.5);
        border-left: 8px solid #06D6A0;
        padding-left: 25px;
        letter-spacing: 1px;
    }
    
    /* Subtítulos */
    h3 {
        color: #e0e0e0;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }
    
    /* Botón de descarga premium oscuro */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #06D6A0 0%, #00ffcc 100%);
        color: #0a0e27;
        border: none;
        border-radius: 14px;
        font-weight: 800;
        padding: 1.2rem 2.5rem;
        box-shadow: 
            0 8px 25px rgba(6, 214, 160, 0.4),
            0 0 20px rgba(6, 214, 160, 0.2);
        transition: all 0.3s ease;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 
            0 12px 35px rgba(6, 214, 160, 0.5),
            0 0 30px rgba(6, 214, 160, 0.3);
        background: linear-gradient(135deg, #00ffcc 0%, #06D6A0 100%);
    }
    
    /* Expander oscuro */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        font-weight: 700;
        color: #e0e0e0;
        border: 1px solid rgba(6, 214, 160, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Tablas con fondo oscuro */
    .dataframe {
        background-color: #1a1a2e;
        color: #e0e0e0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Métricas de Streamlit personalizadas */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #06D6A0;
        font-weight: 900;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    [data-testid="stMetricDelta"] {
        color: #06D6A0;
    }
    </style>
""", unsafe_allow_html=True)

# ===========================
# CARGAR DATOS
# ===========================
@st.cache_data
def cargar_datos():
    data_detalle = pd.read_csv('inventario_detalle.csv')
    data_resumen = pd.read_csv('inventario_resumen.csv')
    data_fifo = pd.read_csv('inventario_fifo.csv')
    return data_detalle, data_resumen, data_fifo

data_detalle, data_resumen, data_fifo = cargar_datos()

# ===========================
# ===========================
# BANNER PREMIUM CON IMAGEN Y PESCADO DESTACADO
# ===========================
import base64
from pathlib import Path

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = "Orizon.png"

if Path(image_path).exists():
    img_base64 = get_base64_image(image_path)
    background_image = f"url(data:image/png;base64,{img_base64}),"
else:
    background_image = ""

st.markdown(f"""
    <style>
        .banner {{
            background: 
                {background_image}
                linear-gradient(135deg, rgba(6, 214, 160, 0.15) 0%, rgba(8, 145, 178, 0.1) 100%);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        .banner h1 {{
            text-shadow: 
                0 0 30px rgba(0, 0, 0, 0.95),
                0 0 20px rgba(0, 0, 0, 0.9),
                0 4px 15px rgba(0, 0, 0, 0.8),
                0 2px 8px rgba(0, 0, 0, 0.7),
                0 0 50px rgba(6, 214, 160, 0.6) !important;
            -webkit-text-stroke: 1px rgba(0, 0, 0, 0.5);
        }}
        
        .fish-emoji {{
            font-size: 4rem;
            display: inline-block;
            filter: 
                drop-shadow(0 0 20px rgba(0, 0, 0, 1))
                drop-shadow(0 0 15px rgba(0, 0, 0, 0.9))
                drop-shadow(0 5px 10px rgba(0, 0, 0, 0.8))
                drop-shadow(0 0 30px rgba(255, 255, 255, 0.3));
            margin-right: 1rem;
        }}
    </style>
    
    <div class="banner">
        <h1>
            <span class="fish-emoji">🐟</span>
            Dashboard de Inventario
        </h1>
        <p style="
            font-size: 1.15rem; 
            font-weight: 500; 
            margin: 0.8rem 0 0.3rem 0;
            text-shadow: 
                0 0 20px rgba(0, 0, 0, 0.95),
                0 0 15px rgba(0, 0, 0, 0.9),
                0 4px 12px rgba(0, 0, 0, 0.8),
                0 2px 6px rgba(0, 0, 0, 0.7);
            letter-spacing: 1.5px;
            -webkit-text-stroke: 0.5px rgba(0, 0, 0, 0.4);
            color: #ffffff;
        ">
            <b>ORIZON</b> - Planta Coronel
        </p>
        <p style="
            font-size: 1.1rem; 
            font-weight: 400; 
            margin: 0;
            text-shadow: 
                0 0 20px rgba(0, 0, 0, 0.95),
                0 0 15px rgba(0, 0, 0, 0.9),
                0 3px 10px rgba(0, 0, 0, 0.8),
                0 2px 5px rgba(0, 0, 0, 0.7);
            -webkit-text-stroke: 0.5px rgba(0, 0, 0, 0.4);
            color: #e0e0e0;
        ">
            Producto Terminado | Centro P109 - Almacén I93
        </p>
    </div>
""", unsafe_allow_html=True)



# ===========================
# ===========================
# KPIs PRINCIPALES
# ===========================
col1, col2, col3, col4 = st.columns(4)

# Calcular métricas
stock_total = data_detalle['Stock'].sum()
cajas_totales = int(stock_total / 10)  # 10 unidades por caja
camiones_total = data_detalle['Camion'].sum()
pallets_total = data_detalle['Pallet'].sum()

# KPI 1: CAJAS (NUEVO)
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span style="font-size: 2rem;">📦</span>
                STOCK TOTAL CAJAS
            </div>
            <div class="big-number">{cajas_totales:,}</div>
            <div class="metric-delta">
                ▲ {stock_total:,} unidades
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI 2: STOCK (emoji cambiado a lata)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span style="font-size: 2rem;">🥫</span>
                STOCK TOTAL UND
            </div>
            <div class="big-number">{stock_total:,}</div>
            <div class="metric-delta">
                ▲ Jurel en conserva
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI 3: CAMIONES (sin cambios)
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span style="font-size: 2rem;">🚛</span>
                CAMIONES
            </div>
            <div class="big-number">{camiones_total:.2f}</div>
            <div class="metric-delta">
                ▲ Capacidad total
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI 4: PALLETS (sin cambios)
with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <span style="font-size: 2rem;">📐</span>
                TOTAL PALLETS
            </div>
            <div class="big-number">{pallets_total:.2f}</div>
            <div class="metric-delta">
                ▲ Espacio ocupado
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===========================

# GRÁFICOS MEJORADOS CON COLORES TEMÁTICOS
# ===========================
st.markdown("## 📊 Análisis de Distribución")

col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown("### 📦 Distribución por Cajas")
    
    data_resumen_fmt = data_resumen.copy()
    data_resumen_fmt['Material'] = data_resumen_fmt['Material'].astype(str).str.replace(',', '')
    
    # ===========================
    # NUEVO: Calcular CAJAS por producto
    # ===========================
    data_resumen_fmt['Cajas'] = (data_resumen_fmt['Stock'] / 10).round(0).astype(int)
    
    # Colores temáticos: Verde para Natural, Rojo tomate para Picante
    colores_productos = {
        'JUREL FIL NATURAL PRINCES 125G EU': '#00D9A3',     # Verde agua brillante
        'JUREL FIL TOM PICANTE PRINCES 125G EU': '#FF4757'  # Rojo tomate
    }
    
    colors = [colores_productos.get(prod, '#06D6A0') for prod in data_resumen_fmt['Producto']]
    
    # ===========================
    # CAMBIO: Usar 'Cajas' en lugar de 'Stock'
    # ===========================
    fig_pastel = go.Figure(data=[go.Pie(
        labels=data_resumen_fmt['Producto'],
        values=data_resumen_fmt['Cajas'],  # ← CAMBIO: ahora muestra CAJAS
        hole=0.55,
        marker=dict(
            colors=colors,
            line=dict(color='#0a0e27', width=4)
        ),
        textinfo='percent+label',
        textposition='inside',
        textfont=dict(
            size=14,
            color='white',
            family="Arial Black"
        ),
        # ===========================
        # HOVER mejorado: Muestra Cajas
        # ===========================
        hovertemplate='<b>%{label}</b><br>Cajas: %{value:,}<br>Porcentaje: %{percent}<extra></extra>',
        pull=[0.05, 0.05]  # Separar ligeramente las secciones
    )])
    
    # ===========================
    # ===========================
    # Texto central: SOLO número
    # ===========================
    total_cajas = data_resumen_fmt['Cajas'].sum()
    fig_pastel.add_annotation(
        text=f"<b>{total_cajas:,}</b>",
        x=0.5, y=0.5,
        font=dict(size=28, color='#06D6A0', family="Arial Black"),
        showarrow=False
    )
    
    fig_pastel.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='#e0e0e0', size=12, family="Arial"),
            bgcolor='rgba(26, 26, 46, 0.6)',
            bordercolor='rgba(6, 214, 160, 0.3)',
            borderwidth=1
        ),
        height=480,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12, color='#e0e0e0'),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig_pastel, use_container_width=True)


with col_der:
    st.markdown("### 📊 Comparación Visual de Productos")
    
    # Crear gráfico de barras horizontal con gradiente
    fig_barras = go.Figure()
    
    for idx, row in data_resumen_fmt.iterrows():
        # Colores según producto
        if 'NATURAL' in row['Producto']:
            color = '#00D9A3'
            color_hover = '#00FFBB'
        else:
            color = '#FF4757'
            color_hover = '#FF6B7A'
        
        fig_barras.add_trace(go.Bar(
            y=[row['Producto']],
            x=[row['Stock']],
            name=row['Producto'],
            orientation='h',
            text=f"<b>{row['Stock']:,}</b>",
            textposition='outside',
            textfont=dict(
                size=16,
                color=color,
                family="Arial Black"
            ),
            marker=dict(
                color=color,
                line=dict(color=color_hover, width=2),
                opacity=0.9,
                pattern=dict(
                    shape="/",
                    bgcolor='rgba(0,0,0,0.2)',
                    size=8,
                    solidity=0.3
                )
            ),
            hovertemplate='<b>%{y}</b><br>Stock: %{x:,} unidades<extra></extra>',
            showlegend=False
        ))
    
    fig_barras.update_layout(
        xaxis_title="<b>Stock (Unidades)</b>",
        yaxis_title="",
        height=480,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 26, 46, 0.3)',
        font=dict(family="Arial, sans-serif", size=12, color='#e0e0e0'),
        xaxis=dict(
            gridcolor='rgba(6, 214, 160, 0.15)',
            showgrid=True,
            tickfont=dict(size=12, color='#b0b0b0', family="Arial"),
            title_font=dict(size=14, color='#06D6A0', family="Arial Black")
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='#e0e0e0', family="Arial"),
            showgrid=False
        ),
        margin=dict(t=20, b=60, l=20, r=100),
        bargap=0.3
    )
    
    # Añadir línea de objetivo o promedio
    promedio = data_resumen_fmt['Stock'].mean()
    fig_barras.add_vline(
        x=promedio,
        line_dash="dash",
        line_color="rgba(6, 214, 160, 0.5)",
        line_width=2,
        annotation_text=f"Promedio: {promedio:,.0f}",
        annotation_position="top",
        annotation_font=dict(size=11, color='#06D6A0')
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)

# Espacio adicional
st.markdown("<br>", unsafe_allow_html=True)


# ===========================
# MINI INSIGHTS - CORREGIDO DEFINITIVAMENTE
# ===========================
col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    # ORDENAR por stock de MAYOR a MENOR y tomar el primero
    data_ordenado = data_resumen_fmt.sort_values('Stock', ascending=False).reset_index(drop=True)
    producto_max = data_ordenado.iloc[0]  # El de MAYOR stock
    
    porcentaje = (producto_max['Stock'] / data_resumen_fmt['Stock'].sum()) * 100
    
    # Determinar color según el producto
    if 'NATURAL' in producto_max['Producto']:
        color_borde = '#00D9A3'
        color_texto = '#00D9A3'
        nombre_corto = "JUREL NATURAL"
    else:
        color_borde = '#FF4757'
        color_texto = '#FF4757'
        nombre_corto = "JUREL TOMATE PICANTE"
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
            border-left: 4px solid {color_borde};
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 
                0 6px 20px rgba(0, 0, 0, 0.4),
                0 0 15px {color_borde}33;
        ">
            <p style="color: #b0b0b0; font-size: 0.9rem; margin: 0 0 0.5rem 0; text-transform: uppercase; font-weight: 600;">
                🐟 Producto Dominante
            </p>
            <p style="
                color: {color_texto}; 
                font-size: 2.2rem; 
                font-weight: 900; 
                margin: 0.5rem 0;
                text-shadow: 0 0 15px {color_borde}66;
            ">
                {porcentaje:.1f}%
            </p>
            <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0.5rem 0 0 0; font-weight: 600;">
                {nombre_corto}
            </p>
            <p style="color: #888; font-size: 0.8rem; margin: 0.3rem 0 0 0;">
                {producto_max['Stock']:,} unidades
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_insight2:
    # Calcular diferencia entre el mayor y menor stock
    stock_mayor = data_ordenado.iloc[0]['Stock']
    stock_menor = data_ordenado.iloc[1]['Stock']
    diff = stock_mayor - stock_menor
    porcentaje_diff = (diff / data_resumen_fmt['Stock'].sum()) * 100
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
            border-left: 4px solid #0891b2;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 
                0 6px 20px rgba(0, 0, 0, 0.4),
                0 0 15px rgba(8, 145, 178, 0.2);
        ">
            <p style="color: #b0b0b0; font-size: 0.9rem; margin: 0 0 0.5rem 0; text-transform: uppercase; font-weight: 600;">
                📊 Diferencia de Stock
            </p>
            <p style="
                color: #0891b2; 
                font-size: 2.2rem; 
                font-weight: 900; 
                margin: 0.5rem 0;
                text-shadow: 0 0 15px rgba(8, 145, 178, 0.4);
            ">
                {diff:,}
            </p>
            <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0.5rem 0 0 0; font-weight: 600;">
                unidades de diferencia
            </p>
            <p style="color: #888; font-size: 0.8rem; margin: 0.3rem 0 0 0;">
                {porcentaje_diff:.1f}% del stock total
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


# ===========================
# TABLA FIFO MEJORADA - 50 LOTES + COLUMNA CAJAS
# ===========================
st.markdown("## 🚨 Prioridad de Despacho FIFO")

# Tomar top 50 lotes (en lugar de 15)
data_fifo_fmt = data_fifo.head(50).copy()
data_fifo_fmt['Material'] = data_fifo_fmt['Material'].astype(str).str.replace(',', '')

# Agregar columna de CAJAS
data_fifo_fmt['Cajas'] = (data_fifo_fmt['Stock'] / 10).round(0).astype(int)

# Función para colorear alertas
def get_color(dias):
    if dias > 10:
        return '🔴'
    elif dias > 5:
        return '🟡'
    else:
        return '🟢'

data_fifo_fmt['Alerta'] = data_fifo_fmt['Dias'].apply(get_color)

# Columnas a mostrar (con CAJAS nueva)
columnas_mostrar = ['Alerta', 'Prioridad', 'Material', 'Producto', 'Lote', 
                    'Fecha_Produccion', 'Dias', 'Stock', 'Cajas', 
                    'Stock_Acumulado', 'Pallet', 'Camiones_Acumulados']

# Mostrar tabla con más altura para 50 lotes
st.dataframe(
    data_fifo_fmt[columnas_mostrar],
    use_container_width=True,
    height=650,  # Aumentado de 520 a 650
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)


# Resumen FIFO CON SOMBRAS Y FORMATO PREMIUM
st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 1.8rem;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(255, 107, 122, 0.15);
            border-left: 5px solid #FF4757;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <p style="
                color: #b0b0b0; 
                font-size: 0.85rem; 
                margin: 0 0 1rem 0; 
                text-transform: uppercase; 
                font-weight: 700;
                letter-spacing: 1.5px;
                text-shadow: 0 2px 5px rgba(0,0,0,0.5);
            ">
                🎯 Lotes en Top 50
            </p>
            <p style="
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(135deg, #FF4757 0%, #FF6B7A 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                filter: drop-shadow(0 4px 15px rgba(255, 71, 87, 0.4));
                line-height: 1;
            ">
                {len(data_fifo_fmt)}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    stock_top15 = data_fifo_fmt['Stock'].sum()
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 1.8rem;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(6, 214, 160, 0.15);
            border-left: 5px solid #06D6A0;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <p style="
                color: #b0b0b0; 
                font-size: 0.85rem; 
                margin: 0 0 1rem 0; 
                text-transform: uppercase; 
                font-weight: 700;
                letter-spacing: 1.5px;
                text-shadow: 0 2px 5px rgba(0,0,0,0.5);
            ">
                📦 Stock Top 50
            </p>
            <p style="
                font-size: 3rem;
                font-weight: 900;
                background: linear-gradient(135deg, #06D6A0 0%, #00ffcc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                filter: drop-shadow(0 4px 15px rgba(6, 214, 160, 0.4));
                line-height: 1;
            ">
                {stock_top15:,}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_c:
    camiones_top15 = data_fifo_fmt['Camiones_Acumulados'].max()
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 1.8rem;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(8, 145, 178, 0.15);
            border-left: 5px solid #0891b2;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <p style="
                color: #b0b0b0; 
                font-size: 0.85rem; 
                margin: 0 0 1rem 0; 
                text-transform: uppercase; 
                font-weight: 700;
                letter-spacing: 1.5px;
                text-shadow: 0 2px 5px rgba(0,0,0,0.5);
            ">
                🚛 Camiones (Acum.)
            </p>
            <p style="
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(135deg, #0891b2 0%, #06D6A0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                filter: drop-shadow(0 4px 15px rgba(8, 145, 178, 0.4));
                line-height: 1;
            ">
                {camiones_top15:.2f}
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===========================
# ===========================
# INFORMACIÓN DEL SISTEMA - TÍTULO PREMIUM
# ===========================
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.2) 0%, rgba(6, 214, 160, 0.15) 100%);
        border-left: 5px solid #06D6A0;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    ">
        <h3 style="
            color: #06D6A0;
            margin: 0;
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 1px;
            text-shadow: 0 2px 8px rgba(6, 214, 160, 0.4);
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-size: 1.1rem;">📘</span>
            INFORMACIÓN DEL SISTEMA
        </h3>
    </div>
""", unsafe_allow_html=True)

with st.expander("Ver detalles del sistema", expanded=False):
    st.markdown("""
        ### Sistema de Gestión de Inventario
        
        - **FIFO:** Primero en Entrar, Primero en Salir
        - **Capacidad por Camión:** 20 pallets 
        - **Unidades por Pallet:** 4,180 unidades
        
        ### Alertas de Antigüedad:
        
        - 🔴 **Más de 10 días** (Urgente - Despachar YA)
        - 🟡 **5-10 días** (Prioridad Media)
        - 🟢 **Menos de 5 días** (Reciente)
    """)

csv = data_fifo_fmt.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Descargar Plan de Despacho (CSV)",
    data=csv,
    file_name='plan_despacho_fifo.csv',
    mime='text/csv'
)
