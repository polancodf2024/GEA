import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from pathlib import Path
import paramiko
import toml

def main():
    # ===== FUNCIONES DE ACCESO REMOTO =====
    def cargar_configuracion():
        """Carga la configuración desde secrets.toml"""
        try:
            config = dict(st.secrets)
            if config.get('remote_host'):
                return config
        except:
            try:
                secrets_path = Path('.streamlit') / 'secrets.toml'
                with open(secrets_path, 'r') as f:
                    return toml.load(f)
            except Exception as e:
                st.error(f"Error de configuración: {e}")
                return None

    def contar_registros_remotos():
        """Obtiene el conteo de registros desde el servidor remoto usando nombres de archivos desde secrets"""
        config = cargar_configuracion()
        if not config:
            return None

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=config['remote_host'],
                port=config['remote_port'],
                username=config['remote_user'],
                password=config['remote_password']
            )

            # Usamos los nombres de archivo definidos en secrets.toml
            archivos = {
                "Artículos": config['remote_file_art'],
                "Tesis": config['remote_file_tes'],
                "Congresos": config['remote_file_con'],
                "Financiamientos": config['remote_file_fin']
            }

            resultados = []
            for nombre, archivo in archivos.items():
                comando = f"if [ -f {config['remote_dir']}/{archivo} ]; then wc -l {config['remote_dir']}/{archivo} | awk '{{print $1}}'; else echo 0; fi"
                stdin, stdout, stderr = ssh.exec_command(comando)
                output = stdout.read().decode().strip()
                count = int(output) if output else 0
                resultados.append({"Tipo": nombre, "Registros": count})

            ssh.close()
            return pd.DataFrame(resultados)

        except Exception as e:
            st.error(f"Conexión fallida: {str(e)}")
            return None

    # ===== CONFIGURACIÓN DE PÁGINA =====
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
        .stats-table {{ margin: 1rem 0; font-size: 0.9em; }}
    </style>
    """, unsafe_allow_html=True)

    # Función para cargar imágenes
    def load_image_with_fallback(main_path, alternative_names):
        paths_to_try = [main_path] + alternative_names
        for img_path in paths_to_try:
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.verify()
                    img = Image.open(img_path)
                    return img, None
            except (IOError, SyntaxError, Exception):
                continue
        return None, f"No se encontró imagen válida en: {', '.join(paths_to_try)}"

    # ===== INTERFAZ PRINCIPAL =====
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

    # ===== ESTADÍSTICAS REMOTAS =====
    with st.expander("📈 Estadísticas de Registros", expanded=False):
        st.markdown("""
        <div class="card">
            <h3 style="color: #6a0f1a; margin-bottom: 0.5rem;">Registros almacenados</h3>
            <div class="stats-table">
        """, unsafe_allow_html=True)
        
        df_stats = contar_registros_remotos()
        if df_stats is not None:
            st.table(df_stats.assign(hack='').set_index('hack'))
            total = df_stats['Registros'].sum()
            st.markdown(f"""
            <div style="margin-top: 0.5rem; font-weight: bold; text-align: right;">
                Total registros: <span style="color: #6a0f1a;">{total}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No se pudo conectar al servidor remoto")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")

    # ===== HISTOGRAMA DINÁMICO =====
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Distribución de Registros")
        
        df_stats = contar_registros_remotos()
        
        if df_stats is not None:
            # Creamos el gráfico con los datos reales
            fig = px.bar(df_stats, x='Tipo', y='Registros',
                         title="Registros por categoría",
                         color='Tipo',
                         color_discrete_sequence=[color_guinda, color_marrón, color_verde_pardo, "#4B3621"],
                         text='Registros',
                         labels={'Tipo': 'Categoría', 'Registros': 'Número de Registros'})
            
            fig.update_traces(textposition='outside', 
                             marker_line_color='rgb(8,48,107)',
                             marker_line_width=1.5)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title=None,
                yaxis_title="Cantidad de Registros",
                showlegend=False,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas resumidas
            total_registros = df_stats['Registros'].sum()
            st.markdown(f"""
            **Resumen estadístico:**
            - Total registros: **{total_registros}**
            - Categoría con más registros: **{df_stats.loc[df_stats['Registros'].idxmax(), 'Tipo']}** ({df_stats['Registros'].max()})
            - Categoría con menos registros: **{df_stats.loc[df_stats['Registros'].idxmin(), 'Tipo']}** ({df_stats['Registros'].min()})
            """)
        else:
            st.warning("No se pudieron cargar los datos para el histograma")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ===== SECCIONES DE CONTENIDO =====
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

    # Sección de Metodología
    with st.container():
        st.header("🔍 Metodología del Estudio GEA")
        
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
                    caption="Flujo metodológico del estudio GEA", 
                    use_container_width=True
                )
                st.markdown("""
                **Componentes principales:**
                - Población mexicana con evaluación integral
                - Análisis bioquímicos y antropométricos
                - Estudios de imagenología cardiovascular
                - Evaluación genética con 256 marcadores
                - Cuestionarios estandarizados de factores de riesgo
                """)
            except Exception as e:
                st.error(f"Error al mostrar la imagen: {str(e)}")
        else:
            st.warning(error)
            st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Sube diagrama de metodología", type=["jpg", "jpeg", "png"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_file:
                try:
                    img = Image.open(uploaded_file)
                    st.image(img, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al procesar imagen: {str(e)}")

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

    # Responsables (versión minimalista)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0;">
        <h3 style="color: #6a0f1a; margin-bottom: 0.5rem;">Responsables</h3>
        <p style="margin: 0.25rem 0;">Dra. Rosalinda Posadas Sánchez</p>
        <p style="margin: 0.25rem 0;">Dr. Gilberto Vargas Alarcón</p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de Contacto
    st.markdown("---")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📬 Contacto")
        st.markdown("""
        <div style="margin: 1rem 0; line-height: 1.6;">
            <p style="margin-bottom: 0.5rem;">Para más información sobre el estudio GEA:</p>
            <div style="background: #f0f0f0; padding: 0.75rem; border-radius: 6px; margin: 0.5rem 0;">
                <p style="margin: 0;"><strong>Dra. Rosalinda Posadas Sánchez</strong><br>
                <small>rosalinda.posadas@cardiologia.org.mx</small></p>
            </div>
            <div style="background: #f0f0f0; padding: 0.75rem; border-radius: 6px; margin: 0.5rem 0;">
                <p style="margin: 0;"><strong>Dr. Gilberto Vargas Alarcón</strong><br>
                <small>gilberto.vargas@cardiologia.org.mx</small></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
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
