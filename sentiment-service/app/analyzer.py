from textblob import TextBlob

class SentimentAnalyzer:
    """Analizador de sentimientos para feedback de usuarios"""
    
    @staticmethod
    def analyze(text: str) -> dict:
        """
        Analiza el sentimiento de un texto.
        
        Args:
            text: Texto a analizar (feedback del usuario)
            
        Returns:
            dict con sentiment (positive/negative/neutral) y score
        """
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.0
            }
        
        # Analizar con TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 (negativo) a 1 (positivo)
        
        # Clasificar
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": round(polarity, 3),
            "confidence": round(abs(polarity), 3),
            "text_length": len(text)
        }
    
    @staticmethod
    def batch_analyze(texts: list[str]) -> list[dict]:
        """Analiza múltiples textos"""
        return [SentimentAnalyzer.analyze(text) for text in texts]