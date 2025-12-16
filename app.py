import streamlit as st
from fpdf import FPDF
from datetime import date, datetime

# --- CONFIGURACIÓN DE LA EMPRESA (Extraída del documento) ---
# [span_3](start_span)[span_4](start_span)Fuentes:[span_3](end_span)[span_4](end_span)
COMPANY_INFO = {
    "name": "Security Services Kuo Sl.",
    "cif": "CIF: B86881588",
    "auth": "Empresa de seguridad autorizada por la D.G.P., Nº 4036",
    "address": "C. Chile, 8, Las Rozas de Madrid, 28290 Madrid",
    "phone": "Teléfono: (+34) 91 250 46 46",
    "email": "info@kuospain.com",
    "group": "Perteneciente al grupo empresarial Kuo Spain"
}

# --- CLASE PARA GENERAR EL PDF ---
class PDFReport(FPDF):
    def __init__(self, title_doc):
        super().__init__()
        self.title_doc = title_doc

    def header(self):
        # Logo (Simulado con texto)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'KUO', 0, 1, 'C')
        
        # [span_5](start_span)[span_6](start_span)Título del Manual[span_5](end_span)[span_6](end_span)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'MANUAL OPERATIVO PARA VIGILANTES DE SEGURIDAD', 0, 1, 'C')
        
        # Título del Anexo específico
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.title_doc, 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-35)
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 100, 100)
        
        # [span_7](start_span)Información del pie de página extraída de los documentos[span_7](end_span)
        footer_text = (
            f"{COMPANY_INFO['name']} | {COMPANY_INFO['cif']}\n"
            f"{COMPANY_INFO['auth']}\n"
            f"{COMPANY_INFO['address']} | {COMPANY_INFO['phone']}\n"
            f"Correo: {COMPANY_INFO['email']} | {COMPANY_INFO['group']}"
        )
        self.multi_cell(0, 5, footer_text, 0, 'C')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- FUNCIÓN: GENERAR INFORME DE SERVICIOS (ANEXO IV) ---
