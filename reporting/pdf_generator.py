import os
from datetime import datetime
from pathlib import Path
from io import BytesIO

import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

class PDFReportGenerator:
    def __init__(self, title, report_type="general"):
        self.title = title
        self.report_type = report_type
        self.test_results = []
        self.styles = getSampleStyleSheet()

    def add_test_result(self, module, test_name, status, details="", duration=None):
        """Añade el resultado de una prueba, incluyendo módulo y duración."""
        self.test_results.append({
            "module": module,
            "name": test_name,
            "status": status,
            "details": details,
            "duration": duration
        })

    def _get_status_color(self, status):
        """Devuelve un color basado en el estado del resultado."""
        if status == 'PASSED': return 'green'
        if status in ['FAILED', 'FATAL']: return 'red'
        if status == 'SETUP': return 'blue'
        if status == 'SKIPPED': return 'orange'
        return 'black'

    def _generate_pie_chart(self):
        """Genera un gráfico de pastel con el resumen de resultados."""
        passed = sum(1 for r in self.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.test_results if r['status'] in ['FAILED', 'FATAL'])
        
        if passed == 0 and failed == 0: return None

        labels = 'Aprobados', 'Fallidos'
        sizes = [passed, failed]
        chart_colors = ['#4CAF50', '#F44336']
        explode = (0.1, 0) if passed > 0 and failed > 0 else (0, 0)

        fig, ax = plt.subplots(figsize=(5, 5)) 
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
           shadow=False, startangle=90, colors=chart_colors)
        ax.axis('equal')
        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def _generate_duration_chart(self):
        """Genera un gráfico de barras con la duración de cada prueba."""
        valid_tests = [r for r in self.test_results if r.get('duration') is not None and r['status'] not in ['SETUP', 'SKIPPED']]
        if not valid_tests: return None

        test_names = [r['name'] for r in valid_tests]
        durations = [r['duration'] for r in valid_tests]
        bar_colors = ['#4CAF50' if r['status'] == 'PASSED' else '#F44336' for r in valid_tests]

        fig, ax = plt.subplots(figsize=(8, len(test_names) * 0.4 + 2))
        bars = ax.barh(test_names, durations, color=bar_colors)
        ax.set_xlabel('Duración (segundos)')
        ax.set_title('Tiempos de Ejecución por Prueba')
        ax.invert_yaxis()

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, f'{width:.2f}s', va='center')
        
        plt.tight_layout()
        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def generate(self, output_folder="."):
        """Crea el archivo PDF con tablas primero y gráficos al final."""
        output_path = Path(output_folder).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        doc_path = output_path / f"integration_report_{self.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(str(doc_path), pagesize=letter)
        story = []

        # --- Cabecera Formal ---
        # Construir la ruta al logo de forma más robusta
        script_dir = Path(__file__).parent
        unal_logo_path = script_dir.parent / 'assets' / 'logounal.jpg'
        header_info_text = """
            <b><br/>Universidad Nacional de Colombia</b><br/>
            Facultad de Ingeniería<br/>
            Ingeniería de software II 2025-1S<br/>
            Grupo Tiburones<br/>
            Proyecto Donatello
        """
        
        if unal_logo_path.exists():
            im = Image(unal_logo_path, width=1*inch, height=1*inch)
            im.hAlign = 'RIGHT' # Alinea la imagen a la derecha dentro de su celda
            
            header_paragraph = Paragraph(header_info_text, self.styles['Normal'])
            
            # Cambiamos el orden: primero el texto, luego la imagen.
            header_table_data = [[header_paragraph, im]]
            # Ajustamos los anchos de columna para que coincidan con el nuevo orden.
            header_table = Table(header_table_data, colWidths=[6*inch, 1.2*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # El padding izquierdo ya no es necesario para la columna de texto.
            ]))
            story.append(header_table)
        else:
            # Si no se encuentra el logo, solo se agrega el texto
            story.append(Paragraph(header_info_text, self.styles['Normal']))

        story.append(Spacer(1, 0.3*inch))

        # Título del Reporte y Fecha
        story.append(Paragraph(self.title, self.styles['h1']))
        story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))


        # --- Sección de Resultados Detallados por Módulo (AHORA PRIMERO) ---
        story.append(Paragraph("Resultados Detallados por Módulo", self.styles['h2']))
        
        modules = sorted(list(set(r['module'] for r in self.test_results)))
        
        for module in modules:
            # --- LÓGICA DE FILTRADO ---
            # 1. Obtener solo los resultados del módulo actual que NO sean SETUP o SKIPPED.
            module_results = [r for r in self.test_results if r['module'] == module and r['status'] not in ['SETUP', 'SKIPPED']]

            # 2. Si la lista de resultados está vacía, no crear la tabla para este módulo.
            if not module_results:
                continue

            story.append(Paragraph(f"Módulo: {module}", self.styles['h3']))
            
            table_data = [['Paso / Prueba', 'Estado', 'Detalles', 'Duración (s)']]
            for res in module_results:
                status_color = self._get_status_color(res['status'])
                status_cell = Paragraph(f'<font color="{status_color}">{res["status"]}</font>', self.styles['Normal'])
                duration_str = f"{res['duration']:.2f}" if res['duration'] is not None else "N/A"
                table_data.append([
                    Paragraph(res['name'], self.styles['Normal']), 
                    status_cell, 
                    Paragraph(res['details'], self.styles['Normal']),
                    duration_str
                ])

            table = Table(table_data, colWidths=[2.5*inch, 0.8*inch, 2.5*inch, 0.7*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            story.append(Spacer(1, 0.2*inch))

        # --- Sección de Gráficos (AHORA AL FINAL) ---
        story.append(Paragraph("Análisis Visual de Resultados", self.styles['h2']))
        pie_chart_img = self._generate_pie_chart()
        if pie_chart_img:
            story.append(Paragraph("Distribución de Resultados", self.styles['h3']))
            story.append(Image(pie_chart_img, width=4*inch, height=4*inch))
            story.append(Spacer(1, 0.2*inch))
        
        duration_chart_img = self._generate_duration_chart()
        if duration_chart_img:
            story.append(Paragraph("Tiempos de Ejecución por Prueba", self.styles['h3']))
            story.append(Image(duration_chart_img, width=7*inch, height=5*inch))
            story.append(Spacer(1, 0.2*inch))

        doc.build(story)
        print(f"✅ Reporte PDF con gráficos generado en: {doc_path}")