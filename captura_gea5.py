import toml
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
import paramiko
from scp import SCPClient
import streamlit as st
from pathlib import Path
from PIL import Image

# Cargar configuración desde secrets.toml
def cargar_configuracion():
    try:
        config = dict(st.secrets)
        if config.get('smtp_server'):
            return config
    except:
        try:
            secrets_path = Path('.streamlit') / 'secrets.toml'
            with open(secrets_path, 'r') as f:
                config = toml.load(f)
            return config
        except Exception as e:
            st.error(f"Error al cargar configuración: {e}")
            st.stop()

# Función para verificar/crear archivo remoto y agregar contenido
def gestionar_archivo_remoto(config, archivo_remoto, contenido):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=config['remote_host'],
            port=config['remote_port'],
            username=config['remote_user'],
            password=config['remote_password']
        )
        
        ruta_completa = f"{config['remote_dir']}/{archivo_remoto}"
        
        stdin, stdout, stderr = ssh.exec_command(f"test -f {ruta_completa} && echo 'exists' || echo 'not exists'")
        existe = stdout.read().decode().strip()
        
        if existe == 'not exists':
            ssh.exec_command(f"echo 'Archivo de registros creado automáticamente' > {ruta_completa}")
        
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ssh.exec_command(f"echo '\n--- Registro del {fecha} ---\n{contenido}\n' >> {ruta_completa}")
        
        ssh.close()
        return True
    except Exception as e:
        st.error(f"Error al gestionar archivo remoto: {e}")
        return False

# Función para enviar notificación por email
def enviar_notificacion(config, tipo_registro, contenido):
    try:
        msg = EmailMessage()
        msg['From'] = config['email_user']
        msg['To'] = config['notification_email']
        msg['Subject'] = f"Nuevo registro de {tipo_registro} capturado"
        
        cuerpo = f"Se ha capturado un nuevo {tipo_registro} con el siguiente contenido:\n\n{contenido}\n"
        cuerpo += f"\nFecha de registro: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        msg.set_content(cuerpo)
        
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['email_user'], config['email_password'])
            server.send_message(msg)
            
    except Exception as e:
        st.error(f"Error al enviar notificación por email: {e}")

# Función para mostrar formulario simplificado
def formulario_simplificado(tipo):
    formatos = {
        "art": """Ejemplo formato artículo:
Título: Nombre del artículo
Autores: Autor1, Autor2, Autor3
Revista: Nombre de la revista
Vol(No): 5(3)
Páginas: 123-135
Año: 2023
DOI: 10.xxxx/xxxx
ISSN: xxxx-xxxx
Indexación: SCI, SCOPUS""",
        
        "tes": """Ejemplo formato tesis:
Título: Título de la tesis
Autor: Nombre del autor
Tipo: Maestría/Doctorado
Director: Nombre del director
Institución: Nombre de la institución
Año: 2023
Departamento: Nombre del departamento
Programa: Nombre del programa""",
        
        "con": """Ejemplo formato congreso:
Título: Título de la presentación
Autores: Autor1, Autor2
Evento: Nombre del evento
Tipo: Nacional/Internacional
Lugar: Ciudad, País
Fecha: 2023-05-15
Memorias: Sí/No
ISBN: xxxx-xxxx-xx""",
        
        "fin": """Ejemplo formato financiamiento:
Proyecto: Nombre del proyecto
Responsable: Nombre del responsable
Fuente: Nombre de la fuente
Monto: $100,000 MXN
Periodo: 2022-2023
Clave: CLAVE-123
Tipo: Interno/Externo"""
    }
    
    titulos = {
        "art": "📄 Capturar Artículo",
        "tes": "📚 Capturar Tesis",
        "con": "🎤 Capturar Congreso",
        "fin": "💰 Capturar Financiamiento"
    }
    
    st.subheader(titulos[tipo])
    with st.form(f"form_{tipo}", clear_on_submit=True):
        st.markdown(formatos[tipo])
        contenido = st.text_area("Ingrese la referencia completa:", height=200, key=f"input_{tipo}")
        
        submitted = st.form_submit_button(f"💾 Guardar {titulos[tipo][2:]}")
        if submitted:
            if not contenido.strip():
                st.warning("Por favor ingrese el contenido del registro")
                return None
            return contenido
    return None

# Pantalla de autenticación
def autenticar(config):
    st.title("🔒 Acceso al Sistema de Captura GEA")
    password = st.text_input("Ingrese la contraseña:", type="password")
    
    if st.button("Acceder"):
        if password == config['remote_password']:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
            return False
    return False

# Configuración de la página
def main():
    st.set_page_config(
        page_title="Sistema de Captura GEA",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Verificar autenticación
    if not hasattr(st.session_state, 'autenticado'):
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        autenticar(config)
        return
    
    # Sidebar
    with st.sidebar:
        # Mostrar logo en la columna izquierda con tamaño fijo
        try:
            logo = Image.open('escudo_COLOR.jpg')
            tamaño_fijo = (160, 160)  # Tamaño fijo de 150x150 píxeles
            logo_reducido = logo.resize(tamaño_fijo)
            st.image(logo_reducido, caption="Escudo", use_container_width=False)
        except Exception as e:
            st.warning("No se pudo cargar el logo: escudo_COLOR.jpg")

        st.title("Sistema de Captura GEA")
        st.markdown("---")
        tipo = st.radio(
            "Tipo de registro:",
            ["📄 Artículo", "📚 Tesis", "🎤 Congreso", "💰 Financiamiento"],
            index=0
        )
        st.markdown("---")
        st.info("Ingrese la referencia completa en el formato sugerido")
        
        if st.button("🚪 Salir"):
            st.session_state.autenticado = False
            st.rerun()
    
    tipo_map = {
        "📄 Artículo": "art",
        "📚 Tesis": "tes",
        "🎤 Congreso": "con",
        "💰 Financiamiento": "fin"
    }
    
    contenido = formulario_simplificado(tipo_map[tipo])
    
    if contenido:
        with st.spinner("Guardando registro en servidor remoto..."):
            if gestionar_archivo_remoto(config, config[f'remote_file_{tipo_map[tipo]}'], contenido):
                st.success("✅ Registro guardado en servidor remoto con éxito!")
                enviar_notificacion(config, tipo[2:].lower(), contenido)
            else:
                st.error("❌ Error al guardar el registro en el servidor remoto")

if __name__ == "__main__":
    main()
