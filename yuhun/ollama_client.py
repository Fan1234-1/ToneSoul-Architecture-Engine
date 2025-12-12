"""
Ollama Client - Legacy Interface
================================
This module is kept for backward compatibility.
New code should use body/llm_bridge.py directly.
"""

import sys
import os

# Add body to path for llm_bridge import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'body'))

try:
    from llm_bridge import create_ollama_bridge
    _bridge = None
    
    def generate(model: str, prompt: str) -> str:
        """
        Generate response from Ollama.
        
        This is a legacy interface. New code should use:
            from body.llm_bridge import create_ollama_bridge
            bridge = create_ollama_bridge(model)
            response = bridge.generate(prompt)
        """
        global _bridge
        if _bridge is None or _bridge.config.model != model:
            _bridge = create_ollama_bridge(model)
        return _bridge.generate(prompt)
        
except ImportError:
    # Fallback to direct implementation if llm_bridge not available
    import requests
    
    OLLAMA_HOST = "http://localhost:11434"
    
    def generate(model: str, prompt: str) -> str:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            resp = requests.post(url, json=payload, timeout=600)
            resp.raise_for_status()
            data = resp.json()
            return data["response"]
        except requests.exceptions.RequestException as e:
            return f"Error calling Ollama: {e}"
