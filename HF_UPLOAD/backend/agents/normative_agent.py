"""
Normative Agent - Verifies compliance with electrical norms using RAG.
Searches normative database and validates findings against regulations.
"""

from typing import Dict, Any, List, Optional

from backend.rag.vector_store import get_vector_store
from backend.api.gemini_client import get_gemini_client


class NormativeAgent:
    """Agent for normative verification using RAG."""
    
    def __init__(self):
        """Initialize normative agent."""
        self.vector_store = get_vector_store()
        self.client = get_gemini_client()
    
    def verify_conformity(self, observation: str, norm_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify if an observation conforms to normative requirements.
        
        Args:
            observation: Observation to verify
            norm_filter: Optional filter by specific norm
            
        Returns:
            Verification result with normative references
        """
        # Search for relevant normative content
        results = self.vector_store.search(observation, n_results=3, norm_filter=norm_filter)
        
        if not results:
            return {
                'observation': observation,
                'conformity': 'unknown',
                'references': [],
                'explanation': 'No se encontraron referencias normativas relevantes.'
            }
        
        # Build context with normative references
        context = "NORMATIVA RELEVANTE:\n\n"
        for i, result in enumerate(results, 1):
            context += f"{i}. {result['metadata']['norm_id']}:\n"
            context += f"{result['content'][:500]}...\n\n"
        
        # Ask Gemini to verify conformity
        prompt = f"""
Eres un experto en normativa eléctrica mexicana. Analiza la siguiente observación y determina si cumple o no cumple con la normativa.

OBSERVACIÓN:
{observation}

{context}

INSTRUCCIONES:
1. Determina si la observación CUMPLE o NO CUMPLE con la normativa
2. Cita los artículos específicos relevantes
3. Explica brevemente por qué cumple o no cumple

FORMATO DE RESPUESTA:
CONFORMIDAD: [CUMPLE/NO CUMPLE/PARCIAL]
ARTÍCULOS: [Lista de artículos citados]
EXPLICACIÓN: [Explicación breve]
"""
        
        response = self.client.generate_text(prompt)
        
        # Parse response
        conformity = self._extract_conformity(response)
        articles = self._extract_articles(response)
        explanation = self._extract_explanation(response)
        
        return {
            'observation': observation,
            'conformity': conformity,
            'articles': articles,
            'references': [
                {
                    'norm_id': r['metadata']['norm_id'],
                    'content': r['content'][:200] + '...'
                }
                for r in results
            ],
            'explanation': explanation,
            'raw_response': response
        }
    
    def verify_non_conformities(self, non_conformities: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Verify multiple non-conformities against normative database.
        
        Args:
            non_conformities: List of non-conformities from vision agent
            
        Returns:
            List of verified non-conformities with normative support
        """
        verified = []
        
        # Limit to first 10 to avoid timeout
        nc_to_verify = non_conformities[:10]
        total = len(nc_to_verify)
        
        print(f"Verifying {total} non-conformities...")
        
        for i, nc in enumerate(nc_to_verify, 1):
            print(f"  Verifying {i}/{total}...")
            description = nc['description']
            article = nc.get('article')
            
            # Search for normative support
            query = f"{description} artículo {article}" if article else description
            verification = self.verify_conformity(query)
            
            verified.append({
                **nc,
                'normative_support': verification
            })
        
        print(f"✓ Verified {len(verified)} non-conformities")
        return verified
    
    def get_article_content(self, article_number: str, norm_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get content of a specific article from norms.
        
        Args:
            article_number: Article number (e.g., '408', '110.14')
            norm_id: Optional specific norm ID
            
        Returns:
            Article content and metadata
        """
        query = f"Artículo {article_number}"
        results = self.vector_store.search(query, n_results=5, norm_filter=norm_id)
        
        if not results:
            return {
                'article': article_number,
                'found': False,
                'content': None
            }
        
        # Find best match
        best_match = results[0]
        
        return {
            'article': article_number,
            'found': True,
            'norm_id': best_match['metadata']['norm_id'],
            'content': best_match['content'],
            'all_matches': results
        }
    
    def _extract_conformity(self, response: str) -> str:
        """Extract conformity status from response."""
        response_upper = response.upper()
        if 'NO CUMPLE' in response_upper:
            return 'no_cumple'
        elif 'PARCIAL' in response_upper:
            return 'parcial'
        elif 'CUMPLE' in response_upper:
            return 'cumple'
        return 'unknown'
    
    def _extract_articles(self, response: str) -> List[str]:
        """Extract article numbers from response."""
        import re
        articles = []
        
        # Find article numbers (e.g., 408, 110.14, 250-122)
        pattern = r'\b\d+(?:\.\d+)?(?:-\d+)?\b'
        matches = re.findall(pattern, response)
        
        # Filter to likely article numbers (not too long)
        articles = [m for m in matches if len(m) <= 10]
        
        return list(set(articles))  # Remove duplicates
    
    def _extract_explanation(self, response: str) -> str:
        """Extract explanation from response."""
        import re
        
        # Try to find explanation section
        match = re.search(r'EXPLICACIÓN:\s*(.+)', response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Otherwise return full response
        return response.strip()


def verify_observation(observation: str, norm_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to verify an observation.
    
    Args:
        observation: Observation to verify
        norm_filter: Optional norm filter
        
    Returns:
        Verification result
    """
    agent = NormativeAgent()
    return agent.verify_conformity(observation, norm_filter)
