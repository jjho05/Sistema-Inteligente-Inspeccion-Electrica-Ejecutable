"""
Integrator Agent - Synthesizes analysis results and generates final reports.
Coordinates vision and normative agents to produce complete inspection reports.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from backend.agents.vision_agent import VisionAgent
from backend.agents.normative_agent import NormativeAgent


class IntegratorAgent:
    """Agent that integrates results from vision and normative agents."""
    
    def __init__(self):
        """Initialize integrator agent."""
        self.vision_agent = VisionAgent()
        self.normative_agent = NormativeAgent()
    
    def generate_complete_analysis(self, image_paths: List[str], installation_type: str,
                                   additional_info: Optional[Dict[str, Any]] = None,
                                   language: str = 'es') -> Dict[str, Any]:
        """
        Generate complete analysis integrating vision and normative verification.
        
        Args:
            image_paths: List of paths to installation images
            installation_type: Type of installation
            additional_info: Optional additional context
            
        Returns:
            Complete analysis with classification
        """
        print("=== Starting Complete Analysis ===")
        
        # Backward compatibility
        if isinstance(image_paths, str):
            image_paths = [image_paths]
        
        # Step 1: Visual analysis
        print(f"\n[1/3] Visual Analysis (language={language})...")
        vision_results = self.vision_agent.analyze_image(
            image_paths, installation_type, additional_info, language=language
        )
        
        # Step 2: Normative verification (DISABLED for speed - Vision Agent is sufficient)
        print("\n[2/3] Normative Verification...")
        print("  ⚡ Using Vision Agent results directly (faster)")
        non_conformities = vision_results.get('non_conformities', [])
        
        # Ensure all NCs have severity
        verified_nc = []
        for nc in non_conformities:
            if 'severity' not in nc:
                nc['severity'] = 'high'  # Default to high for safety
            verified_nc.append(nc)
        
        # Step 3: Generate final classification
        print("\n[3/3] Generating Classification...")
        classification = self._classify_installation(verified_nc, language=language)
        
        # Build complete report
        report = {
            'timestamp': datetime.now().isoformat(),
            'installation_type': installation_type,
            'installation_name': vision_results['context']['installation_name'],
            'applicable_norms': vision_results['context']['applicable_norms'],
            'vision_analysis': vision_results,
            'verified_non_conformities': verified_nc,
            'classification': classification,
            'summary': self._generate_summary(vision_results, verified_nc, classification, language=language)
        }
        
        print(f"\n✓ Analysis Complete: {classification['status']}")
        
        return report
    
    def _classify_installation(self, verified_non_conformities: List[Dict[str, Any]],
                               language: str = 'es') -> Dict[str, str]:
        """
        Classify installation based on verified non-conformities.
        STRICT POLICY: Any non-conformity = NON-COMPLIANT / NO CONFORME
        """
        en = (language == 'en')

        if verified_non_conformities and len(verified_non_conformities) > 0:
            high_severity   = sum(1 for nc in verified_non_conformities if nc.get('severity') == 'high')
            medium_severity = sum(1 for nc in verified_non_conformities if nc.get('severity') == 'medium')
            total_nc        = len(verified_non_conformities)

            if high_severity > 0:
                return {
                    'status': 'NON-COMPLIANT' if en else 'NO CONFORME',
                    'justification': (
                        f'{high_severity} CRITICAL non-conformity/ies detected, representing a significant safety risk. Immediate correction required.'
                        if en else
                        f'Se detectaron {high_severity} no conformidad(es) CRÍTICA(S) que representan riesgo significativo. Requiere corrección inmediata.'
                    )
                }
            elif medium_severity > 0:
                return {
                    'status': 'NON-COMPLIANT' if en else 'NO CONFORME',
                    'justification': (
                        f'{medium_severity} medium-severity non-conformity/ies detected. Installation does not meet regulatory requirements.'
                        if en else
                        f'Se detectaron {medium_severity} no conformidad(es) de severidad media. La instalación no cumple con los requisitos normativos.'
                    )
                }
            else:
                return {
                    'status': 'NON-COMPLIANT' if en else 'NO CONFORME',
                    'justification': (
                        f'{total_nc} non-conformity/ies detected. Installation requires corrections to meet the standard.'
                        if en else
                        f'Se detectaron {total_nc} no conformidad(es). La instalación requiere correcciones para cumplir con la normativa.'
                    )
                }

        return {
            'status': 'COMPLIANT' if en else 'CONFORME',
            'justification': (
                'Installation meets all verified regulatory requirements. No non-conformities were detected.'
                if en else
                'La instalación cumple con todos los requisitos normativos verificados. No se detectaron no conformidades.'
            )
        }
    
    def _generate_summary(self, vision_results: Dict[str, Any],
                         verified_nc: List[Dict[str, Any]],
                         classification: Dict[str, str],
                         language: str = 'es') -> str:
        """Generate executive summary of the analysis (bilingual)."""
        en = (language == 'en')

        if en:
            summary  = "EXECUTIVE SUMMARY\n\n"
            summary += f"Classification: {classification['status']}\n"
            summary += f"{classification['justification']}\n\n"
            conformities = vision_results.get('conformities', [])
            summary += f"Conformities: {len(conformities)}\n"
            summary += f"Non-Conformities: {len(verified_nc)}\n"
            high   = [nc for nc in verified_nc if nc.get('severity') == 'high']
            medium = [nc for nc in verified_nc if nc.get('severity') == 'medium']
            low    = [nc for nc in verified_nc if nc.get('severity') == 'low']
            if high:
                summary += f"\n🔴 CRITICAL ({len(high)}):\n"
                for nc in high[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "No ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"
            if medium:
                summary += f"\n🟡 MEDIUM ({len(medium)}):\n"
                for nc in medium[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "No ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"
            if low:
                summary += f"\n🟢 LOW ({len(low)}):\n"
                for nc in low[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "No ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"
        else:
            summary  = "RESUMEN EJECUTIVO\n\n"
            summary += f"Clasificación: {classification['status']}\n"
            summary += f"{classification['justification']}\n\n"
            conformities = vision_results.get('conformities', [])
            summary += f"Conformidades: {len(conformities)}\n"
            summary += f"No Conformidades: {len(verified_nc)}\n"
            high   = [nc for nc in verified_nc if nc.get('severity') == 'high']
            medium = [nc for nc in verified_nc if nc.get('severity') == 'medium']
            low    = [nc for nc in verified_nc if nc.get('severity') == 'low']
            if high:
                summary += f"\n🔴 CRÍTICAS ({len(high)}):\n"
                for nc in high[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "Sin ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"
            if medium:
                summary += f"\n🟡 MEDIA ({len(medium)}):\n"
                for nc in medium[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "Sin ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"
            if low:
                summary += f"\n🟢 BAJA ({len(low)}):\n"
                for nc in low[:10]:
                    article = f"Art. {nc.get('article')}" if nc.get('article') else "Sin ref."
                    summary += f"  • {nc['description'][:150]} ({article})\n"

        return summary
    
    def generate_dictamen_data(self, analysis_report: Dict[str, Any],
                              inspection_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate data structure for Word document generation.
        
        Args:
            analysis_report: Complete analysis report
            inspection_data: Optional inspection metadata (folio, solicitante, etc.)
            
        Returns:
            Data dictionary for document template
        """
        inspection_data = inspection_data or {}
        
        # Build observations text (simple format)
        observations = []
        for nc in analysis_report.get('verified_non_conformities', []):
            desc = nc['description']
            article = nc.get('article', 'N/A')
            observations.append(f"• {desc} (Art. {article})")
        
        observations_text = "\n".join(observations) if observations else "Sin observaciones"
        
        # Build detailed non-conformities (Omar Zúñiga format)
        detailed_nc = []
        for i, nc in enumerate(analysis_report.get('verified_non_conformities', []), 1):
            # Create detailed structure for each non-conformity
            nc_detail = {
                'titulo': f"{i}. {nc.get('description', 'Observación')}",
                'descripcion': f"Lo que se observa: {nc.get('description', 'N/A')}",
                'norma': self._format_norm_reference(nc),
                'veredicto': self._format_verdict(nc)
            }
            detailed_nc.append(nc_detail)
        
        # Build dictamen data
        dictamen_data = {
            'folio': inspection_data.get('folio', f'DICT-{datetime.now().strftime("%Y-%m")}-AUTO'),
            'fecha': inspection_data.get('fecha', datetime.now().strftime('%d de %B de %Y')),
            'solicitante': inspection_data.get('solicitante', ''),
            'rfc': inspection_data.get('rfc', 'N/A'),
            'ubicacion': inspection_data.get('ubicacion', {
                'direccion': 'Instalación eléctrica',
                'municipio': 'N/A',
                'estado': 'N/A',
                'cp': 'N/A'
            }),
            'tipo_instalacion': analysis_report['installation_name'],
            'observaciones': observations_text,
            'no_conformidades': len(analysis_report.get('verified_non_conformities', [])),
            'no_conformidades_detalladas': detailed_nc,
            'dictamen_final': analysis_report['classification']['status'],
            'justificacion': analysis_report['classification'].get('justification', ''),
            'non_conformities': analysis_report.get('verified_non_conformities', []),
            'conformities': analysis_report.get('vision_analysis', {}).get('conformities', []),
            'classification': analysis_report['classification'],
            'summary': analysis_report.get('summary', ''),
            'inspector_name': inspection_data.get('inspector_name', '[ Tu Nombre ]'),
            'normas_aplicables': ', '.join(analysis_report['applicable_norms'])
        }
        
        return dictamen_data
    
    def _format_norm_reference(self, nc: Dict[str, Any]) -> str:
        """Format normative reference for detailed non-conformity."""
        article = nc.get('article')
        normative_support = nc.get('normative_support', {})
        
        if normative_support and normative_support.get('explanation'):
            return normative_support['explanation']
        elif article:
            return f"• Artículo {article}: Requisitos aplicables según NOM-001-SEDE-2012"
        else:
            return "• Requisitos generales de la normativa eléctrica"
    
    def _format_verdict(self, nc: Dict[str, Any]) -> str:
        """Format verdict for detailed non-conformity."""
        severity = nc.get('severity', 'medium')
        
        if severity == 'high':
            return "CRÍTICO. Esta condición representa un riesgo significativo y debe ser corregida de inmediato."
        elif severity == 'medium':
            return "INCUMPLIMIENTO. Se requiere corrección para cumplir con la normativa."
        else:
            return "OBSERVACIÓN. Se recomienda atender esta condición."


def analyze_installation(image_paths: List[str], installation_type: str,
                        additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function for complete installation analysis.
    
    Args:
        image_paths: List of paths to images
        installation_type: Type of installation
        additional_info: Optional additional context
        
    Returns:
        Complete analysis report
    """
    agent = IntegratorAgent()
    return agent.generate_complete_analysis(image_paths, installation_type, additional_info)
