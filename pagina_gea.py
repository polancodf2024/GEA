import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    # Configuración minimalista de la página
    st.set_page_config(
        page_title="GEA - Genética de la Enfermedad Aterosclerótica",
        layout="centered",
        page_icon="🧬"
    )

    # Paleta de colores oficiales
    color_guinda = "#6a0f1a"
    color_marrón = "#8B4513"
    color_verde_pardo = "#6B8E23"
    color_fondo = "#f9f5f5"

    # CSS personalizado minimalista
    st.markdown(f"""
    <style>
        body {{
            font-family: 'Arial', sans-serif;
        }}
        .stApp {{
            background-color: {color_fondo};
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            color: {color_guinda};
            border-bottom: 2px solid {color_marrón};
            padding-bottom: 8px;
        }}
        h2 {{
            color: {color_guinda};
            font-size: 1.3em;
        }}
        .footer {{
            background-color: {color_guinda};
            color: white;
            padding: 1rem;
            margin-top: 3rem;
            text-align: center;
            border-radius: 4px;
        }}
        .card {{
            background-color: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid {color_marrón};
        }}
        .mission-icon {{
            font-size: 1.5rem;
            margin-right: 0.5rem;
            color: {color_guinda};
        }}
        .value-item {{
            margin-bottom: 0.8rem;
            display: flex;
            align-items: flex-start;
        }}
        .value-icon {{
            margin-right: 0.8rem;
            color: {color_marrón};
        }}
    </style>
    """, unsafe_allow_html=True)

    # Logo y encabezado
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("escudo_COLOR.jpg", width=100)
    with col2:
        st.title("GEA")
        st.caption("Estudio Genética de la Enfermedad Aterosclerótica")

    st.markdown("---")

    # Sección de Identidad Institucional
    with st.container():
        st.header("Identidad Institucional")
        
        # Misión
        with st.expander("🧭 **Misión**", expanded=True):
            st.markdown("""
            > *"Investigar los factores genéticos, bioquímicos y ambientales que contribuyen al desarrollo de la aterosclerosis en la población mexicana, 
            para mejorar el diagnóstico temprano, la prevención y el tratamiento personalizado de enfermedades cardiovasculares."*
            """)
        
        # Visión
        with st.expander("🔭 **Visión**", expanded=True):
            st.markdown("""
            > *"Ser referente científico en América Latina en el estudio de la aterosclerosis, integrando investigación genómica, 
            herramientas diagnósticas innovadoras y medicina traslacional para reducir la incidencia de enfermedades cardiovasculares."*
            """)

    # Valores y Servicios en dos columnas
    col_valores, col_servicios = st.columns(2)
    
    with col_valores:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📜 Valores")
            st.markdown("""
            <div class="value-item">
                <span class="value-icon">🔬</span>
                <span><strong>Excelencia científica</strong>: Rigor metodológico en investigación</span>
            </div>
            <div class="value-item">
                <span class="value-icon">🌐</span>
                <span><strong>Enfoque multidisciplinario</strong>: Integración de genética, bioquímica y clínica</span>
            </div>
            <div class="value-item">
                <span class="value-icon">❤️</span>
                <span><strong>Impacto social</strong>: Salud cardiovascular en México</span>
            </div>
            <div class="value-item">
                <span class="value-icon">💡</span>
                <span><strong>Innovación</strong>: Tecnologías genómicas avanzadas</span>
            </div>
            <div class="value-item">
                <span class="value-icon">⚖️</span>
                <span><strong>Ética</strong>: Transparencia y respeto a participantes</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_servicios:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🛠️ Servicios")
            st.markdown("""
            - **Diagnóstico avanzado**:
              - Perfil genético cardiovascular
              - Análisis de marcadores bioquímicos
              - Evaluación de placa aterosclerótica
            
            - **Investigación clínica**:
              - Estudios genómicos poblacionales
              - Análisis de factores de riesgo
            
            - **Programas preventivos**:
              - Estrategias personalizadas
              - Educación en salud cardiovascular
            
            - **Colaboraciones**:
              - Redes multicéntricas
              - Formación de investigadores
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # Datos del proyecto (sección original mejorada)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Proyecto GEA en cifras")
        
        # Datos para el histograma
        datos_gea = pd.DataFrame({
            'Área': ['Artículos científicos', 'Tesis', 'Congresos', 'Financiamientos'],
            'Total': [124, 15, 6, 5]
        })
        
        fig = px.bar(datos_gea, x='Área', y='Total',
                     title="Datos clave del estudio (2025)",
                     color_discrete_sequence=[color_verde_pardo],
                     text='Total')
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title=None,
            yaxis_title="Cantidad",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Características únicas:**
        - 2,740 participantes mexicanos
        - 256 marcadores de ancestría
        - Protocolo integrado (genética + imagenología)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Pie de página
    st.markdown("---")
    st.markdown(
        f'<div class="footer">'
        '© 2025 Proyecto GEA | Instituto Nacional de Cardiología Ignacio Chávez'
        '</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
