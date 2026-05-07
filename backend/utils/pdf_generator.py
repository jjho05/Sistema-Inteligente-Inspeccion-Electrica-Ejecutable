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
        
    def generate_dictamen(self, data: Dict[str, Any], image_paths: List[str] = None, image_path: str = None, language: str = 'es') -> str:
        """Generate PDF dictamen. language='en' produces an English report."""
        en = (language == 'en')
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
        doc_title = "Technical Report – Electrical Installation (NOM-001-SEDE-2012 / NEC)" if en else "Dictamen Técnico de Instalación Eléctrica (Basado en NOM-001-SEDE-2012)"
        story.append(Paragraph(doc_title, title_style))
        story.append(Spacer(1, 0.15*inch))

        # Metadata
        now = datetime.now()
        if en:
            fecha = now.strftime('%B %d, %Y')
            story.append(Paragraph(f"<b>Report Date:</b> {fecha}", metadata_style))
            story.append(Paragraph("<b>Reference:</b> AI Analysis of Electrical Installation Image(s)", metadata_style))
            norm_text = "<b>Applicable Standard:</b> NOM-001-SEDE-2012 / National Electrical Code (NFPA 70). Numerical article references correspond to NEC articles integrated into the NOM structure."
        else:
            meses_es = {1:'enero',2:'febrero',3:'marzo',4:'abril',5:'mayo',6:'junio',7:'julio',8:'agosto',9:'septiembre',10:'octubre',11:'noviembre',12:'diciembre'}
            fecha = f"{now.day} de {meses_es[now.month]} de {now.year}"
            story.append(Paragraph(f"<b>Fecha del Dictamen:</b> {fecha}", metadata_style))
            story.append(Paragraph("<b>Referencia:</b> Análisis de Imagen(es) de Instalación Eléctrica", metadata_style))
            norm_text = "<b>Normativa Aplicable:</b> Norma Oficial Mexicana NOM-001-SEDE-2012, Instalaciones Eléctricas (Utilización). (Se reconoce que la NOM-001-SEDE-2012 se basa en el National Electrical Code, NFPA 70)."
        story.append(Paragraph(norm_text, body_style))
        story.append(Spacer(1, 0.2*inch))

        # 1. Introduction
        story.append(Paragraph("1. Introduction" if en else "1. Introducción", heading1_style))
        intro = ("This technical report analyzes the provided electrical installation image(s), focusing on conductor distribution and safety compliance with NOM-001-SEDE-2012 / NEC standards."
                 if en else
                 "El presente dictamen técnico analiza la(s) imagen(es) proporcionada(s) de una instalación eléctrica, evaluando el cumplimiento con la NOM-001-SEDE-2012.")
        story.append(Paragraph(intro, body_style))
        story.append(Spacer(1, 0.2*inch))

        # 2. Detailed Analysis
        story.append(Paragraph("2. Detailed Analysis" if en else "2. Análisis Detallado de la Instalación", heading1_style))
        story.append(Paragraph("The following elements were identified in the image(s):" if en else "A continuación se presenta el análisis de los elementos visibles en la(s) imagen(es):", body_style))
        
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
                
        # Get NCs
        non_conformities = data.get('non_conformities', [])
        conformities = data.get('conformities', [])

        # 2.1 Conforming aspects
        h21 = "2.1. Conforming Aspects (✓)" if en else "2.1. Aspectos que cumplen con la normativa (✓)"
        story.append(Paragraph(h21, heading2_style))
        if conformities:
            for conf in conformities[:5]:
                story.append(Paragraph(f"• <b>✓ {conf}</b>", body_style))
                story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph("• No specific conforming aspects were identified." if en else "• No se identificaron aspectos conformes específicos en el análisis visual.", body_style))
        story.append(Spacer(1, 0.15*inch))

        # 2.2 Non-conforming aspects
        h22 = "2.2. Non-Conforming Aspects / Risks (✗)" if en else "2.2. Aspectos que NO cumplen o presentan riesgos (✗)"
        story.append(Paragraph(h22, heading2_style))
        if non_conformities:
            risk_map_en = {'high': 'Severe. Imminent risk of conductor insulation damage, potentially causing short circuits, ground faults, arcing or fire.', 'medium': 'High. May cause overheating, protection failures and fire risk.', 'low': 'Moderate. May affect safety and efficiency over time.'}
            risk_map_es = {'high': 'Severo. Riesgo inminente de daño al aislamiento de los conductores por abrasión o corte, lo que podría provocar cortocircuitos, fallas a tierra, arcos eléctricos e incluso incendios.', 'medium': 'Alto. Puede generar sobrecalentamiento, fallas en la protección y riesgo de incendio.', 'low': 'Moderado. Puede afectar la seguridad y eficiencia de la instalación a largo plazo.'}
            risk_map = risk_map_en if en else risk_map_es
            for nc in non_conformities:
                desc = nc.get('description', 'No description' if en else 'Sin descripción')
                article = nc.get('article', 'No reference' if en else 'Sin referencia')
                severity = nc.get('severity', 'medium')
                story.append(Paragraph(f"• <b>✗ {desc}</b>", body_style))
                obs_label = "Observation:" if en else "Observación:"
                story.append(Paragraph(f"<b>{obs_label}</b> {desc}", body_style))
                risk_label = "Risk:" if en else "Riesgo:"
                story.append(Paragraph(f"<b>{risk_label}</b> {risk_map.get(severity, risk_map['medium'])}", body_style))
                if article and article not in ('Sin referencia', 'No reference'):
                    norm_label = "Applicable Standard:" if en else "Normativa Aplicable:"
                    norm_ref = f"NOM-001-SEDE-2012 / NEC, Article {article}" if en else f"NOM-001-SEDE-2012, Artículo {article}"
                    story.append(Paragraph(f'<b>{norm_label}</b> <font color="red">{norm_ref}</font>', body_style))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("• No non-conformities were detected." if en else "• No se identificaron no conformidades en el análisis visual.", body_style))
        story.append(Spacer(1, 0.2*inch))

        # 3. Recommendations
        story.append(Paragraph("3. Specific Correction Recommendations" if en else "3. Recomendaciones Específicas de Corrección", heading1_style))
        if en:
            recommendations = [
                ("Conductor Protection at Metal Openings", "Immediately install approved cable grommets or bushings at all metal openings where conductors enter the panel, ensuring full coverage of metal edges."),
                ("Conductor Bundling & Heat Dissipation", "Reduce excessive conductor bundling or apply the corresponding ampacity adjustment factors per Table 310.15(B)(3)(a) to prevent overheating."),
                ("Cable Organization", "Reorganize wiring inside the panel for a cleaner layout, using non-restrictive cable ties to secure conductors without excessive compression."),
            ]
        else:
            recommendations = [
                ("Protección en Aberturas Metálicas", "Instalar de inmediato pasacables, bujes o anillos aprobados en todas las aberturas metálicas por donde ingresan los conductores al tablero."),
                ("Manejo de Conductores y Disipación de Calor", "Deshacer el agrupamiento excesivo de conductores o aplicar los factores de ajuste de ampacidad correspondientes según la Tabla 310.15(B)(3)(a)."),
                ("Organización del Cableado", "Reorganizar el cableado dentro del tablero para un tendido más limpio, utilizando cinchos o sujetacables de forma no restrictiva."),
            ]
        for i, (title, desc) in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. <b>{title}:</b>", body_style))
            story.append(Paragraph(f"   {desc}", body_style))
            story.append(Spacer(1, 0.08*inch))
        story.append(Spacer(1, 0.2*inch))

        # 4. Conclusion
        story.append(Paragraph("4. Conclusion" if en else "4. Conclusión", heading1_style))
        
        classification = data.get('classification', {})
        justification = classification.get('justification', '')
        
        if justification:
            story.append(Paragraph(justification, body_style))
        else:
            conclusion_text = "La instalación eléctrica analizada presenta deficiencias significativas en cuanto a la protección mecánica de los conductores y organización del cableado. Estas no conformidades representan riesgos serios para la seguridad de las personas y la propiedad, y deben ser corregidas de manera prioritaria para asegurar el cumplimiento con la NOM-001-SEDE-2012. Se recomienda encarecidamente la intervención de personal calificado para realizar las modificaciones necesarias y garantizar la seguridad y fiabilidad de la instalación."
            story.append(Paragraph(conclusion_text, body_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        inspector_name = data.get('inspector_name', '[ Inspector ]')
        elaborado = "Prepared by:" if en else "Elaborado por:"
        story.append(Paragraph(f"<b>{elaborado}</b> {inspector_name}", metadata_style))
        story.append(Spacer(1, 0.15*inch))

        ref_label = "Standards References:" if en else "Referencias de NOMs:"
        story.append(Paragraph(ref_label, body_style))
        articles_set: Set[str] = set()
        for nc in non_conformities:
            article = nc.get('article')
            if article and article not in ('Sin referencia', 'No reference'):
                articles_set.add(article)
        if articles_set:
            for article in sorted(articles_set):
                ref_text = f"• NOM-001-SEDE-2012 / NEC (Article {article})" if en else f"• NOM-001-SEDE-2012.pdf (Artículo {article})"
                story.append(Paragraph(ref_text, ParagraphStyle('Ref', parent=body_style, fontName='Courier', fontSize=9)))
        else:
            ref_text = "• NOM-001-SEDE-2012 / NEC (General Reference)" if en else "• NOM-001-SEDE-2012.pdf (Referencia general)"
            story.append(Paragraph(ref_text, ParagraphStyle('Ref', parent=body_style, fontName='Courier', fontSize=9)))
        
        # Build PDF
        doc.build(story)
        
        print(f"✓ PDF generated: {filepath}")
        return str(filepath)
