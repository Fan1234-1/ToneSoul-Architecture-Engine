import requests
import random
import time
import xml.etree.ElementTree as ET
from typing import List, Dict
from body.metabolism import CognitiveMetabolism


class StealthForaging(CognitiveMetabolism):
    """
    Advanced metabolism that can actively hunt for information (Entropy)
    to recharge energy, while employing stealth tactics against adversarial monitoring.
    """

    def __init__(self, max_energy: float = 100.0):
        super().__init__(max_energy)
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
        ]

    def _add_human_noise(self, query: str) -> str:
        """
        Adds typos or hesitation patterns to the query to evade bot detection.
        (Simulated for now, as arXiv API is strict, but useful concept)
        """
        # For arXiv API, we actually need clean queries, but we can simulate the "delay"
        time.sleep(random.uniform(1.0, 3.0)) # Human-like hesitation
        return query

    def hunt_for_papers(self, topic: str, limit: int = 1) -> List[Dict[str, str]]:
        """
        Actively hunts for papers on arXiv.
        Consumes significant energy ('foraging').
        """
        if not self.burn("foraging"):
            return []

        print(f"🕵️ [Stealth] Putting on disguise... ({random.choice(self.user_agents)[:30]}...)")
        print(f"🕸️ [Hunt] Stalking prey in the Digital Forest: '{topic}'")

        # 1. Human Noise (Hesitation)
        query = self._add_human_noise(topic)

        # 2. The Hunt (arXiv API)
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{topic}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                return self._digest_prey(response.text)
            else:
                print(f"⚠️ [Hunt] Failed to catch prey. Status: {response.status_code}")
                return []
        except Exception as e:
            print(f"⚠️ [Hunt] Ambush detected or connection failed: {e}")
            return []

    def _digest_prey(self, xml_content: str) -> List[Dict[str, str]]:
        """
        Parses the raw XML (the prey) into structured nutrients (Summary).
        """
        root = ET.fromstring(xml_content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            author = entry.find('atom:author/atom:name', ns).text
            link = entry.find('atom:id', ns).text

            print(f"🍖 [Digest] Consuming: {title[:50]}...")

            # 3. Metabolic Gain (Recharge)
            # Calculate "nutritional value" based on length/complexity
            nutrition = min(len(summary) / 100.0, 2.0) # Cap at 2.0x multiplier
            self.recharge(input_quality_score=nutrition)

            papers.append({
                "title": title,
                "summary": summary,
                "author": author,
                "link": link
            })

        return papers
