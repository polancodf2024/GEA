import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    # Configuración minimalista de la página
    st.set_page_config(
        page_title="GEA - Genética de la Enfermedad Aterosclerótica",
        layout="centered",
        page_icon="❤️"
    )

    # Paleta de colores oficiales
    color_guinda = "#6a0f1a"
    color_marrón = "#8B4513"
    color_verde_pardo = "#6B8E23"  # Verde pardo/oliva
    color_fondo = "#f9f5f5"

    # CSS personalizado minimalista
    st.markdown(f"""
    <style>
        /* Eliminar el cero en la esquina superior izquierda */
        .stApp > header > div > div > div > div > div > small {{
            display: none;
        }}
        
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
        .proyecto-header {{
            color: {color_guinda};
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .proyecto-item {{
            margin-bottom: 0.5rem;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Logo y encabezado minimalista
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("escudo_COLOR.jpg", width=100)
    with col2:
        st.title("OASIS")
        st.caption("Observatorio de Avances en Genética de la Enfermedad Aterosclerótica")

    st.markdown("---")

    # Contenido principal minimalista
    with st.container():
        st.markdown("""
        **Investigación clínica** enfocada en el avance del conocimiento genético cardiovascular 
        mediante metodologías innovadoras y colaboración multidisciplinaria.
        """)

    # Tarjetas de información esencial
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Líneas Estratégicas")
        st.markdown("""
        - Epidemiología cardiovascular avanzada
        - Ensayos clínicos traslacionales
        - Desarrollo de guías basadas en evidencia
        - Formación de investigadores clínicos
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Proyecto GEA con histograma
        st.markdown('<p class="proyecto-header">📊 Proyecto GEA en cifras</p>', unsafe_allow_html=True)
        
        # Datos para el histograma
        datos_productos = pd.DataFrame({
            'Tipo': ['Artículos', 'Congresos', 'Tesis', 'Financiamientos'],
            'Cantidad': [100, 8, 29, 5]
        })
        
        # Histograma con verde pardo
        fig = px.bar(datos_productos, x='Tipo', y='Cantidad',
                     title="Distribución de productos académicos (2020-2023)",
                     color_discrete_sequence=[color_verde_pardo],
                     text='Cantidad')
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title=None,
            yaxis_title="Cantidad",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Actualización cifras GEA
        st.markdown("""
        **Actualización cifras GEA (2025):**
        - 42 investigadores participantes
        - 15 instituciones colaboradoras
        - 3 patentes en proceso
        - $2.8M MXN en financiamiento obtenido
        """)
        
        # Separador visual
        st.markdown("---")
        
        # Otros proyectos - AHORA CON MEJOR FORMATO
        st.markdown("""
        <div class="proyecto-item">🔍 <strong>REGISTRO MEX-AMI</strong>: Caracterización del infarto agudo en población mexicana</div>
        <div class="proyecto-item">💻 <strong>PLATAFORMA DIGITAL</strong>: Herramientas para investigación multicéntrica</div>
        <div class="proyecto-item">📊 <strong>PROYECTO GEA</strong>: Actualización numeralia</div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Pie de página minimalista
    st.markdown("---")
    st.markdown(
        f'<div class="footer">'
        '© 2023 Dirección de Investigación | Instituto Nacional de Cardiología Ignacio Chávez'
        '</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
