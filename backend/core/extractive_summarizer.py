"""
Extractive Summarization Module
Genera resúmenes seleccionando las frases más importantes del texto
Funciona mejor que modelos abstractivos para español conversacional
"""
import re
from typing import List, Tuple
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class ExtractiveSummarizer:
    """Genera resúmenes extractivos basados en relevancia de frases"""

    def __init__(self):
        """Inicializa el resumidor extractivo"""
        self.stop_words = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
            'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
            'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
            'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
            'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
            'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
            'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
            'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
            'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
            'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar',
            'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo',
            'decir', 'quien', 'mundo', 'te', 'les', 'fue', 'ha', 'es', 'son', 'una',
            'del', 'al', 'las', 'los', 'estos', 'estas', 'esos', 'esas', 'este', 'esta'
        ])

    def _split_sentences(self, text: str) -> List[str]:
        """
        Divide el texto en frases

        Args:
            text: Texto a dividir

        Returns:
            Lista de frases
        """
        # Limpiar texto
        text = text.replace('\n', ' ').strip()

        # Dividir por puntos, signos de interrogación y exclamación
        sentences = re.split(r'[.!?]+', text)

        # Limpiar y filtrar frases vacías
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]

        return sentences

    def _calculate_word_frequencies(self, sentences: List[str]) -> dict:
        """
        Calcula la frecuencia de palabras (excluyendo stop words)

        Args:
            sentences: Lista de frases

        Returns:
            Diccionario con frecuencias normalizadas
        """
        word_freq = Counter()

        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            for word in words:
                if word not in self.stop_words and len(word) > 2:
                    word_freq[word] += 1

        # Normalizar frecuencias
        max_freq = max(word_freq.values()) if word_freq else 1
        word_freq = {word: freq/max_freq for word, freq in word_freq.items()}

        return word_freq

    def _score_sentences(self, sentences: List[str], word_freq: dict) -> List[Tuple[str, float]]:
        """
        Asigna puntuación a cada frase basándose en frecuencia de palabras

        Args:
            sentences: Lista de frases
            word_freq: Frecuencias de palabras

        Returns:
            Lista de tuplas (frase, puntuación)
        """
        sentence_scores = []

        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            score = 0
            word_count = 0

            for word in words:
                if word in word_freq:
                    score += word_freq[word]
                    word_count += 1

            # Normalizar por longitud de frase
            if word_count > 0:
                score = score / word_count

            # Penalizar frases muy cortas o muy largas
            if len(words) < 5:
                score *= 0.5
            elif len(words) > 50:
                score *= 0.8

            sentence_scores.append((sentence, score))

        return sentence_scores

    def _select_top_sentences(
        self,
        sentence_scores: List[Tuple[str, float]],
        num_sentences: int,
        preserve_order: bool = True
    ) -> List[str]:
        """
        Selecciona las frases con mayor puntuación

        Args:
            sentence_scores: Lista de (frase, puntuación)
            num_sentences: Número de frases a seleccionar
            preserve_order: Si mantener el orden original

        Returns:
            Lista de frases seleccionadas
        """
        # Ordenar por puntuación
        sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

        # Seleccionar top N
        top_sentences = sorted_sentences[:num_sentences]

        if preserve_order:
            # Mantener orden original del texto
            original_order = {sent: i for i, (sent, _) in enumerate(sentence_scores)}
            top_sentences = sorted(top_sentences, key=lambda x: original_order[x[0]])

        return [sent for sent, score in top_sentences]

    def summarize(
        self,
        text: str,
        num_sentences: int = None,
        compression_ratio: float = 0.3,
        preserve_order: bool = True
    ) -> str:
        """
        Genera un resumen extractivo del texto

        Args:
            text: Texto a resumir
            num_sentences: Número de frases en el resumen (None = auto)
            compression_ratio: Ratio de compresión si num_sentences es None
            preserve_order: Si mantener orden original de frases

        Returns:
            Resumen del texto
        """
        if not text or len(text.strip()) < 50:
            logger.warning("Texto muy corto para resumir")
            return text

        try:
            # Dividir en frases
            sentences = self._split_sentences(text)

            if len(sentences) <= 3:
                logger.info("Texto muy corto, devolviendo original")
                return text

            # Calcular número de frases objetivo
            if num_sentences is None:
                num_sentences = max(2, int(len(sentences) * compression_ratio))

            num_sentences = min(num_sentences, len(sentences))

            logger.info(f"Resumiendo: {len(sentences)} frases → {num_sentences} frases")

            # Calcular frecuencias de palabras
            word_freq = self._calculate_word_frequencies(sentences)

            # Puntuar frases
            sentence_scores = self._score_sentences(sentences, word_freq)

            # Seleccionar mejores frases
            summary_sentences = self._select_top_sentences(
                sentence_scores,
                num_sentences,
                preserve_order
            )

            # Unir frases con puntos
            summary = '. '.join(summary_sentences)
            if not summary.endswith('.'):
                summary += '.'

            logger.info(f"✅ Resumen generado: {len(summary.split())} palabras")

            return summary

        except Exception as e:
            logger.error(f"Error al generar resumen: {e}")
            # Devolver primeras frases como fallback
            sentences = self._split_sentences(text)
            return '. '.join(sentences[:3]) + '.'


