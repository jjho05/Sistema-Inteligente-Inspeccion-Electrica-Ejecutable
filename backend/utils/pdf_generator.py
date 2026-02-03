"""
PDF Generator for Electrical Inspection Dictamen
Generates PDF documents matching the simplified technical format.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Set, List


class PDFGenerator:
    """Generate PDF dictamen documents."""
    
    def __init__(self, output_dir: str = "data/generated"):
        """Initialize PDF generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_dictamen(self, data: Dict[str, Any], image_paths: List[str] = None, image_path: str = None) -> str:
        """
        Generate PDF dictamen from analysis data.
        
        Args:
            data: Dictionary containing analysis results
            image_paths: Optional list of paths to analyzed images
            image_path: Legacy support for single image path
            
        Returns:
            Path to generated PDF file
        """
        # Handle legacy image_path
        if image_path and not image_paths:
            image_paths = [image_path]
        elif not image_paths:
            image_paths = []
            
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Dictamen_AUTO-{int(datetime.now().timestamp() * 1000)}_{timestamp}.pdf"
        filepath = self.output_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2C5282'),
            spaceAfter=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        heading1_style = ParagraphStyle(
            'Heading1',
            parent=styles['Heading1'],
            fontSize=13,
            textColor=colors.HexColor('#2C5282'),
            spaceAfter=12,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        heading2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            leading=14
        )
        
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph("Dictamen Técnico de Instalación Eléctrica (Basado en NOM-001-SEDE-2012)", title_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Metadata
        now = datetime.now()
        meses_es = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        fecha = f"{now.day} de {meses_es[now.month]} de {now.year}"
        story.append(Paragraph(f"<b>Fecha del Dictamen:</b> {fecha}", metadata_style))
        story.append(Paragraph(f"<b>Referencia:</b> Análisis de Imagen(es) de Instalación Eléctrica", metadata_style))
        
        normativa_text = """<b>Normativa Aplicable:</b> Norma Oficial Mexicana NOM-001-SEDE-2012, Instalaciones Eléctricas (Utilización). (Se reconoce que la NOM-001-SEDE-2012 se basa en el National Electrical Code, NFPA 70, y las referencias numéricas proporcionadas en las imágenes corresponden a artículos de dicho código, los cuales están integrados en la estructura de la NOM)."""
        story.append(Paragraph(normativa_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # 1. Introducción
        story.append(Paragraph("1. Introducción", heading1_style))
        intro_text = """El presente dictamen técnico tiene como objetivo analizar la(s) imagen(es) proporcionada(s) de una instalación eléctrica, con especial atención a la distribución de conductores dentro de un tablero de distribución o centro de carga. Se evaluará el cumplimiento de los principios fundamentales de seguridad, diseño, selección y construcción establecidos en la NOM-001-SEDE-2012, identificando aspectos conformes, no conformes y aquellos que requieren verificación adicional, así como proporcionando recomendaciones para subsanar deficiencias."""
        story.append(Paragraph(intro_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # 2. Análisis Detallado
        story.append(Paragraph("2. Análisis Detallado de la Instalación", heading1_style))
        intro_analisis = "A continuación, se presenta un análisis de los elementos visibles en la(s) imagen(es), en relación con las referencias normativas señaladas y la NOM-001-SEDE-2012:"
        story.append(Paragraph(intro_analisis, body_style))
        
        # Insert images (Grid Layout)
        if image_paths:
            story.append(Spacer(1, 0.15*inch))
            
            # Prepare images for grid
            grid_data = []
            row = []
            
            for i, img_path in enumerate(image_paths):
                if Path(img_path).exists():
                    try:
                        # Resize maintaining aspect ratio approx
                        img = Image(img_path, width=2.5*inch, height=None, kind='proportional')
                        
                        # Add caption if needed?
                        # For now just image
                        row.append(img)
                        
                        # Max 2 images per row
                        if len(row) == 2:
                            grid_data.append(row)
                            row = []
                    except Exception as e:
                        print(f"Error inserting image {img_path}: {e}")
            
            if row:
                grid_data.append(row)
                
            if grid_data:
                t = Table(grid_data, colWidths=[3*inch, 3*inch])
                t.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.15*inch))
                
        story.append(Spacer(1, 0.15*inch))
        
        # Get NCs
        non_conformities = data.get('non_conformities', [])
        conformities = data.get('conformities', [])
        
        # 2.1 Aspectos que cumplen
        story.append(Paragraph("2.1. Aspectos que cumplen con la normativa (✓)", heading2_style))
        
        if conformities:
            for conf in conformities[:5]:  # Max 5
                bullet = f"• <b>✓ {conf}</b>"
                story.append(Paragraph(bullet, body_style))
                story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph("• No se identificaron aspectos conformes específicos en el análisis visual.", body_style))
        
        story.append(Spacer(1, 0.15*inch))
        
        # 2.2 Aspectos que NO cumplen
        story.append(Paragraph("2.2. Aspectos que NO cumplen o presentan riesgos (✗)", heading2_style))
        
        if non_conformities:
            for nc in non_conformities:
                desc = nc.get('description', 'Sin descripción')
                article = nc.get('article', 'Sin referencia')
                severity = nc.get('severity', 'medium')
                
                # Title with X
                nc_title = f"• <b>✗ {desc}</b>"
                story.append(Paragraph(nc_title, body_style))
                
                # Observación
                obs_text = f"<b>Observación:</b> {desc}"
                story.append(Paragraph(obs_text, body_style))
                
                # Riesgo
                risk_map = {
                    'high': 'Severo. Riesgo inminente de daño al aislamiento de los conductores por abrasión o corte, lo que podría provocar cortocircuitos, fallas a tierra, arcos eléctricos e incluso incendios.',
                    'medium': 'Alto. Puede generar sobrecalentamiento, fallas en la protección y riesgo de incendio.',
                    'low': 'Moderado. Puede afectar la seguridad y eficiencia de la instalación a largo plazo.'
                }
                risk_text = f"<b>Riesgo:</b> {risk_map.get(severity, risk_map['medium'])}"
                story.append(Paragraph(risk_text, body_style))
                
                # Normativa Aplicable (in red)
                if article and article != 'Sin referencia':
                    norm_text = f'<b>Normativa Aplicable:</b> <font color="red">NOM-001-SEDE-2012, Artículo {article}</font>'
                    story.append(Paragraph(norm_text, body_style))
                
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("• No se identificaron no conformidades en el análisis visual.", body_style))
        
        story.append(Spacer(1, 0.2*inch))
        
        # 3. Recomendaciones
        story.append(Paragraph("3. Recomendaciones Específicas de Corrección", heading1_style))
        
        recommendations = [
            ("Protección en Aberturas Metálicas", "Instalar de inmediato pasacables, bujes o anillos aprobados en todas las aberturas metálicas por donde ingresan los conductores al tablero, asegurando que cubran completamente los bordes metálicos."),
            ("Manejo de Conductores y Disipación de Calor", "Deshacer el agrupamiento excesivo de conductores o, en su defecto, aplicar los factores de ajuste de ampacidad correspondientes según la Tabla 310.15(B)(3)(a) de la NOM-001-SEDE-2012 para asegurar que los conductores no se sobrecalienten."),
            ("Organización del Cableado", "Reorganizar el cableado dentro del tablero para un tendido más limpio y ordenado, utilizando cinchos o sujetacables de forma no restrictiva para mantener los conductores en su lugar sin apretarlos excesivamente.")
        ]
        
        for i, (title, desc) in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. <b>{title}:</b>", body_style))
            story.append(Paragraph(f"   {desc}", body_style))
            story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # 4. Conclusión
        story.append(Paragraph("4. Conclusión", heading1_style))
        
        classification = data.get('classification', {})
        justification = classification.get('justification', '')
        
        if justification:
            story.append(Paragraph(justification, body_style))
        else:
            conclusion_text = "La instalación eléctrica analizada presenta deficiencias significativas en cuanto a la protección mecánica de los conductores y organización del cableado. Estas no conformidades representan riesgos serios para la seguridad de las personas y la propiedad, y deben ser corregidas de manera prioritaria para asegurar el cumplimiento con la NOM-001-SEDE-2012. Se recomienda encarecidamente la intervención de personal calificado para realizar las modificaciones necesarias y garantizar la seguridad y fiabilidad de la instalación."
            story.append(Paragraph(conclusion_text, body_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Elaborado por
        inspector_name = data.get('inspector_name', '[ Tu Nombre ]')
        story.append(Paragraph(f"<b>Elaborado por:</b> {inspector_name}", metadata_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Referencias de NOMs
        story.append(Paragraph("Referencias de NOMs:", body_style))
        
        # Extract unique articles
        articles_set: Set[str] = set()
        for nc in non_conformities:
            article = nc.get('article')
            if article and article != 'Sin referencia':
                articles_set.add(article)
        
        # Generate references
        if articles_set:
            for article in sorted(articles_set):
                ref_text = f"• NOM-001-SEDE-2012.pdf (Artículo {article})"
                story.append(Paragraph(ref_text, ParagraphStyle('Ref', parent=body_style, fontName='Courier', fontSize=9)))
        else:
            story.append(Paragraph("• NOM-001-SEDE-2012.pdf (Referencia general)", ParagraphStyle('Ref', parent=body_style, fontName='Courier', fontSize=9)))
        
        # Build PDF
        doc.build(story)
        
        print(f"✓ PDF generated: {filepath}")
        return str(filepath)
