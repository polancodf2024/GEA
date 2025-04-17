import streamlit as st
from streamlit_option_menu import option_menu

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Subdirección de Investigación Clínica - GEA",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Definir colores exactos de la página
    color_guinda = "#6a0f1a"  # Color guinda principal
    color_guinda_claro = "#8c1a27"  # Variación más clara
    color_marrón = "#8B4513"  # Color marrón para acentos
    color_fondo = "#f5f5f5"   # Fondo claro
    color_texto = "#333333"   # Texto principal
    color_texto_claro = "#ffffff" # Texto sobre fondos oscuros

    # CSS personalizado
    st.markdown(f"""
    <style>
        /* Estilo general */
        .stApp {{
            background-color: {color_fondo};
        }}
        
        /* Barra superior */
        header[data-testid="stHeader"] {{
            background-color: {color_guinda};
            color: {color_texto_claro};
        }}
        
        /* Barra lateral */
        section[data-testid="stSidebar"] {{
            background-color: {color_guinda} !important;
        }}
        
        /* Títulos */
        h1, h2, h3 {{
            color: {color_guinda} !important;
            border-bottom: 2px solid {color_marrón};
            padding-bottom: 5px;
        }}
        
        /* Texto normal */
        p, li {{
            color: {color_texto} !important;
        }}
        
        /* Botones */
        .stButton>button {{
            background-color: {color_guinda};
            color: {color_texto_claro};
            border-radius: 4px;
            border: none;
            padding: 8px 16px;
            transition: background-color 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: {color_guinda_claro};
            color: {color_texto_claro};
        }}
        
        /* Tarjetas/secciones */
        .stMarkdown, .stExpander {{
            background-color: white;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-left: 4px solid {color_marrón};
        }}
        
        /* Menú seleccionado */
        div[data-testid="stHorizontalBlock"] > div[data-active="true"] {{
            color: {color_texto_claro} !important;
            background-color: {color_marrón} !important;
        }}
        
        /* Pie de página */
        .footer {{
            background-color: {color_guinda};
            color: {color_texto_claro};
            padding: 15px;
            margin-top: 30px;
            border-radius: 0 0 8px 8px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Barra lateral con menú de navegación
    with st.sidebar:
        # Logo (simulado)
        st.markdown(
            f'<div style="text-align: center; padding: 15px 0; border-bottom: 1px solid {color_marrón}">'
            f'<p style="color: {color_texto_claro}; font-weight: bold; font-size: 20px;">SOCIEDAD MEXICANA DE CARDIOLOGÍA</p>'
            f'<p style="color: {color_texto_claro}; font-size: 14px;">Subdirección de Investigación Clínica</p>'
            '</div>', 
            unsafe_allow_html=True
        )
        
        # Menú de navegación
        selected = option_menu(
            menu_title=None,
            options=["Inicio", "Organización", "Dirección General", 
                    "Dirección de Investigación", "Subdirección Clínica", "GEA", "Contacto"],
            icons=["house", "people", "building", "search", "clipboard2-pulse", "clipboard2-data", "envelope"],
            menu_icon="cast",
            default_index=4,
            styles={
                "container": {"padding": "0!important", "background-color": color_guinda},
                "icon": {"color": color_texto_claro, "font-size": "16px"}, 
                "nav-link": {
                    "font-size": "15px", 
                    "text-align": "left", 
                    "margin": "5px 0", 
                    "color": color_texto_claro,
                    "border-radius": "4px",
                    "padding": "8px 12px"
                },
                "nav-link-selected": {
                    "background-color": color_marrón,
                    "color": color_texto_claro,
                    "font-weight": "normal"
                },
            }
        )

    # Contenido principal
    st.image("https://www.cardiologia.org.mx/images/logo_smc.png", width=200)
    st.title("Subdirección de Investigación Clínica")
    st.subheader("Observatorio de Avances en Salud Integral y Sostenible (GEA)")
    
    # Sección descriptiva
    st.markdown("""
    **El GEA** es una iniciativa estratégica de la Sociedad Mexicana de Cardiología dedicada a la 
    generación de conocimiento científico en el área cardiovascular, con enfoque en:
    """)
    
    st.markdown("""
    - Investigación clínica traslacional
    - Epidemiología cardiovascular
    - Desarrollo de guías de práctica clínica
    - Formación de investigadores en cardiología
    """)
    
    # Líneas de investigación
    with st.expander("**Líneas de Investigación Prioritarias**", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            **Cardiopatía Isquémica**
            - Estrategias de reperfusión
            - Medicina de precisión
            - Registro nacional de SCAMEST
            
            **Insuficiencia Cardíaca**
            - Terapias avanzadas
            - Dispositivos de asistencia
            - Estrategias de manejo integral
            """)
        
        with cols[1]:
            st.markdown("""
            **Arritmias Cardiacas**
            - Ablación con nuevas tecnologías
            - Terapia de resincronización
            - Registro nacional de FA
            
            **Cardiología Preventiva**
            - Estrategias poblacionales
            - Innovación en rehabilitación
            - Tecnologías digitales
            """)
    
    # Proyectos destacados
    st.markdown("---")
    st.subheader("Proyectos Destacados GEA")
    
    proyecto1, proyecto2, proyecto3 = st.columns(3)
    
    with proyecto1:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid {color_marrón};'>
        <h4 style='color: {color_guinda};'>REGISTRO MEX-AMI</h4>
        <p>Registro mexicano de infarto agudo de miocardio con participación de 32 centros hospitalarios.</p>
        </div>
        """.format(color_guinda=color_guinda, color_marrón=color_marrón), unsafe_allow_html=True)
    
    with proyecto2:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid {color_marrón};'>
        <h4 style='color: {color_guinda};'>ESTUDIO MEX-HF</h4>
        <p>Cohorte prospectiva de insuficiencia cardíaca con seguimiento a 5 años.</p>
        </div>
        """.format(color_guinda=color_guinda, color_marrón=color_marrón), unsafe_allow_html=True)
    
    with proyecto3:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid {color_marrón};'>
        <h4 style='color: {color_guinda};'>PLATAFORMA DIGITAL</h4>
        <p>Desarrollo de sistema integrado para investigación multicéntrica.</p>
        </div>
        """.format(color_guinda=color_guinda, color_marrón=color_marrón), unsafe_allow_html=True)
    
    # Pie de página
    st.markdown(
        f'<div class="footer">'
        '<div style="text-align: center;">'
        '<p style="margin-bottom: 5px;">© 2023 Dirección de Investigación.</p>'
        '<p style="font-size: 14px; margin-top: 0;">Av. Cuauhtémoc 330, Col. Doctores, CDMX. Tel: 55 5604 2694</p>'
        '</div>'
        '</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