class HybridSummarizer:
    """
    Combina resumen extractivo y abstractivo
    Usa extractivo como fallback si el abstractivo falla
    """

    def __init__(self, abstractive_summarizer=None):
        """
        Args:
            abstractive_summarizer: Instancia de VideoSummarizer (opcional)
        """
        self.extractive = ExtractiveSummarizer()
        self.abstractive = abstractive_summarizer

    def summarize(
        self,
        text: str,
        use_abstractive: bool = True,
        **kwargs
    ) -> str:
        """
        Genera resumen usando el método más apropiado

        Args:
            text: Texto a resumir
            use_abstractive: Si intentar usar modelo abstractivo primero
            **kwargs: Argumentos adicionales
                - compression_ratio, num_sentences, preserve_order (extractivo)
                - max_length, min_length, num_beams, etc. (abstractivo)

        Returns:
            Resumen del texto
        """
        # Intentar resumen abstractivo si está disponible
        if use_abstractive and self.abstractive is not None:
            try:
                logger.info("Intentando resumen abstractivo...")

                # Filtrar parámetros para abstractivo
                abstractive_params = {
                    k: v for k, v in kwargs.items()
                    if k in ['max_length', 'min_length', 'num_beams', 'temperature',
                            'top_p', 'repetition_penalty', 'length_penalty',
                            'no_repeat_ngram_size', 'early_stopping', 'prefix']
                }

                summary = self.abstractive.summarize(text, **abstractive_params)

                # Validar calidad del resumen
                if self._is_good_summary(text, summary):
                    logger.info("✅ Resumen abstractivo válido")
                    return summary
                else:
                    logger.warning("⚠️ Resumen abstractivo de baja calidad, usando extractivo")
            except Exception as e:
                logger.warning(f"Error en resumen abstractivo: {e}, usando extractivo")

        # Usar resumen extractivo
        logger.info("Usando resumen extractivo")

        # Filtrar parámetros para extractivo
        extractive_params = {
            k: v for k, v in kwargs.items()
            if k in ['num_sentences', 'compression_ratio', 'preserve_order']
        }

        return self.extractive.summarize(text, **extractive_params)

    def _is_good_summary(self, original: str, summary: str) -> bool:
        """
        Valida la calidad del resumen

        Args:
            original: Texto original
            summary: Resumen generado

        Returns:
            True si el resumen es válido
        """
        original_words = len(original.split())
        summary_words = len(summary.split())

        # Verificar longitud mínima absoluta (al menos 50 palabras para textos largos)
        min_words = max(50, int(original_words * 0.15))  # Al menos 15% del original
        if summary_words < min_words:
            logger.warning(f"Resumen muy corto: {summary_words} palabras (mínimo: {min_words})")
            return False

        # Verificar que no sea demasiado similar al original
        if summary.strip().lower() == original.strip().lower()[:len(summary)]:
            logger.warning("Resumen idéntico al inicio del original")
            return False

        # Verificar que no tenga tokens especiales o caracteres raros
        if '<extra_id' in summary or '▁' in summary:
            logger.warning("Resumen contiene tokens especiales")
            return False

        # Verificar compresión razonable (entre 10% y 50%)
        compression = summary_words / original_words
        if compression > 0.5:  # Muy poca compresión
            logger.warning(f"Compresión muy baja: {compression*100:.1f}%")
            return False
        if compression < 0.05:  # Demasiado corto
            logger.warning(f"Compresión muy alta: {compression*100:.1f}%")
            return False

        # Verificar que no repita la misma frase/patrón
        first_sentence = summary.split('.')[0].lower()
        if first_sentence.count('mi mamá') > 1:  # Detectar repeticiones obvias
            logger.warning("Resumen contiene repeticiones obvias")
            return False

        logger.info(f"Resumen válido: {summary_words} palabras ({compression*100:.1f}% compresión)")
        return True


def main():
    """Ejemplo de uso"""
    texto = """
    Las redes sociales han transformado completamente la forma en que conocemos a otras personas.
    Hoy en día podemos conocer detalles de la personalidad, gustos y vida de alguien en segundos.
    Esta nueva forma de conocer personas traspasa las pantallas y afecta nuestros encuentros diarios.
    Mi generación es más tolerante y multicultural gracias a esta exposición constante.
    Las redes nos ayudan a cuestionar nuestra visión del mundo y ser más abiertos.
    Ya no buscamos etiquetas para encasillar a las personas que conocemos.
    En cambio, buscamos conocer los detalles que hacen única a cada persona.
    """

    summarizer = ExtractiveSummarizer()
    resumen = summarizer.summarize(texto, num_sentences=3)

    print("Texto original:")
    print(texto)
    print("\nResumen extractivo:")
    print(resumen)


if __name__ == "__main__":
    main()
