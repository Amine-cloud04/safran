import os
import numpy as np
from typing import Dict, List, Tuple, Optional
from sentence_transformers import SentenceTransformer
import faiss
from data.kb_rh import KB_RH, PROFILE_ADAPTATIONS
import logging

logger = logging.getLogger(__name__)

class ChatbotBackend:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.kb_rh = KB_RH
        self.profile_adaptations = PROFILE_ADAPTATIONS
        self.index = None
        self.kb_embeddings = None
        self.kb_keys = []
        self._build_index()
        
    def _build_index(self):
        kb_texts = []
        for key, value in self.kb_rh.items():
            if key != "default" and isinstance(value, dict):
                keywords = value.get("keywords", [])
                for kw in keywords:
                    kb_texts.append(kw)
                    self.kb_keys.append(key)
        
        if kb_texts:
            self.kb_embeddings = self.model.encode(kb_texts)
            self.index = faiss.IndexFlatL2(self.kb_embeddings.shape[1])
            self.index.add(self.kb_embeddings.astype(np.float32))
    
    def _detect_blocked_question(self, question: str) -> bool:
        blocked_keywords = ["salaire", "médical", "sanction", "discipline"]
        question_lower = question.lower()
        for keyword in blocked_keywords:
            if keyword in question_lower:
                return True
        return False
    
    def _find_best_match(self, question: str, top_k: int = 1) -> Tuple[str, float]:
        if self.index is None or self.kb_embeddings is None:
            return "default", 0.0
        
        question_embedding = self.model.encode([question])
        distances, indices = self.index.search(question_embedding.astype(np.float32), top_k)
        
        if len(indices[0]) > 0:
            best_idx = indices[0][0]
            distance = distances[0][0]
            confidence = 1.0 / (1.0 + distance)
            matched_key = self.kb_keys[best_idx]
            return matched_key, confidence
        
        return "default", 0.0
    
    def _get_response(self, intent_key: str, profile: str, language: str) -> str:
        if intent_key not in self.kb_rh:
            return self.kb_rh["default"]["response"]
        
        intent_data = self.kb_rh[intent_key]
        
        if intent_data.get("blocked"):
            return intent_data["responses"]["default"]
        
        responses = intent_data.get("responses", {})
        
        if profile in responses:
            return responses[profile]
        
        if language == "ar" and "darija" in responses:
            return responses["darija"]
        
        return responses.get("default", self.kb_rh["default"]["response"])
    
    def ask(self, question: str, profile: str = "CDI", language: str = "fr") -> Dict:
        if self._detect_blocked_question(question):
            return {
                "response": "Je ne peux pas répondre à cette question pour des raisons de confidentialité. Contactez RH directement.",
                "confidence": 1.0,
                "intent": "blocked"
            }
        
        intent_key, confidence = self._find_best_match(question)
        response = self._get_response(intent_key, profile, language)
        
        return {
            "response": response,
            "confidence": float(confidence),
            "intent": intent_key,
            "profile": profile,
            "language": language
        }
    
    def get_available_profiles(self) -> List[str]:
        return list(self.profile_adaptations.keys())
    
    def get_available_languages(self) -> List[str]:
        return ["fr", "ar"]
