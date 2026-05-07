"""
Vision Agent - Analyzes electrical installation images using Gemini Vision.
Detects elements and non-conformities in electrical installations.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

from backend.api.gemini_client import get_gemini_client
from backend.vision.context_builder import create_vision_context
from backend.vision.detection_parser import parse_vision_response


class VisionAgent:
    """Agent for visual analysis of electrical installations."""
    
    def __init__(self):
        """Initialize vision agent."""
        self.client = get_gemini_client()
    
    def analyze_image(self, image_paths: List[str], installation_type: str,
                     additional_info: Optional[Dict[str, Any]] = None,
                     language: str = 'es') -> Dict[str, Any]:
        """
        Analyze electrical installation images (multiple).
        """
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        print(f"Analyzing {len(image_paths)} images | type: {installation_type} | lang: {language}")

        # Build context (pass language for bilingual prompt injection)
        context = create_vision_context(installation_type, additional_info, language=language)
        prompt = context['prompt']

        print("Sending to Gemini Vision...")
        response = self.client.analyze_images(image_paths, prompt)

        print("\n" + "="*60)
        print("GEMINI VISION RAW RESPONSE:")
        print("="*60)
        print(response)
        print("="*60 + "\n")

        print("Parsing response...")
        parsed_results = parse_vision_response(response)

        parsed_results['context'] = {
            'installation_type': installation_type,
            'installation_name': context['installation_name'],
            'applicable_norms': context['applicable_norms']
        }

        print(f"\u2713 Analysis complete: {parsed_results['summary']}")
        return parsed_results
    
    def analyze_image_bytes(self, image_bytes: bytes, installation_type: str,
                           additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze an electrical installation image from bytes.
        
        Args:
            image_bytes: Image data as bytes
            installation_type: Type of installation
            additional_info: Optional additional context
            
        Returns:
            Analysis results
        """
        print(f"Analyzing image from bytes")
        print(f"Installation type: {installation_type}")
        
        # Build context
        context = create_vision_context(installation_type, additional_info)
        prompt = context['prompt']
        
        # Analyze image with Gemini Vision
        print("Sending to Gemini Vision...")
        response = self.client.analyze_image_bytes(image_bytes, prompt)
        
        # Parse response
        print("Parsing response...")
        parsed_results = parse_vision_response(response)
        
        # Add context to results
        parsed_results['context'] = {
            'installation_type': installation_type,
            'installation_name': context['installation_name'],
            'applicable_norms': context['applicable_norms']
        }
        
        print(f"✓ Analysis complete: {parsed_results['summary']}")
        
        return parsed_results
    
    def get_visual_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a visual summary of analysis results.
        
        Args:
            analysis_results: Results from analyze_image
            
        Returns:
            Formatted summary string
        """
        summary = f"=== Análisis Visual ===\n\n"
        summary += f"Tipo: {analysis_results['context']['installation_name']}\n\n"
        
        # Conformities
        conformities = analysis_results.get('conformities', [])
        if conformities:
            summary += f"✓ Conformidades ({len(conformities)}):\n"
            for conf in conformities:
                summary += f"  • {conf}\n"
            summary += "\n"
        
        # Non-conformities
        non_conformities = analysis_results.get('non_conformities', [])
        if non_conformities:
            summary += f"⚠️ No Conformidades ({len(non_conformities)}):\n"
            for nc in non_conformities:
                article = f" (Art. {nc['article']})" if nc.get('article') else ""
                summary += f"  • {nc['description']}{article}\n"
            summary += "\n"
        
        # Observations
        observations = analysis_results.get('observations', '')
        if observations:
            summary += f"📝 Observaciones:\n{observations}\n"
        
        return summary


def analyze_installation_image(image_path: str, installation_type: str,
                               additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to analyze an installation image.
    
    Args:
        image_path: Path to image
        installation_type: Type of installation
        additional_info: Optional additional context
        
    Returns:
        Analysis results
    """
    agent = VisionAgent()
    return agent.analyze_image(image_path, installation_type, additional_info)
