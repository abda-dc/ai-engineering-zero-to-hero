import time
from typing import Optional, Dict, Any, Tuple
import math

class SemanticCache:
    """
    Dual-layer Cache:
    1. Exact Key-Value Cache (MD5/string hash)
    2. Semantic Vector Similarity Cache (Cosine threshold >= 0.92)
    Gracefully runs in-memory with optional Redis connection.
    """
    def __init__(self, threshold: float = 0.92):
        self.exact_cache: Dict[str, Tuple[str, float]] = {}
        self.vector_cache: list = []
        self.threshold = threshold
        self.hits = 0
        self.misses = 0

    def _cosine_similarity(self, u: list, v: list) -> float:
        dot = sum(a * b for a, b in zip(u, v))
        nu = math.sqrt(sum(a * a for a in u))
        nv = math.sqrt(sum(b * b for b in v))
        if nu == 0 or nv == 0:
            return 0.0
        return dot / (nu * nv)

    def get_exact(self, key: str) -> Optional[str]:
        now = time.time()
        if key in self.exact_cache:
            val, expires = self.exact_cache[key]
            if expires > now:
                self.hits += 1
                return val
            del self.exact_cache[key]
        self.misses += 1
        return None

    def set_exact(self, key: str, value: str, ttl_seconds: int = 3600):
        self.exact_cache[key] = (value, time.time() + ttl_seconds)

    def get_semantic(self, query_vec: list) -> Optional[Dict[str, Any]]:
        now = time.time()
        self.vector_cache = [item for item in self.vector_cache if item["expires"] > now]
        
        best_sim = -1.0
        best_match = None
        for item in self.vector_cache:
            sim = self._cosine_similarity(query_vec, item["vector"])
            if sim > best_sim:
                best_sim = sim
                best_match = item
                
        if best_match and best_sim >= self.threshold:
            self.hits += 1
            return {
                "response": best_match["response"],
                "similarity": round(best_sim, 4),
                "matched_prompt": best_match["prompt"],
                "hit": True
            }
            
        self.misses += 1
        return None

    def set_semantic(self, query_vec: list, prompt: str, response: str, ttl_seconds: int = 3600):
        self.vector_cache.append({
            "vector": query_vec,
            "prompt": prompt,
            "response": response,
            "expires": time.time() + ttl_seconds
        })

    def get_stats(self) -> Dict[str, Any]:
        total = self.hits + self.misses
        hit_rate = (self.hits / total) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 4),
            "exact_cached_items": len(self.exact_cache),
            "semantic_cached_items": len(self.vector_cache)
        }

semantic_cache = SemanticCache()
