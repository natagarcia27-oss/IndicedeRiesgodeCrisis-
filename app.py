# app.py (Versión V2.1)

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Índice de Riesgo de Crisis",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# ESTILO
# =====================================================

st.markdown("""
<style>

.main{
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
# FUNCIONES
# =====================================================

def determinar_criticidad(irc):

    if irc < 40:
        return "ESTABLE"

    elif irc < 70:
        return "RIESGO CRECIENTE"

    else:
        return "CRÍTICO"


def escenario_dominante(estable, creciente, critico):

    escenarios = {
        "Estable": estable,
        "Riesgo creciente": creciente,
        "Crítico": critico
    }

    return max(
        escenarios,
        key=escenarios.get
    )


def generar_resumen(
        irc,
        iaam,
        escenario
):

    if escenario == "Estable":

        return f"""
El sistema evidencia condiciones de estabilidad funcional.

El Índice de Riesgo de Crisis (IRC) se ubica en {irc:.1f}%,
mientras que el Índice de Activación de Asistencia Militar
(IAAM) alcanza {iaam:.1f}%.

Los indicadores evaluados permanecen dentro de parámetros
compatibles con un escenario estable y no se identifican
factores con capacidad suficiente para generar una alteración
significativa del orden público en el corto plazo.
"""

    elif escenario == "Riesgo creciente":

        return f"""
El sistema evidencia una fase de riesgo creciente.

El IRC alcanza {irc:.1f}% y el IAAM {iaam:.1f}%.

La convergencia de factores asociados a movilización,
amplificación narrativa y conflictividad social incrementa
la probabilidad de afectaciones localizadas y exige
fortalecimiento de capacidades de monitoreo y coordinación.
"""

    else:

        return f"""
El sistema evidencia convergencia de factores críticos.

El IRC alcanza {irc:.1f}% y el IAAM {iaam:.1f}%.

La simultaneidad de múltiples factores de riesgo incrementa
la probabilidad de evolución hacia escenarios de crisis y
requiere fortalecimiento de capacidades institucionales y
mecanismos de coordinación.
"""


def generar_alerta(irc):

    if irc >= 70:

        return (
            "ALERTA CRÍTICA",
            "Convergencia de factores críticos con capacidad de escalamiento."
        )

    elif irc >= 40:

        return (
            "ALERTA PREVENTIVA",
            "Incremento de indicadores de conflictividad y movilización."
        )

    else:

        return (
            "ALERTA INFORMATIVA",
            "Condiciones generales compatibles con estabilidad funcional."
        )


def generar_recomendaciones(
        irc,
        iaam,
        escenario
):

    recomendaciones = []

    if escenario == "Estable":

        recomendaciones.extend([
            "Mantener monitoreo preventivo.",
            "Actualizar evaluación periódicamente.",
            "Conservar coordinación institucional."
        ])

    elif escenario == "Riesgo creciente":

        recomendaciones.extend([
            "Fortalecer monitoreo territorial.",
            "Incrementar coordinación interinstitucional.",
            "Monitorear dinámicas digitales y movilización."
        ])

    else:

        recomendaciones.extend([
            "Activar mecanismos reforzados de coordinación.",
            "Incrementar monitoreo estratégico.",
            "Evaluar capacidades institucionales de respuesta."
        ])

    if iaam >= 60:

        recomendaciones.append(
            "Revisar protocolos asociados a escenarios de asistencia militar."
        )

    return recomendaciones


# =====================================================
# HISTORIAL
# =====================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Gestión de Evaluación")

archivo = st.sidebar.file_uploader(
    "Cargar matriz diligenciada",
    type=["xlsx"]
)

procesar = st.sidebar.button(
    "Procesar evaluación"
)

if st.sidebar.button("Nueva evaluación"):

    st.session_state.clear()
    st.rerun()

# =====================================================
# HEADER
# =====================================================

st.title(
    "Índice de Riesgo de Crisis ante manifestaciones sociales violentas"
)

st.caption(
    "Sistema de monitoreo estratégico"
)

# =====================================================
# PROCESAMIENTO
# =====================================================

if archivo and procesar:

    try:

        hoja = pd.read_excel(
            archivo,
            sheet_name="Matriz integrada",
            header=None
        )

        fila = 66

        estable = float(hoja.iloc[fila, 4])
        creciente = float(hoja.iloc[fila, 6])
        critico = float(hoja.iloc[fila, 8])

        irc = float(hoja.iloc[fila, 10])
        iaam = float(hoja.iloc[fila, 12])

        criticidad = determinar_criticidad(
            irc
        )

        escenario = escenario_dominante(
            estable,
            creciente,
            critico
        )

        resumen = generar_resumen(
            irc,
            iaam,
            escenario
        )

        alerta_titulo, alerta_texto = generar_alerta(
            irc
        )

        recomendaciones = generar_recomendaciones(
            irc,
            iaam,
            escenario
        )

        st.session_state.historial.append({
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "IRC": irc,
            "IAAM": iaam,
            "Escenario": escenario
        })

        # ============================================
        # KPI
        # ============================================

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            st.metric(
                "IRC",
                f"{irc:.1f}%"
            )

        with c2:
            st.metric(
                "IAAM",
                f"{iaam:.1f}%"
            )

        with c3:
            st.metric(
                "Escenario",
                escenario
            )

        with c4:
            st.metric(
                "Criticidad",
                criticidad
            )

        # ============================================
        # RESUMEN
        # ============================================

        st.subheader(
            "Resumen Ejecutivo Automatizado"
        )

        st.info(
            resumen
        )

        # ============================================
        # ALERTA
        # ============================================

        st.subheader(
            "Alertas Tempranas"
        )

        st.warning(
            f"{alerta_titulo}: {alerta_texto}"
        )

        # ============================================
        # ESCENARIOS
        # ============================================

        col1,col2 = st.columns(2)

        with col1:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Estable",
                            "Riesgo creciente",
                            "Crítico"
                        ],
                        values=[
                            estable,
                            creciente,
                            critico
                        ],
                        hole=0.55
                    )
                ]
            )

            fig.update_layout(
                title="Distribución de Escenarios"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig2 = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=iaam,
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

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        # ============================================
        # DEFINICIONES
        # ============================================

        st.caption(
            """
IRC: Índice de Riesgo de Crisis

IAAM: Índice de Activación de Asistencia Militar
"""
        )

        # ============================================
        # RECOMENDACIONES
        # ============================================

        st.subheader(
            "Recomendaciones Estratégicas"
        )

        for r in recomendaciones:

            st.success(
                r
            )

        # ============================================
        # HISTORIAL
        # ============================================

        st.subheader(
            "Historial de Evaluaciones"
        )

        st.dataframe(
            pd.DataFrame(
                st.session_state.historial
            ),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Error procesando matriz: {e}"
        )

else:

    st.info(
        "Cargue una matriz diligenciada y pulse 'Procesar evaluación'."
    )
```
