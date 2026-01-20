"""
Detection parser for extracting structured information from Gemini Vision responses.
Parses analysis results into structured data for visualization.
"""

import re
from typing import Dict, Any, List


class DetectionParser:
    """Parses Gemini Vision responses into structured data."""
    
    def __init__(self):
        """Initialize detection parser."""
        pass
    
    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Gemini Vision response into structured format.
        
        Args:
            response_text: Raw response from Gemini Vision
            
        Returns:
            Structured detection data
        """
        sections = self._extract_sections(response_text)
        
        return {
            'raw_response': response_text,
            'elements_identified': sections.get('elementos_identificados', []),
            'conformities': sections.get('conformidades', []),
            'non_conformities': sections.get('no_conformidades', []),
            'observations': sections.get('observaciones', ''),
            'risks': sections.get('riesgos', []),
            'recommendations': sections.get('recomendaciones', [])
        }
    
    def _extract_sections(self, text: str) -> Dict[str, Any]:
        """Extract different sections from the response."""
        sections = {}
        
        # Check for critical keywords that indicate non-conformities
        critical_keywords = [
            'riesgo', 'peligro', 'negligencia', 'deficiente', 'incumpl',
            'violación', 'no conforme', 'incorrecta', 'inadecuada',
            'ausencia', 'falta', 'sin', 'expuesto', 'daño', 'corrosión'
        ]
        
        # If response contains critical keywords, treat as non-conformity
        text_lower = text.lower()
        has_critical_issues = any(keyword in text_lower for keyword in critical_keywords)
        
        # Extract elements identified
        elements_match = re.search(r'##\s*(?:Tipo de Instalación|Elementos?\s+(?:Visibles?|Identificados?))(.*?)(?=##|$)', 
                                  text, re.DOTALL | re.IGNORECASE)
        if elements_match:
            sections['elementos_identificados'] = self._extract_list_items(elements_match.group(1))
        
        # Extract conformities
        conf_match = re.search(r'##\s*(?:✓\s*)?Conformidades?(.*?)(?=##|$)', 
                              text, re.DOTALL | re.IGNORECASE)
        if conf_match:
            conformities = self._extract_list_items(conf_match.group(1))
            # Filter out "Ninguna" or similar
            conformities = [c for c in conformities if 'ninguna' not in c.lower() and len(c) > 10]
            sections['conformidades'] = conformities
        
        # Extract non-conformities - try multiple patterns
        nonconf_patterns = [
            r'###\s*(?:⚠️\s*)?NO\s+CONFORMIDADES?\s+DETECTADAS?(.*?)(?=###|##|$)',
            r'##\s*(?:⚠️\s*)?NO\s+CONFORMIDADES?\s+DETECTADAS?(.*?)(?=##|$)',
            r'##\s*No\s+Conformidades?(.*?)(?=##|$)',
        ]
        
        non_conformities = []
        for pattern in nonconf_patterns:
            nonconf_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if nonconf_match:
                extracted = self._extract_non_conformities(nonconf_match.group(1))
                non_conformities.extend(extracted)
                break  # Only use first matching pattern
        
        # If still no non-conformities but text indicates critical issues, create summary NC
        if not non_conformities and has_critical_issues:
            # Look for numbered items in the response
            numbered_items = re.findall(r'^\s*\d+\.\s*\*?\*?(.+?)(?:\n|$)', text, re.MULTILINE)
            if numbered_items:
                for item in numbered_items[:10]:  # Limit to first 10 items
                    item_lower = item.lower()
                    if any(keyword in item_lower for keyword in critical_keywords):
                        # Extract article if present
                        article_match = re.search(r'(?:art(?:ículo)?\\.?\s*)(\d+(?:\.\d+)?(?:-\d+)?)', item, re.IGNORECASE)
                        article = article_match.group(1) if article_match else None
                        
                        non_conformities.append({
                            'description': item.strip()[:200],  # Limit description length
                            'article': article,
                            'severity': 'high'
                        })
        
        sections['no_conformidades'] = non_conformities[:10]  # Limit to 10 max
        
        # Extract observations
        obs_match = re.search(r'##\s*Observaciones?(.*?)(?=##|$)', 
                             text, re.DOTALL | re.IGNORECASE)
        if obs_match:
            sections['observaciones'] = obs_match.group(1).strip()
        
        # Extract additional observations (Observaciones Adicionales)
        add_obs_match = re.search(r'##\s*Observaciones?\s+Adicionales?(.*?)(?=##|$)', 
                                 text, re.DOTALL | re.IGNORECASE)
        if add_obs_match:
            sections['observaciones_adicionales'] = add_obs_match.group(1).strip()
        
        # Extract risks
        risk_match = re.search(r'##\s*Riesgos?(.*?)(?=##|$)', 
                              text, re.DOTALL | re.IGNORECASE)
        if risk_match:
            sections['riesgos'] = self._extract_list_items(risk_match.group(1))
        
        # Extract recommendations
        rec_match = re.search(r'##\s*Recomendaciones?(.*?)(?=##|$)', 
                             text, re.DOTALL | re.IGNORECASE)
        if rec_match:
            sections['recomendaciones'] = self._extract_list_items(rec_match.group(1))
        
        # Extract actions from DICTAMEN or ACCIONES REQUERIDAS
        actions = []
        dictamen_match = re.search(r'\*{0,2}DICTAMEN:\*{0,2}(.*?)(?=\*{0,2}EL\s+DESCUIDO|$)', 
                                  text, re.DOTALL | re.IGNORECASE)
        if dictamen_match:
            dictamen_text = dictamen_match.group(1).strip()
            sections['dictamen'] = dictamen_text
        
        # Extract ACCIONES REQUERIDAS
        acciones_match = re.search(r'\*{0,2}ACCIONES?\s+REQUERIDAS?:\*{0,2}(.*?)(?=\*{0,2}Dictaminado|$)', 
                                  text, re.DOTALL | re.IGNORECASE)
        if acciones_match:
            actions = self._extract_list_items(acciones_match.group(1))
            sections['acciones_sugeridas'] = actions

        
        return sections
    
    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from text."""
        items = []
        
        # Match numbered or bulleted lists
        patterns = [
            r'^\d+\.\s+(.+)$',  # Numbered: 1. Item
            r'^[-*]\s+(.+)$',   # Bulleted: - Item or * Item
        ]
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    items.append(match.group(1).strip())
                    break
        
        return items
    
    def _extract_non_conformities(self, text: str) -> List[Dict[str, str]]:
        """Extract non-conformities with full structure from Gemini's format."""
        non_conformities = []
        
        # Pattern for numbered NC with bold formatting: "**1. TITLE**" or "1. **TITLE**"
        numbered_patterns = [
            r'^\s*\*{0,2}(\d+)\.\s*(.+?)\*{0,2}\s*$',  # **1. Title** or 1. **Title**
            r'^\s*(\d+)\.\s*\*{0,2}(.+?)\*{0,2}\s*$',  # 1. **Title**
        ]
        
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty or headers
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # Try to match numbered NC item
            match = None
            for pattern in numbered_patterns:
                match = re.match(pattern, line)
                if match:
                    break
            
            if match:
                nc_title = match.group(2).strip()
                nc_title = re.sub(r'\*+', '', nc_title)  # Remove markdown
                
                # Skip very short titles (likely not a real NC)
                if len(nc_title) < 10:
                    i += 1
                    continue
                
                # Initialize NC data with title as fallback description
                description = nc_title
                article = None
                severity = 'high'  # Default
                
                # Look ahead for sub-items (Description, Artículo, Nivel de Riesgo)
                j = i + 1
                found_description = False
                
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    # Stop at next numbered item or section
                    if re.match(r'^\s*\*{0,2}\d+\.', next_line) or next_line.startswith('##'):
                        break
                    
                    # Extract Description (prioritize this over title)
                    desc_match = re.search(r'\*{0,2}Descripción:\*{0,2}\s*(.+)', next_line, re.IGNORECASE)
                    if desc_match:
                        description = desc_match.group(1).strip()
                        description = re.sub(r'\*+', '', description)
                        found_description = True
                    
                    # Extract Article - ROBUST multi-pattern search
                    # Search in next 10 lines for ANY article reference
                    article = None
                    search_end = min(j, len(lines))
                    
                    for search_idx in range(i + 1, search_end):
                        search_line = lines[search_idx].strip()
                        
                        # Stop at next numbered NC
                        if re.match(r'^\s*\*{0,2}\d+\.', search_line):
                            break
                        
                        # Try multiple article patterns
                        article_patterns = [
                            r'\*\s*\*{0,2}(\d+(?:[.-]\d+)*)\*{0,2}:',  # * **314-23**: or * 314-23:
                            r'Art(?:ículo)?\.\s*(\d+(?:[.-]\d+)*)',     # Art. 314-23 or Artículo 314-23
                            r'Artículo\s+(\d+(?:[.-]\d+)*)',            # Artículo 314-23
                            r'^(\d+(?:[.-]\d+)*):',                     # 314-23: at line start
                        ]
                        
                        for pattern in article_patterns:
                            art_match = re.search(pattern, search_line, re.IGNORECASE)
                            if art_match:
                                article = art_match.group(1)
                                print(f"  DEBUG: Extracted article '{article}' from line: {search_line[:80]}")
                                break
                        
                        if article:
                            break
                    
                    if not article and 'art' in ' '.join(lines[i:search_end]).lower():
                        print(f"  DEBUG: Failed to extract article from NC: {nc_title[:60]}")

                    
                    # Extract Risk Level
                    risk_match = re.search(r'\*{0,2}Nivel\s+de\s+Riesgo:\*{0,2}\s*\*{0,2}(ALTO|MEDIO|BAJO)', next_line, re.IGNORECASE)
                    if risk_match:
                        risk_level = risk_match.group(1).upper()
                        if risk_level == 'ALTO':
                            severity = 'high'
                        elif risk_level == 'MEDIO':
                            severity = 'medium'
                        else:
                            severity = 'low'
                    
                    j += 1
                
                # If no article found in sub-items, try title
                if not article:
                    art_match = re.search(r'(?:Art(?:ículo)?\\.?\s*)(\d+(?:[.-]\d+)*)', nc_title, re.IGNORECASE)
                    if art_match:
                        article = art_match.group(1)
                
                # Only add if we have meaningful content
                if len(description) >= 10:
                    non_conformities.append({
                        'description': description,
                        'article': article,
                        'severity': severity
                    })
                
                i = j  # Skip processed lines
            else:
                i += 1
        
        return non_conformities
    
    def classify_severity(self, non_conformities: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Classify severity of non-conformities.
        
        Args:
            non_conformities: List of non-conformities
            
        Returns:
            Non-conformities with severity classification
        """
        high_severity_keywords = [
            'peligro', 'riesgo', 'expuesto', 'sin protección', 
            'falta de tierra', 'conexión suelta', 'corto circuito'
        ]
        
        for nc in non_conformities:
            desc_lower = nc['description'].lower()
            
            # Check for high severity keywords
            if any(keyword in desc_lower for keyword in high_severity_keywords):
                nc['severity'] = 'high'
            elif nc.get('article'):
                nc['severity'] = 'medium'
            else:
                nc['severity'] = 'low'
        
        return non_conformities
    
    def generate_summary(self, parsed_data: Dict[str, Any]) -> str:
        """
        Generate a summary of the analysis.
        
        Args:
            parsed_data: Parsed detection data
            
        Returns:
            Summary string
        """
        num_conformities = len(parsed_data.get('conformities', []))
        num_non_conformities = len(parsed_data.get('non_conformities', []))
        
        summary = f"Análisis completado:\n"
        summary += f"- {num_conformities} conformidades detectadas\n"
        summary += f"- {num_non_conformities} no conformidades detectadas\n"
        
        if num_non_conformities == 0:
            summary += "\n✓ La instalación cumple con la normativa revisada."
        else:
            summary += f"\n⚠️ Se requieren {num_non_conformities} correcciones."
        
        return summary


def parse_vision_response(response_text: str) -> Dict[str, Any]:
    """
    Convenience function to parse vision response.
    
    Args:
        response_text: Raw response from Gemini Vision
        
    Returns:
        Parsed detection data
    """
    parser = DetectionParser()
    parsed = parser.parse_response(response_text)
    
    # Classify severity of non-conformities
    if parsed.get('non_conformities'):
        parsed['non_conformities'] = parser.classify_severity(parsed['non_conformities'])
    
    # Add summary
    parsed['summary'] = parser.generate_summary(parsed)
    
    return parsed