def create_service_report(data):
    pdf = PDFReport("ANEXO IV. INFORME DE SERVICIOS")
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    # [span_8](start_span)Campos principales[span_8](end_span)
    pdf.cell(40, 10, "CLIENTE:", 1)
    pdf.cell(0, 10, data['cliente'], 1, 1)
    
    pdf.cell(40, 10, "SERVICIO:", 1)
    pdf.cell(0, 10, data['servicio'], 1, 1)
    
    pdf.cell(40, 10, "FECHA:", 1)
    pdf.cell(50, 10, str(data['fecha']), 1)
    pdf.cell(30, 10, "HORARIO:", 1)
    pdf.cell(0, 10, data['horario'], 1, 1)
    
    pdf.ln(5)
    
    # Sección Empleados
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "EMPLEADOS", 0, 1)
    pdf.set_font("Arial", size=11)
    
    employees = [data['emp1'], data['emp2'], data['emp3'], data['emp4']]
    for i, emp in enumerate(employees, 1):
        pdf.cell(20, 10, f"{i}º", 1)
        pdf.cell(0, 10, emp if emp else "-", 1, 1)

    pdf.ln(5)

    # Observaciones e Incidencias
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "OBSERVACIONES / INCIDENCIAS", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=data['observaciones'], border=1)
    
    pdf.ln(10)
    
    # Firmas
    y_pos = pdf.get_y()
    pdf.cell(90, 30, "FIRMA EMPLEADO", 1, 0, 'C')
    pdf.cell(90, 30, "RECIBÍ CLIENTE", 1, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- FUNCIÓN: GENERAR PARTE DE INCIDENCIAS (ANEXO V) ---
def create_incident_report(data):
    pdf = PDFReport("ANEXO V. PARTE DE INCIDENCIAS")
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    # [span_9](start_span)Tabla superior[span_9](end_span)
    pdf.cell(30, 10, "FECHA", 1)
    pdf.cell(50, 10, str(data['fecha']), 1)
    pdf.cell(30, 10, "SERVICIO", 1)
    pdf.cell(0, 10, data['servicio'], 1, 1)
    
    pdf.cell(30, 10, "EMPLEADO", 1)
    pdf.cell(0, 10, data['empleado'], 1, 1)
    
    pdf.ln(5)

    # [span_10](start_span)Detalle y Observaciones[span_10](end_span)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "DETALLE DE LA INCIDENCIA", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, txt=data['detalle'], border=1)
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "OBSERVACIONES", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, txt=data['observaciones'], border=1)

    pdf.ln(10)

    # Pie del formulario
    pdf.cell(40, 10, "ELABORADO POR:", 0)
    pdf.cell(0, 10, data['empleado'], 0, 1)
    pdf.cell(40, 10, "REMITIDO A:", 0)
    pdf.cell(0, 10, data['remitido_a'], 0, 1)
    
    pdf.ln(10)
    
    # Firmas Anexo V
    pdf.cell(90, 30, "FIRMA CLIENTE", 1, 0, 'C')
    pdf.cell(90, 30, "FIRMA KUO", 1, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO (APP) ---
def main():
    st.set_page_config(page_title="Gestión Kuo Security", page_icon="🛡️")
    
    # Sidebar de navegación
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2462/2462719.png", width=100)
    st.sidebar.title("Kuo Security App")
    opcion = st.sidebar.radio("Seleccione Tipo de Informe:", ["Informe de Servicios (Anexo IV)", "Parte de Incidencias (Anexo V)"])

    st.title("Generador de Informes Operativos")
    st.markdown("---")

    if opcion == "Informe de Servicios (Anexo IV)":
        st.subheader("📝 Anexo IV: Informe de Servicios")
        
        with st.form("form_servicios"):
            col1, col2 = st.columns(2)
            cliente = col1.text_input("Cliente")
            servicio = col2.text_input("Servicio")
            fecha = col1.date_input("Fecha", date.today())
            horario = col2.text_input("Horario (ej. 08:00 - 20:00)")
            
            st.markdown("**Empleados:**")
            ce1, ce2 = st.columns(2)
            emp1 = ce1.text_input("Empleado 1º")
            emp2 = ce2.text_input("Empleado 2º")
            emp3 = ce1.text_input("Empleado 3º")
            emp4 = ce2.text_input("Empleado 4º")
            
            obs = st.text_area("Observaciones e Incidencias", height=100)
            
            submitted = st.form_submit_button("Generar PDF Informe")
            
            if submitted:
                data = {
                    "cliente": cliente, "servicio": servicio, "fecha": fecha,
                    "horario": horario, "emp1": emp1, "emp2": emp2, 
                    "emp3": emp3, "emp4": emp4, "observaciones": obs
                }
                pdf_bytes = create_service_report(data)
                
                st.success("✅ Informe generado correctamente.")
                
                # Nombre del archivo con fecha
                file_name = f"Informe_Servicio_{fecha}.pdf"
                
                # Botón de descarga
                st.download_button(
                    label="📥 Descargar PDF para enviar",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime='application/pdf'
                )
                
                # Enlace para enviar por correo (mailto)
                subject = f"Informe de Servicio - {fecha}"
                body = "Adjunto encontrará el informe de servicio generado."
                mailto_link = f"mailto:?subject={subject}&body={body}"
                st.markdown(f"[📧 Abrir Cliente de Correo para Enviar]({mailto_link})")

    elif opcion == "Parte de Incidencias (Anexo V)":
        st.subheader("⚠️ Anexo V: Parte de Incidencias")
        
        with st.form("form_incidencias"):
            col1, col2 = st.columns(2)
            fecha = col1.date_input("Fecha", date.today())
            servicio = col2.text_input("Servicio")
            empleado = st.text_input("Nombre del Empleado que reporta")
            
            [span_11](start_span)detalle = st.text_area("Detalle de la Incidencia[span_11](end_span)", height=100)
            observaciones = st.text_area("Observaciones Adicionales", height=80)
            
            remitido = st.text_input("Remitido a (Nombre responsable/cliente)")
            
            submitted = st.form_submit_button("Generar PDF Incidencia")
            
            if submitted:
                data = {
                    "fecha": fecha, "servicio": servicio, "empleado": empleado,
                    "detalle": detalle, "observaciones": observaciones,
                    "remitido_a": remitido
                }
                pdf_bytes = create_incident_report(data)
                
                st.success("✅ Parte de incidencia generado correctamente.")
                
                file_name = f"Incidencia_{fecha}.pdf"
                
                st.download_button(
                    label="📥 Descargar PDF para enviar",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime='application/pdf'
                )
                
                subject = f"Parte de Incidencia Urgente - {fecha}"
                body = "Adjunto encontrará el parte de incidencias."
                mailto_link = f"mailto:?subject={subject}&body={body}"
                st.markdown(f"[📧 Abrir Cliente de Correo para Enviar]({mailto_link})")

if __name__ == "__main__":
    main()
