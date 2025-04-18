import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from pathlib import Path

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="GEA - Genética de la Enfermedad Aterosclerótica",
        layout="centered",
        page_icon="🧬"
    )

    # Paleta de colores
    color_guinda = "#6a0f1a"
    color_marrón = "#8B4513"
    color_verde_pardo = "#6B8E23"
    color_fondo = "#f9f5f5"

    # CSS personalizado
    st.markdown(f"""
    <style>
        body {{ font-family: 'Arial', sans-serif; }}
        .stApp {{ background-color: {color_fondo}; max-width: 900px; margin: 0 auto; }}
        h1 {{ color: {color_guinda}; border-bottom: 2px solid {color_marrón}; padding-bottom: 8px; }}
        h2 {{ color: {color_guinda}; font-size: 1.3em; }}
        .footer {{ background-color: {color_guinda}; color: white; padding: 1rem; margin-top: 3rem; text-align: center; border-radius: 4px; }}
        .logo-container {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
        .logo-item {{ flex: 1; display: flex; align-items: center; }}
        .logo-item.left {{ justify-content: flex-start; }}
        .logo-item.right {{ justify-content: flex-end; }}
        .title-wrapper {{ flex: 2; text-align: center; }}
        .responsables {{ margin-top: 1rem; font-style: italic; text-align: center; color: {color_guinda}; }}
        .gea-title {{ margin-bottom: 0; }}
        .gea-subtitle {{ margin-top: 0; }}
        .card {{ background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }}
        .value-item {{ margin-bottom: 0.5rem; display: flex; align-items: center; }}
        .value-icon {{ margin-right: 0.5rem; font-size: 1.2em; }}
        .methodology-img {{ margin: 1.5rem 0; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .file-uploader {{ margin: 1rem 0; padding: 1rem; border: 2px dashed {color_guinda}; border-radius: 8px; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

    # Función mejorada para cargar imágenes con verificación robusta
    def load_image_with_fallback(main_path, alternative_names):
        """Versión mejorada con verificación exhaustiva y manejo de errores"""
        paths_to_try = [main_path] + alternative_names
        
        for img_path in paths_to_try:
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.verify()  # Verifica integridad del archivo
                    img = Image.open(img_path)  # Necesario reabrir después de verify
                    return img, None
            except (IOError, SyntaxError, Exception) as e:
                continue
                
        return None, f"No se encontró una imagen válida. Intentó con: {', '.join(paths_to_try)}"

    # Encabezado con logos
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        try:
            logo_izq = Image.open("escudo_COLOR.jpg")
            st.image(logo_izq, width=100)
        except Exception as e:
            st.error(f"No se pudo cargar el logo izquierdo: {str(e)}")

    with col2:
        st.markdown('<h1 class="gea-title">GEA</h1>', unsafe_allow_html=True)
        st.markdown('<p class="gea-subtitle">Estudio Genética de la Enfermedad Aterosclerótica</p>', unsafe_allow_html=True)

    with col3:
        try:
            logo_der = Image.open("UTF-8IMG-20250417-WA0007.jpg")
            st.image(logo_der, width=100)
        except Exception as e:
            st.error(f"No se pudo cargar el logo derecho: {str(e)}")

    st.markdown("---")

    # Sección de Identidad Institucional
    with st.container():
        st.header("Identidad Institucional")
        
        with st.expander("🧭 **Misión**", expanded=True):
            st.markdown("""
            > *"Investigar los factores genéticos, bioquímicos y ambientales que contribuyen al desarrollo de la aterosclerosis en la población mexicana, 
            para mejorar el diagnóstico temprano, la prevención y el tratamiento personalizado de enfermedades cardiovasculares."*
            """)
        
        with st.expander("🔭 **Visión**", expanded=True):
            st.markdown("""
            > *"Ser referente científico en América Latina en el estudio de la aterosclerosis, integrando investigación genómica, 
            herramientas diagnósticas innovadoras y medicina traslacional para reducir la incidencia de enfermedades cardiovasculares."*
            """)

    # Sección de Metodología con manejo robusto de imágenes
    with st.container():
        st.header("🔍 Metodología del Estudio GEA")
        
        # Intento de carga de imagen con múltiples alternativas
        img, error = load_image_with_fallback(
            main_path="UTF-8IMG-20250417-WA0004.jpg",
            alternative_names=[
                "metodologia_gea.jpg",
                "diagrama_gea.jpg",
                "metodologia.jpg",
                "diagrama.jpg",
                "gea_metodologia.jpg"
            ]
        )
        
        if img:
            try:
                st.image(
                    img, 
                    caption="Flujo metodológico del estudio GEA: población, análisis y componentes", 
                    use_container_width=True,
                    output_format="auto"
                )
                
                st.markdown("""
                **Componentes principales del estudio:**
                - Población mexicana con evaluación integral
                - Análisis bioquímicos y antropométricos
                - Estudios de imagenología cardiovascular
                - Evaluación genética con 256 marcadores
                - Cuestionarios estandarizados de factores de riesgo
                """)
            except Exception as e:
                st.error(f"Error al mostrar la imagen: {str(e)}")
                st.warning("Por favor verifica que el archivo de imagen no esté corrupto")
        else:
            st.warning(error)
            
            # Opción de subir la imagen manualmente
            st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Sube aquí el diagrama de metodología", type=["jpg", "jpeg", "png"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_file:
                try:
                    img = Image.open(uploaded_file)
                    st.image(img, use_container_width=True)
                    st.success("¡Imagen cargada correctamente!")
                except Exception as e:
                    st.error(f"Error al procesar la imagen subida: {str(e)}")

    # Valores y Servicios
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

    # Datos del proyecto
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Proyecto GEA en cifras")
        
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

    # Responsables
    st.markdown("""
    <div class="responsables">
        <strong>Responsables:</strong><br>
        Dra. Rosalinda Posadas Sánchez<br>
        Dr. Gilberto Vargas Alarcón
    </div>
    """, unsafe_allow_html=True)

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
