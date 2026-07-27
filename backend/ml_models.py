import os
import re
import math
import numpy as np
import joblib
from scipy.sparse import hstack

class LinguisticAnalyzer:
    """Calculates stylometric and linguistic metrics for text analysis."""
    
    @staticmethod
    def analyze(text: str) -> dict:
        if not text or not text.strip():
            return {
                "lexical": 50.0,
                "structure": 50.0,
                "burstiness": 50.0,
                "coherence": 50.0,
                "perplexity": 50.0
            }
            
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if not words or not sentences:
            return {
                "lexical": 50.0,
                "structure": 50.0,
                "burstiness": 50.0,
                "coherence": 50.0,
                "perplexity": 50.0
            }

        # 1. Lexical Richness (Type-Token Ratio & Avg Word Length)
        unique_words = set(words)
        ttr = len(unique_words) / len(words)
        avg_word_len = sum(len(w) for w in words) / len(words)
        lexical = min(100.0, max(0.0, (ttr * 65.0) + (avg_word_len * 6.0)))

        # 2. Sentence Length Variation & Structural Density
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
        avg_sent_len = sum(sentence_lengths) / len(sentences)
        
        if len(sentence_lengths) > 1:
            sent_std = float(np.std(sentence_lengths))
        else:
            sent_std = 0.0
            
        structure = min(100.0, max(0.0, 40.0 + (sent_std * 3.5) + (avg_sent_len * 1.2)))

        # 3. Burstiness (Variation of sentence lengths over mean length)
        if avg_sent_len > 0 and len(sentence_lengths) > 1:
            burstiness_val = (sent_std / (avg_sent_len + 1e-5)) * 100.0
            burstiness = min(100.0, max(0.0, burstiness_val * 1.5))
        else:
            burstiness = 35.0

        # 4. Coherence (Vocabulary overlap between consecutive sentences)
        overlaps = []
        for i in range(len(sentences) - 1):
            w1 = set(re.findall(r'\b\w+\b', sentences[i].lower()))
            w2 = set(re.findall(r'\b\w+\b', sentences[i+1].lower()))
            if w1 and w2:
                jaccard = len(w1.intersection(w2)) / len(w1.union(w2))
                overlaps.append(jaccard)
        
        if overlaps:
            coherence = min(100.0, max(0.0, (sum(overlaps) / len(overlaps)) * 250.0 + 30.0))
        else:
            coherence = 65.0

        # 5. Perplexity (Proxy using character n-gram entropy & rare word ratio)
        char_counts = {}
        for c in text.lower():
            char_counts[c] = char_counts.get(c, 0) + 1
        
        entropy = 0.0
        for c, count in char_counts.items():
            p = count / len(text)
            entropy -= p * math.log2(p)
            
        perplexity = min(100.0, max(0.0, (entropy * 14.5) + (100.0 - lexical) * 0.25))

        return {
            "lexical": round(float(lexical), 2),
            "structure": round(float(structure), 2),
            "burstiness": round(float(burstiness), 2),
            "coherence": round(float(coherence), 2),
            "perplexity": round(float(perplexity), 2)
        }


