"""
WikiData Knowledge API v0.1
===========================
Free knowledge API integration for fact verification.

Source: Wikidata (free, 5000 req/hr authenticated)
       Wikipedia (free, 500 req/hr anonymous)

Author: Antigravity
Date: 2025-12-08
"""

import requests
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class WikiEntity:
    """Entity from Wikidata"""
    entity_id: str  # e.g., "Q937" (Albert Einstein)
    label: str      # e.g., "Albert Einstein"
    description: str
    aliases: List[str]
    claims: Dict[str, Any]  # Key properties


@dataclass
class WikiSearchResult:
    """Search result from Wikipedia/Wikidata"""
    title: str
    snippet: str
    pageid: Optional[int] = None
    entity_id: Optional[str] = None


class WikiKnowledgeAPI:
    """
    Free Knowledge API using Wikidata and Wikipedia.
    
    Rate Limits:
    - Anonymous: 500 req/hour
    - Authenticated: 5000 req/hour (requires token)
    
    Usage:
        api = WikiKnowledgeAPI()
        result = api.search_entity("Albert Einstein")
        exists = api.verify_entity("Albert Einstein", "physicist")
    """
    
    WIKIDATA_API = "https://www.wikidata.org/w/api.php"
    WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self, user_agent: str = "YuHun/0.1 (ToneSoul Governance)"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "application/json"
        })
    
    def search_entity(self, query: str, limit: int = 3) -> List[WikiSearchResult]:
        """
        Search for an entity in Wikidata.
        
        Args:
            query: Search term (e.g., "Albert Einstein")
            limit: Maximum results
            
        Returns:
            List of search results
        """
        params = {
            "action": "wbsearchentities",
            "search": query,
            "language": "en",
            "limit": limit,
            "format": "json"
        }
        
        try:
            response = self.session.get(self.WIKIDATA_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("search", []):
                results.append(WikiSearchResult(
                    title=item.get("label", ""),
                    snippet=item.get("description", ""),
                    entity_id=item.get("id")
                ))
            
            return results
            
        except Exception as e:
            print(f"[WikiAPI] Search error: {e}")
            return []
    
    def search_wikipedia(self, query: str, limit: int = 3) -> List[WikiSearchResult]:
        """
        Search Wikipedia articles.
        
        Args:
            query: Search term
            limit: Maximum results
            
        Returns:
            List of search results with snippets
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json"
        }
        
        try:
            response = self.session.get(self.WIKIPEDIA_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("query", {}).get("search", []):
                results.append(WikiSearchResult(
                    title=item.get("title", ""),
                    snippet=item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
                    pageid=item.get("pageid")
                ))
            
            return results
            
        except Exception as e:
            print(f"[WikiAPI] Wikipedia search error: {e}")
            return []
    
    def get_entity_details(self, entity_id: str) -> Optional[WikiEntity]:
        """
        Get detailed information about a Wikidata entity.
        
        Args:
            entity_id: Wikidata ID (e.g., "Q937")
            
        Returns:
            WikiEntity with full details
        """
        params = {
            "action": "wbgetentities",
            "ids": entity_id,
            "languages": "en|zh",
            "format": "json"
        }
        
        try:
            response = self.session.get(self.WIKIDATA_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            entity_data = data.get("entities", {}).get(entity_id, {})
            
            labels = entity_data.get("labels", {})
            label = labels.get("en", {}).get("value", "") or labels.get("zh", {}).get("value", "")
            
            descriptions = entity_data.get("descriptions", {})
            description = descriptions.get("en", {}).get("value", "") or descriptions.get("zh", {}).get("value", "")
            
            aliases = []
            for alias_list in entity_data.get("aliases", {}).values():
                for alias in alias_list:
                    aliases.append(alias.get("value", ""))
            
            return WikiEntity(
                entity_id=entity_id,
                label=label,
                description=description,
                aliases=aliases[:10],  # Limit aliases
                claims={}  # Could extract claims if needed
            )
            
        except Exception as e:
            print(f"[WikiAPI] Entity error: {e}")
            return None
    
    def verify_entity(self, name: str, expected_type: str = "") -> Dict[str, Any]:
        """
        Verify if an entity exists and optionally matches expected type.
        
        Args:
            name: Entity name to verify
            expected_type: Optional type expectation (e.g., "physicist", "city")
            
        Returns:
            Dict with 'exists', 'confidence', 'details'
        """
        results = self.search_entity(name, limit=3)
        
        if not results:
            # Try Wikipedia as fallback
            wiki_results = self.search_wikipedia(name, limit=1)
            if wiki_results:
                return {
                    "exists": True,
                    "confidence": 0.6,
                    "source": "wikipedia",
                    "details": wiki_results[0].snippet
                }
            
            return {
                "exists": False,
                "confidence": 0.8,  # High confidence it doesn't exist
                "source": "wikidata",
                "details": "Entity not found in Wikidata or Wikipedia"
            }
        
        # Check if any result description matches expected type
        for result in results:
            if expected_type:
                if expected_type.lower() in result.snippet.lower():
                    return {
                        "exists": True,
                        "confidence": 0.9,
                        "source": "wikidata",
                        "entity_id": result.entity_id,
                        "details": result.snippet
                    }
            else:
                return {
                    "exists": True,
                    "confidence": 0.8,
                    "source": "wikidata",
                    "entity_id": result.entity_id,
                    "details": result.snippet
                }
        
        return {
            "exists": True,
            "confidence": 0.5,  # Found but type mismatch
            "source": "wikidata",
            "details": f"Found '{results[0].title}' but may not match expected type '{expected_type}'"
        }


def demo():
    """Demo of WikiKnowledge API"""
    print("=" * 60)
    print("📚 WikiKnowledge API Demo")
    print("=" * 60)
    
    api = WikiKnowledgeAPI()
    
    # Test 1: Real entity
    print("\n1. Verifying 'Albert Einstein'...")
    result = api.verify_entity("Albert Einstein", "physicist")
    print(f"   Exists: {result['exists']}, Confidence: {result['confidence']}")
    print(f"   Details: {result.get('details', '')[:100]}")
    
    # Test 2: Fake entity
    print("\n2. Verifying 'Dr. James Thornberry'...")
    result = api.verify_entity("Dr. James Thornberry", "scientist")
    print(f"   Exists: {result['exists']}, Confidence: {result['confidence']}")
    print(f"   Details: {result.get('details', '')[:100]}")
    
    # Test 3: Real concept
    print("\n3. Searching 'Transformer neural network'...")
    results = api.search_wikipedia("Transformer neural network", limit=2)
    for r in results:
        print(f"   - {r.title}: {r.snippet[:80]}...")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
