"""
Context builder for Gemini Vision analysis.
Constructs enriched prompts with installation-specific context.
"""

from typing import Dict, Any, Optional
from backend.knowledge.installation_types import get_installation_type
from backend.vision.prompt_templates import build_contextualized_prompt


class ContextBuilder:
    """Builds contextual prompts for vision analysis."""
    
    def __init__(self):
        """Initialize context builder."""
        pass
    
    def build_context(self, installation_type: str, 
                     additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build complete context for vision analysis.
        
        Args:
            installation_type: Type ID (e.g., 'tablero_distribucion')
            additional_info: Optional additional information
            
        Returns:
            Context dictionary with prompt and metadata
        """
        # Get installation type info
        type_info = get_installation_type(installation_type)
        if not type_info:
            raise ValueError(f"Unknown installation type: {installation_type}")
        
        # Build additional context string
        additional_context = ""
        if additional_info:
            if 'location' in additional_info:
                additional_context += f"Ubicación: {additional_info['location']}\n"
            if 'voltage' in additional_info:
                additional_context += f"Voltaje: {additional_info['voltage']}\n"
            if 'notes' in additional_info:
                additional_context += f"Notas: {additional_info['notes']}\n"
        
        # Build contextualized prompt
        prompt = build_contextualized_prompt(installation_type, additional_context)
        
        # Return complete context
        return {
            'installation_type': installation_type,
            'installation_name': type_info['nombre'],
            'applicable_norms': type_info['normas'],
            'key_elements': type_info['elementos_clave'],
            'prompt': prompt,
            'additional_info': additional_info or {}
        }
    
    def get_analysis_instructions(self, installation_type: str) -> str:
        """
        Get specific analysis instructions for an installation type.
        
        Args:
            installation_type: Type ID
            
        Returns:
            Analysis instructions
        """
        type_info = get_installation_type(installation_type)
        if not type_info:
            return "Analiza la instalación eléctrica en la imagen."
        
        instructions = f"Analiza esta {type_info['nombre'].lower()}. "
        instructions += f"Enfócate en: {', '.join(type_info['elementos_clave'])}."
        
        return instructions


def create_vision_context(installation_type: str, 
                         additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to create vision context.
    
    Args:
        installation_type: Type ID
        additional_info: Optional additional information
        
    Returns:
        Context dictionary
    """
    builder = ContextBuilder()
    return builder.build_context(installation_type, additional_info)
