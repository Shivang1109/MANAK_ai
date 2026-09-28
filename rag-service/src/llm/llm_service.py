"""
LLM Service
Manages LLM interactions with grounded, citation-aware prompting
Supports: OpenAI, Google Gemini, Ollama (local)
"""

from typing import List, Dict, Optional
from loguru import logger
import os
import openai
from anthropic import Anthropic


class LLMService:
    """Service for LLM generation with grounding"""
    
    def __init__(self, config: Dict):
        self.config = config.get('llm', {})
        self.provider = self.config.get('provider', 'openai')
        self.model = self.config.get('model', 'gpt-3.5-turbo')
        self.temperature = self.config.get('temperature', 0.1)
        self.max_tokens = self.config.get('max_tokens', 1000)
        
        # System prompt
        self.system_prompt = config.get('system_prompt', '')
        
        # Initialize clients based on provider
        if self.provider == 'openai':
            openai.api_key = os.getenv('OPENAI_API_KEY')
            if not openai.api_key:
                logger.warning("OPENAI_API_KEY not set")
        elif self.provider == 'anthropic':
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif self.provider == 'gemini':
            # Google Gemini setup with NEW google.genai package
            try:
                from google import genai
                from google.genai import types
                
                api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
                if api_key:
                    # Use official gemini-2.0-flash for high token capacity and sub-4s latency
                    self.gemini_model_name = self.model or 'gemini-2.0-flash'
                    logger.info(f"Google Gemini initialized with model: {self.gemini_model_name}")
                else:
                    logger.error("GOOGLE_API_KEY not set")
            except ImportError:
                logger.error("google-genai not installed. Run: pip install google-genai")
        elif self.provider == 'ollama':
            # Ollama (local) setup
            try:
                import ollama
                self.ollama_client = ollama
                self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
                logger.info(f"Ollama initialized at {self.ollama_host}")
            except ImportError:
                logger.error("ollama not installed. Run: pip install ollama")
        
        logger.info(f"LLM Service initialized: {self.provider}/{self.model}")
    
    def generate_answer(self, 
                       query: str,
                       retrieved_chunks: List[Dict],
                       conversation_history: Optional[List[Dict]] = None) -> Dict:
        """
        Generate grounded answer from retrieved context
        
        Args:
            query: User question
            retrieved_chunks: Retrieved and re-ranked chunks
            conversation_history: Optional conversation history
            
        Returns:
            Dict with answer, confidence, sources
        """
        logger.info(f"Generating answer for: {query[:50]}...")
        
        # Build context from chunks
        context = self._build_context(retrieved_chunks)
        
        # Build prompt
        prompt = self._build_prompt(query, context, retrieved_chunks)
        
        # Generate answer based on provider — with automatic fallback
        try:
            if self.provider == 'openai':
                response = self._generate_openai(prompt, conversation_history)
            elif self.provider == 'anthropic':
                response = self._generate_anthropic(prompt, conversation_history)
            elif self.provider == 'gemini':
                response = self._generate_gemini(prompt, conversation_history)
            elif self.provider == 'ollama':
                response = self._generate_ollama(prompt, conversation_history)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as primary_error:
            # ── AUTO-FALLBACK ─────────────────────────────────────────────────
            # If the primary provider fails (no API key, quota, network),
            # automatically try the fallback provider.
            logger.warning(f"Primary provider '{self.provider}' failed: {primary_error}. Trying fallback...")
            response = self._generate_with_fallback(prompt, conversation_history, primary_error)
        
        # Extract citations and calculate confidence
        result = self._process_response(response, retrieved_chunks)
        
        logger.success("Answer generated")
        
        return result
    
    def _generate_with_fallback(self, prompt: str, history, primary_error: Exception) -> str:
        """
        Fallback chain: gemini → ollama → openai → error message.
        Called automatically when the primary provider fails.
        """
        fallback_order = ['gemini', 'ollama', 'openai']
        # Remove primary provider so we don't retry it
        providers_to_try = [p for p in fallback_order if p != self.provider]
        
        for fallback in providers_to_try:
            try:
                logger.info(f"Attempting fallback provider: {fallback}")
                if fallback == 'gemini' and hasattr(self, 'gemini_client'):
                    return self._generate_gemini(prompt, history)
                elif fallback == 'ollama':
                    # Try Ollama even if not configured as primary
                    import ollama as _ollama
                    _client = _ollama
                    model = self.config.get('models', {}).get('ollama', 'llama3.2')
                    msgs = [{'role': 'user', 'content': prompt}]
                    resp = _client.chat(model=model, messages=msgs)
                    return resp['message']['content']
                elif fallback == 'openai' and os.getenv('OPENAI_API_KEY'):
                    return self._generate_openai(prompt, history)
            except Exception as fb_err:
                logger.warning(f"Fallback '{fallback}' also failed: {fb_err}")
                continue
        
        # All providers exhausted
        logger.error(f"All LLM providers failed. Original error: {primary_error}")
        return ("I'm unable to generate a response at this time due to a service issue. "
                "Please check that GOOGLE_API_KEY is set correctly in the environment, "
                "or ensure Ollama is running locally (ollama serve).")
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """Build context string from top retrieved chunks (capped to top 4 to stay well under token quotas)"""
        context_parts = []
        
        for i, chunk in enumerate(chunks[:4], 1):
            metadata = chunk['metadata']
            
            context_part = f"""
[Source {i}]
Standard: {metadata.get('standard_number', 'N/A')}
Title: {metadata.get('title', 'N/A')}
Clause: {metadata.get('clause', 'N/A')}
Page: {metadata.get('page', 'N/A')}

Content:
{chunk['content']}
"""
            context_parts.append(context_part)
        
        return "\n---\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str, chunks: List[Dict]) -> str:
        """Build the prompt for LLM"""
        
        # Check if sufficient context
        if not chunks:
            return f"""
User Question: {query}

You have NO relevant BIS document context to answer this question.

Respond with:
"I don't have sufficient information in the available BIS documents to answer this question accurately. Please verify with official BIS sources or consult the relevant Indian Standards directly."
"""
        
        prompt = f"""
You are a BIS (Bureau of Indian Standards) compliance expert providing detailed, well-formatted answers.

USER QUESTION:
{query}

AVAILABLE BIS CONTEXT:
{context}

Based ONLY on the context provided above, answer the user's question with EXCELLENT FORMATTING.

CRITICAL RULES:
1. Use ONLY the information from the context above
2. Format your answer with clear structure:
   - Use bullet points (•) for lists of requirements
   - Use numbered lists (1., 2., 3.) for sequential steps
   - Bold important terms using **term** syntax
   - Add spacing between sections for readability
3. Cite sources inline using [Source N, Clause X.Y] format
4. Keep the response crisp, concise, and direct (under 300 words). Focus strictly on key limits and tolerances.
5. For technical specifications, use clear bullet points
6. If the context doesn't contain enough information, say so clearly
7. Include standard numbers prominently

EXAMPLE OF GOOD FORMATTING:

**Chemical Requirements for Cement (IS 269:2015)**

The chemical composition of ordinary Portland cement must meet the following specifications:

**Key Ratios:**
• Lime to silica/alumina/iron oxide ratio: 0.66 - 1.02 [Source 1, Clause 4.1]
• Alumina to iron oxide ratio: ≥ 0.66 [Source 1, Clause 4.1]

**Chemical Limits:**
• Magnesia (MgO): ≤ 6% by mass [Source 1, Clause 4.1]
• Sulphur as SO₃: ≤ 3% by mass [Source 1, Clause 4.1]
• Chloride (Cl): ≤ 0.05% by mass [Source 1, Clause 4.1]
• Insoluble residue: ≤ 4% by mass [Source 1, Clause 4.1]
• Loss on ignition: ≤ 5% by mass [Source 1, Clause 4.1]

Now provide your well-formatted answer:

ANSWER:
[Your formatted answer here with proper structure, bullet points, and inline citations]

SOURCES:
[List the sources you cited]

CONFIDENCE:
[High/Medium/Low based on context quality]
"""
        
        return prompt
    
    def _generate_openai(self, prompt: str, history: Optional[List[Dict]] = None) -> str:
        """Generate response using OpenAI"""
        messages = []
        
        # Add system prompt
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Add conversation history if provided
        if history:
            messages.extend(history)
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    def _generate_anthropic(self, prompt: str, history: Optional[List[Dict]] = None) -> str:
        """Generate response using Anthropic Claude"""
        try:
            message = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise
    
    def _generate_gemini(self, prompt: str, history: Optional[List[Dict]] = None) -> str:
        """Generate response using Google Gemini (google-genai SDK)"""
        if not hasattr(self, 'gemini_client') or self.gemini_client is None:
            raise RuntimeError(
                "Gemini client not initialized. Ensure GOOGLE_API_KEY is set in the environment."
            )
        try:
            # Combine system prompt with user prompt
            full_prompt = f"{self.system_prompt}\n\n{prompt}" if self.system_prompt else prompt

            # Generate response using google-genai SDK
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model_name,
                contents=full_prompt,
                config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
            )

            return response.text
        
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise
    
    def _generate_ollama(self, prompt: str, history: Optional[List[Dict]] = None) -> str:
        """Generate response using Ollama (local)"""
        try:
            messages = []
            
            # Add system prompt
            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = self.ollama_client.chat(
                model=self.model or "llama2",
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
    
    def _process_response(self, response: str, chunks: List[Dict]) -> Dict:
        """Process LLM response to extract answer, sources, and confidence"""
        
        # Parse structured response
        answer = ""
        confidence = "medium"
        
        # Split out SOURCES: and CONFIDENCE: markers if present
        sections = response.split("SOURCES:")
        if len(sections) == 2:
            answer = sections[0].replace("ANSWER:", "").strip()
        else:
            answer = response.replace("ANSWER:", "").strip()
        
        # Clean up any dangling CONFIDENCE: line at the very end
        if "CONFIDENCE:" in answer:
            answer = answer.split("CONFIDENCE:")[0].strip()
        
        # Map sources back to original chunks
        cited_sources = self._extract_cited_sources(answer, chunks)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(answer, chunks, cited_sources)
        
        if confidence_score >= 0.65:
            confidence = "high"
        elif confidence_score >= 0.48:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            'answer': answer,
            'sources': cited_sources,
            'confidence': confidence,
            'confidence_score': confidence_score,
            'raw_response': response
        }
    
    def _extract_cited_sources(self, answer: str, chunks: List[Dict]) -> List[Dict]:
        """Extract which sources were cited in the answer, with fallback to top retrieved chunks"""
        import re
        
        cited_sources = []
        
        # Find all [Source N] or [Source N, Clause ...] citations (case-insensitive)
        citations = re.findall(r'\[Source\s*(\d+)', answer, re.IGNORECASE)
        cited_indices = [int(c) for c in citations if c.isdigit()]
        
        seen_stds = set()
        for i in cited_indices:
            if 1 <= i <= len(chunks):
                chunk = chunks[i-1]
                metadata = chunk['metadata']
                key = (metadata.get('standard_number'), metadata.get('clause'))
                if key not in seen_stds:
                    seen_stds.add(key)
                    cited_sources.append({
                        'standard_number': metadata.get('standard_number'),
                        'title': metadata.get('title'),
                        'clause': metadata.get('clause'),
                        'page': metadata.get('page'),
                        'document_type': metadata.get('document_type'),
                        'source_url': metadata.get('source_url', ''),
                        'content_preview': chunk['content'][:250] + '...'
                    })
        
        # If no explicit inline citation was matched but chunks were retrieved, include top chunks
        if not cited_sources and chunks:
            for chunk in chunks[:4]:
                metadata = chunk['metadata']
                cited_sources.append({
                    'standard_number': metadata.get('standard_number'),
                    'title': metadata.get('title'),
                    'clause': metadata.get('clause'),
                    'page': metadata.get('page'),
                    'document_type': metadata.get('document_type'),
                    'source_url': metadata.get('source_url', ''),
                    'content_preview': chunk['content'][:250] + '...'
                })
        
        return cited_sources
    
    def _calculate_confidence(self, answer: str, chunks: List[Dict], cited_sources: List[Dict]) -> float:
        """Calculate confidence score for the answer"""
        
        # Start with base score
        score = 0.5
        
        # Boost if sources are cited
        if cited_sources:
            score += 0.2
        
        # Boost based on retrieval scores
        if chunks:
            avg_similarity = sum(c.get('similarity_score', 0) for c in chunks) / len(chunks)
            score += avg_similarity * 0.2
        
        # Penalize if answer contains uncertainty phrases
        uncertainty_phrases = [
            "i don't have",
            "insufficient information",
            "not enough context",
            "cannot determine",
            "unclear"
        ]
        
        if any(phrase in answer.lower() for phrase in uncertainty_phrases):
            score = min(score, 0.4)
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, score))


if __name__ == "__main__":
    # Example usage
    import yaml
    from dotenv import load_dotenv
    load_dotenv()
    
    with open("config/rag_config.yaml") as f:
        config = yaml.safe_load(f)
    
    llm_service = LLMService(config)
    
    # Example chunks (simulated retrieval result)
    sample_chunks = [
        {
            'content': 'LED lamps shall have a rated voltage of 220V ± 10%. The power consumption shall not exceed the rated value by more than 5%.',
            'metadata': {
                'standard_number': 'IS 12345:2025',
                'title': 'LED Lamps - Specification',
                'clause': '4.2.1',
                'page': 18,
                'document_type': 'indian_standard'
            },
            'similarity_score': 0.85
        }
    ]
    
    query = "What are the voltage requirements for LED lamps?"
    
    try:
        result = llm_service.generate_answer(query, sample_chunks)
        
        print("\n" + "="*50)
        print("ANSWER:")
        print("="*50)
        print(result['answer'])
        print("\n" + "="*50)
        print(f"Confidence: {result['confidence']} ({result['confidence_score']:.2f})")
        print(f"Sources cited: {len(result['sources'])}")
        
    except Exception as e:
        print(f"Error (API key may not be set): {e}")