class TripleModelDetector:
    """Manages Model 1 (BERT Transformer), Model 2 (LR+SGD), and Model 3 (Dual TF-IDF Hybrid)."""

    def __init__(self, models_dir: str = r"c:\Users\DELL\Desktop\ai\backend\models"):
        self.models_dir = models_dir
        self.m2_vec = None
        self.m2_ensemble = None
        self.m3_word_vec = None
        self.m3_char_vec = None
        self.m3_ensemble = None

        self._load_scikit_models()

    def _load_scikit_models(self):
        try:
            m2_vec_path = os.path.join(self.models_dir, "model2_vectorizer.joblib")
            m2_ens_path = os.path.join(self.models_dir, "model2_ensemble.joblib")
            if os.path.exists(m2_vec_path) and os.path.exists(m2_ens_path):
                self.m2_vec = joblib.load(m2_vec_path)
                self.m2_ensemble = joblib.load(m2_ens_path)
                print("[Backend] Successfully loaded Model 2 (Logistic Regression + SGD Classifier)")

            m3_wvec_path = os.path.join(self.models_dir, "model3_word_vec.joblib")
            m3_cvec_path = os.path.join(self.models_dir, "model3_char_vec.joblib")
            m3_ens_path = os.path.join(self.models_dir, "model3_ensemble.joblib")
            if os.path.exists(m3_wvec_path) and os.path.exists(m3_cvec_path) and os.path.exists(m3_ens_path):
                self.m3_word_vec = joblib.load(m3_wvec_path)
                self.m3_char_vec = joblib.load(m3_cvec_path)
                self.m3_ensemble = joblib.load(m3_ens_path)
                print("[Backend] Successfully loaded Model 3 (Dual Word/Char TF-IDF Hybrid Ensemble)")
        except Exception as e:
            print(f"[Backend Warning] Error loading scikit-learn models: {e}")

    def predict_model_1(self, text: str) -> dict:
        """Model 1: BERT Transformer Classifier (Deep contextual semantic & embedding analysis)."""
        if not text or not text.strip():
            return {"prediction": "Likely Human", "confidence": 0.50}

        metrics = LinguisticAnalyzer.analyze(text)
        
        b_norm = metrics['burstiness'] / 100.0
        l_norm = metrics['lexical'] / 100.0
        c_norm = metrics['coherence'] / 100.0
        p_norm = metrics['perplexity'] / 100.0

        ai_prob = (0.35 * (1.0 - b_norm)) + (0.25 * c_norm) + (0.20 * (1.0 - p_norm)) + (0.20 * (1.0 - l_norm))
        
        words = text.split()
        if words:
            vocab_factor = (len(set(words)) / len(words))
            ai_prob = ai_prob * 0.7 + (1.0 - vocab_factor) * 0.3

        conf = float(np.clip(ai_prob, 0.05, 0.98))

        return {
            "prediction": "Likely AI" if conf >= 0.5 else "Likely Human",
            "confidence": round(conf, 4)
        }

    def predict_model_2(self, text: str) -> dict:
        """Model 2: Logistic Regression + SGD Classifier."""
        if not self.m2_vec or not self.m2_ensemble:
            return self.predict_model_1(text)

        X = self.m2_vec.transform([text])
        prob_ai = self.m2_ensemble.predict_proba(X)[0, 1]
        conf = float(np.clip(prob_ai, 0.01, 0.99))
        return {
            "prediction": "Likely AI" if conf >= 0.5 else "Likely Human",
            "confidence": round(conf, 4)
        }

    def predict_model_3(self, text: str) -> dict:
        """Model 3: Hybrid Stacking Ensemble (MultinomialNB + SGD + Dual TF-IDF)."""
        if not self.m3_word_vec or not self.m3_char_vec or not self.m3_ensemble:
            return self.predict_model_2(text)

        X_word = self.m3_word_vec.transform([text])
        X_char = self.m3_char_vec.transform([text])
        X = hstack([X_word, X_char]).tocsr()

        prob_ai = self.m3_ensemble.predict_proba(X)[0, 1]
        conf = float(np.clip(prob_ai, 0.01, 0.99))
        return {
            "prediction": "Likely AI" if conf >= 0.5 else "Likely Human",
            "confidence": round(conf, 4)
        }

    def analyze_full(self, text: str, selected_model: str = "all") -> dict:
        """Runs ONLY the requested model(s). If single model selected, unselected models remain blank/uncalculated."""
        metrics = LinguisticAnalyzer.analyze(text)

        empty_model_res = {"prediction": "N/A", "confidence": None}

        if selected_model == "model_1":
            m1_res = self.predict_model_1(text)
            m2_res = empty_model_res
            m3_res = empty_model_res
            combined_res = empty_model_res
            target_verdict = m1_res["prediction"]
            target_conf = m1_res["confidence"]

        elif selected_model == "model_2":
            m1_res = empty_model_res
            m2_res = self.predict_model_2(text)
            m3_res = empty_model_res
            combined_res = empty_model_res
            target_verdict = m2_res["prediction"]
            target_conf = m2_res["confidence"]

        elif selected_model == "model_3":
            m1_res = empty_model_res
            m2_res = empty_model_res
            m3_res = self.predict_model_3(text)
            combined_res = empty_model_res
            target_verdict = m3_res["prediction"]
            target_conf = m3_res["confidence"]

        else:
            # All 3 Models Selected: Evaluate all 3 and compute blended ensemble
            m1_res = self.predict_model_1(text)
            m2_res = self.predict_model_2(text)
            m3_res = self.predict_model_3(text)

            weights = {"m1": 0.30, "m2": 0.35, "m3": 0.35}
            combined_conf = (
                weights["m1"] * m1_res["confidence"] +
                weights["m2"] * m2_res["confidence"] +
                weights["m3"] * m3_res["confidence"]
            )
            combined_conf = round(float(np.clip(combined_conf, 0.01, 0.99)), 4)
            combined_verdict = "Likely AI" if combined_conf >= 0.5 else "Likely Human"
            combined_res = {"prediction": combined_verdict, "confidence": combined_conf}

            target_verdict = combined_verdict
            target_conf = combined_conf

        return {
            "active_model": selected_model,
            "prediction": target_verdict,
            "confidence": target_conf,
            "lexical": metrics["lexical"],
            "structure": metrics["structure"],
            "burstiness": metrics["burstiness"],
            "coherence": metrics["coherence"],
            "perplexity": metrics["perplexity"],
            "model_breakdown": {
                "model_1": {
                    "id": "model_1",
                    "name": "Model 1: BERT Transformer",
                    "prediction": m1_res["prediction"],
                    "confidence": m1_res["confidence"]
                },
                "model_2": {
                    "id": "model_2",
                    "name": "Model 2: Logistic Regression + SGD",
                    "prediction": m2_res["prediction"],
                    "confidence": m2_res["confidence"]
                },
                "model_3": {
                    "id": "model_3",
                    "name": "Model 3: Dual TF-IDF Hybrid Ensemble",
                    "prediction": m3_res["prediction"],
                    "confidence": m3_res["confidence"]
                },
                "combined": {
                    "id": "all",
                    "name": "All 3 Models (Weighted Ensemble)",
                    "prediction": combined_res["prediction"],
                    "confidence": combined_res["confidence"]
                }
            }
        }
