import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="IRC Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# ESTILO
# =====================================================

st.markdown("""
<style>
.main {
    background-color:#0B1118;
}
[data-testid="stMetricValue"]{
    font-size:2rem;
}
.block-container{
    padding-top:1rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CARGA DE DATOS
# =====================================================

ARCHIVO_EXCEL = "data/Matriz_indicadores.xlsx"

@st.cache_data
def cargar_datos():

    categorias = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name="Categorias"
    )

    matriz = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name="Matriz integrada"
    )

    criticidad = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name="Nivel de criticidad"
    )

    iaam_tabla = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name="Probabilidad asistencia militar"
    )

    return categorias, matriz, criticidad, iaam_tabla


try:
    categorias, matriz, criticidad, iaam_tabla = cargar_datos()

except Exception as e:
    st.error(f"Error cargando Excel: {e}")
    st.stop()

# =====================================================
# VALORES ACTUALES
# (reemplazar posteriormente por cálculo automático)
# =====================================================

IRC = 2.9
IAAM = 3.2

ESCENARIO = "Estabilidad funcional"

INDICADORES_CRITICOS = 0

# =====================================================
# HEADER
# =====================================================

st.title(
    "Índice de Riesgo de Crisis ante manifestaciones sociales violentas"
)

st.caption(
    "Sistema de monitoreo estratégico"
)

st.success(
    "ALERTA VERDE · Estabilidad funcional"
)

# =====================================================
# KPI
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "IRC",
        f"{IRC:.1f}%"
    )

with c2:
    st.metric(
        "IAAM",
        f"{IAAM:.1f}%"
    )

with c3:
    st.metric(
        "Escenario",
        ESCENARIO
    )

with c4:
    st.metric(
        "Indicadores críticos",
        INDICADORES_CRITICOS
    )

# =====================================================
# RESUMEN EJECUTIVO
# =====================================================

st.subheader("Resumen Ejecutivo Automatizado")

st.info("""
El sistema evidencia condiciones de estabilidad funcional.
No se observan señales de convergencia suficientes para una
crisis de orden público de carácter nacional.
La capacidad institucional permanece dentro de parámetros normales.
""")

# =====================================================
# TENDENCIA TEMPORAL
# =====================================================

st.subheader("Tendencia Temporal IRC · IAAM")

dias = [
    "D1",
    "D5",
    "D10",
    "D15",
    "D20",
    "D25",
    "D30"
]

irc_hist = [
    1.2,
    1.5,
    1.8,
    2.0,
    2.4,
    2.7,
    2.9
]

iaam_hist = [
    1.1,
    1.4,
    1.7,
    2.0,
    2.4,
    2.8,
    3.2
]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dias,
        y=irc_hist,
        mode="lines+markers",
        name="IRC"
    )
)

fig.add_trace(
    go.Scatter(
        x=dias,
        y=iaam_hist,
        mode="lines+markers",
        name="IAAM"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption("""
IRC: Índice de Riesgo de Crisis

IAAM: Índice de Activación de Asistencia Militar
""")

# =====================================================
# DISTRIBUCIÓN DE ESCENARIOS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Distribución de Escenarios")

    fig2 = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Estable",
                    "Riesgo creciente",
                    "Crítico"
                ],
                values=[
                    100,
                    0,
                    0
                ],
                hole=0.55
            )
        ]
    )

    fig2.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    st.subheader("Asistencia Militar")

    fig3 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=IAAM,
            title={
                "text":"IAAM"
            },
            gauge={
                "axis":{
                    "range":[0,100]
                }
            }
        )
    )

    fig3.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================================
# CATEGORÍAS
# =====================================================

st.subheader("Riesgo por Categoría")

st.dataframe(
    categorias,
    use_container_width=True
)

# =====================================================
# ALERTAS
# =====================================================

st.subheader("Alertas Tempranas")

st.warning(
    "No se registran alertas críticas activas."
)

# =====================================================
# ACTORES
# =====================================================

st.subheader("Actores Relevantes")

a1,a2 = st.columns(2)

with a1:

    st.markdown("""
    **Movimientos sociales**

    - Capacidad movilizadora: Baja
    - Tendencia: Estable
    """)

    st.markdown("""
    **Actores políticos**

    - Polarización: Moderada
    - Tendencia: Estable
    """)

with a2:

    st.markdown("""
    **Plataformas digitales**

    - Actividad: Baja
    - Tendencia: Estable
    """)

# =====================================================
# MATRIZ DE ESCALAMIENTO
# =====================================================

st.subheader("Matriz de Escalamiento")

st.dataframe(
    matriz.head(20),
    use_container_width=True
)

# =====================================================
# RECOMENDACIONES
# =====================================================

st.subheader("Recomendaciones Estratégicas")

st.success("""
• Mantener monitoreo preventivo.

• Continuar coordinación institucional.

• Actualizar evaluación semanal.
""")

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "IRC Dashboard · Sistema de monitoreo estratégico"
)
```
