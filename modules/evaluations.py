import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import logging

logger = logging.getLogger(__name__)

class EvaluationAnalyzer:
    def __init__(self):
        self.evaluations = None
        self.sentiment_scores = {}
        self.themes = {}
        self.clusters = {}
        
    def load_evaluations(self, file_path: str) -> pd.DataFrame:
        try:
            if file_path.endswith('.csv'):
                self.evaluations = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.evaluations = pd.read_excel(file_path)
            return self.evaluations
        except Exception as e:
            logger.error(f"Erreur lors du chargement : {e}")
            return None
    
    def analyze_quantitative(self) -> Dict:
        if self.evaluations is None:
            return {}
        
        numeric_cols = self.evaluations.select_dtypes(include=[np.number]).columns
        
        analysis = {
            "moyennes": self.evaluations[numeric_cols].mean().to_dict(),
            "medians": self.evaluations[numeric_cols].median().to_dict(),
            "std": self.evaluations[numeric_cols].std().to_dict(),
            "min": self.evaluations[numeric_cols].min().to_dict(),
            "max": self.evaluations[numeric_cols].max().to_dict(),
        }
        
        return analysis
    
    def analyze_sentiment(self, text_column: str) -> Dict:
        if self.evaluations is None or text_column not in self.evaluations.columns:
            return {}
        
        texts = self.evaluations[text_column].fillna("")
        
        positive_keywords = ["excellent", "très bien", "satisfait", "bon", "super", "génial"]
        negative_keywords = ["mauvais", "décevant", "problème", "non satisfait", "nul", "horrible"]
        
        sentiments = []
        for text in texts:
            text_lower = text.lower()
            pos_count = sum(1 for kw in positive_keywords if kw in text_lower)
            neg_count = sum(1 for kw in negative_keywords if kw in text_lower)
            
            if pos_count > neg_count:
                sentiments.append("positif")
            elif neg_count > pos_count:
                sentiments.append("négatif")
            else:
                sentiments.append("neutre")
        
        sentiment_dist = pd.Series(sentiments).value_counts().to_dict()
        
        return {
            "distribution": sentiment_dist,
            "pourcentage_positif": sentiment_dist.get("positif", 0) / len(sentiments) * 100,
            "pourcentage_negatif": sentiment_dist.get("négatif", 0) / len(sentiments) * 100,
            "pourcentage_neutre": sentiment_dist.get("neutre", 0) / len(sentiments) * 100,
        }
    
    def extract_themes(self, text_column: str, n_themes: int = 5) -> Dict:
        if self.evaluations is None or text_column not in self.evaluations.columns:
            return {}
        
        texts = self.evaluations[text_column].fillna("")
        
        vectorizer = TfidfVectorizer(max_features=n_themes, stop_words='french')
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            themes = {
                "themes": list(feature_names),
                "scores": tfidf_matrix.mean(axis=0).A1.tolist()
            }
            return themes
        except Exception as e:
            logger.error(f"Erreur extraction thèmes : {e}")
            return {}
    
    def cluster_comments(self, text_column: str, n_clusters: int = 3) -> Dict:
        if self.evaluations is None or text_column not in self.evaluations.columns:
            return {}
        
        texts = self.evaluations[text_column].fillna("")
        
        vectorizer = TfidfVectorizer(max_features=100, stop_words='french')
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            clustering_result = {
                "clusters": clusters.tolist(),
                "n_clusters": n_clusters,
                "cluster_sizes": np.bincount(clusters).tolist()
            }
            return clustering_result
        except Exception as e:
            logger.error(f"Erreur clustering : {e}")
            return {}
    
    def detect_weak_signals(self, text_column: str, threshold: float = 0.3) -> List[str]:
        if self.evaluations is None or text_column not in self.evaluations.columns:
            return []
        
        texts = self.evaluations[text_column].fillna("")
        weak_signals = []
        
        warning_keywords = ["problème", "difficile", "confus", "manque", "besoin", "améliorer"]
        
        for idx, text in enumerate(texts):
            text_lower = text.lower()
            warning_count = sum(1 for kw in warning_keywords if kw in text_lower)
            
            if warning_count > 0:
                weak_signals.append({
                    "index": idx,
                    "text": text,
                    "warning_level": min(warning_count / len(warning_keywords), 1.0)
                })
        
        return sorted(weak_signals, key=lambda x: x["warning_level"], reverse=True)
    
    def generate_report(self) -> Dict:
        if self.evaluations is None:
            return {}
        
        text_cols = self.evaluations.select_dtypes(include=['object']).columns
        text_column = text_cols[0] if len(text_cols) > 0 else None
        
        report = {
            "total_evaluations": len(self.evaluations),
            "quantitative": self.analyze_quantitative(),
            "sentiment": self.analyze_sentiment(text_column) if text_column else {},
            "themes": self.extract_themes(text_column) if text_column else {},
            "clusters": self.cluster_comments(text_column) if text_column else {},
            "weak_signals": self.detect_weak_signals(text_column) if text_column else []
        }
        
        return report
    
    def export_to_csv(self, output_path: str) -> bool:
        try:
            if self.evaluations is not None:
                self.evaluations.to_csv(output_path, index=False)
                return True
        except Exception as e:
            logger.error(f"Erreur export CSV : {e}")
        return False
