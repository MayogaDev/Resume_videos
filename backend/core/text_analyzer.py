"""
Text Analysis Module
Proporciona análisis adicional de textos: títulos, palabras clave, bullet points
"""
import re
from typing import List, Dict, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """Analiza textos para extraer metadatos y generar formatos alternativos"""

    def __init__(self):
        """Inicializa el analizador de texto"""
        # Stop words expandido con verbos comunes y palabras irrelevantes
        self.stop_words = set([
            # Artículos
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'del', 'al', 'las', 'los',
            # Pronombres
            'se', 'le', 'lo', 'me', 'te', 'nos', 'les', 'mi', 'tu', 'su', 'yo', 'él', 'ella',
            # Verbos comunes (ser, estar, haber, hacer, decir, etc.)
            'ser', 'es', 'son', 'era', 'fue', 'sido', 'estar', 'está', 'están', 'estaba',
            'haber', 'ha', 'han', 'había', 'hacer', 'hace', 'hacen', 'hecho',
            'decir', 'dice', 'dicen', 'dijo', 'dicho', 'poder', 'puede', 'pueden', 'pudo',
            'tener', 'tiene', 'tienen', 'tenía', 'ir', 'va', 'van', 'iba', 'fue',
            'ver', 've', 'ven', 'vio', 'visto', 'dar', 'da', 'dan', 'dio', 'dado',
            'saber', 'sabe', 'saben', 'sabía', 'querer', 'quiere', 'quieren', 'quería',
            'llegar', 'llega', 'llegan', 'llegó', 'pasar', 'pasa', 'pasan', 'pasó',
            'quedar', 'queda', 'quedan', 'quedó', 'creer', 'cree', 'creen', 'creía',
            'hablar', 'habla', 'hablan', 'habló', 'llevar', 'lleva', 'llevan', 'llevó',
            'dejar', 'deja', 'dejan', 'dejó', 'seguir', 'sigue', 'siguen', 'siguió',
            'encontrar', 'encuentra', 'encuentran', 'encontró', 'parecer', 'parece', 'parecen',
            # Preposiciones y conjunciones
            'por', 'con', 'para', 'como', 'pero', 'o', 'si', 'porque', 'cuando', 'donde',
            'entre', 'desde', 'hasta', 'sobre', 'sin', 'tras', 'durante', 'mediante',
            # Adverbios comunes
            'más', 'muy', 'ya', 'también', 'así', 'ahora', 'después', 'siempre', 'tan',
            'bien', 'poco', 'mucho', 'menos', 'aquí', 'allí', 'ahí',
            # Determinantes
            'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
            'otro', 'otra', 'otros', 'otras', 'alguno', 'alguna', 'algunos',
            'todo', 'toda', 'todos', 'todas', 'cada', 'mismo', 'misma',
            'primero', 'primera', 'segundo', 'nueva', 'nuevo',
            # Otros
            'no', 'ni', 'qué', 'algo', 'nada', 'solo', 'quien', 'cual',
            'vez', 'veces', 'año', 'años', 'día', 'días', 'tiempo', 'parte',
            'cosa', 'cosas', 'mundo', 'vida', 'hombre', 'mujer', 'persona',
            # Palabras de transcripción que no son relevantes
            'había', 'habían', 'hay', 'hubo'
        ])

    def generate_title(self, text: str, max_length: int = 80) -> str:
        """
        Genera un título automático para el texto

        Args:
            text: Texto a analizar
            max_length: Longitud máxima del título

        Returns:
            Título generado
        """
        try:
            # Limpiar texto
            text = text.strip()

            # Opción 1: Tomar la primera frase significativa
            sentences = re.split(r'[.!?]+', text)
            first_sentences = [s.strip() for s in sentences[:5] if len(s.strip()) > 20]

            if first_sentences:
                # Buscar una frase que parezca un título/tema
                for sentence in first_sentences:
                    # Evitar frases con preguntas directas al principio
                    if not sentence.lower().startswith(('a unos', 'entonces', 'y ', 'pero ')):
                        title = sentence[:max_length]
                        # Capitalizar primera letra
                        if title:
                            title = title[0].upper() + title[1:]
                            # Añadir puntos suspensivos si se cortó
                            if len(sentence) > max_length:
                                title = title.rstrip() + '...'
                            return title

            # Fallback: usar palabras clave principales
            keywords = self.extract_keywords(text, top_n=5)
            if keywords:
                title = ' - '.join([k[0].capitalize() for k in keywords[:3]])
                return title[:max_length]

            # Último fallback
            return "Video sin título"

        except Exception as e:
            logger.error(f"Error generando título: {e}")
            return "Video sin título"

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extrae las palabras clave más importantes

        Args:
            text: Texto a analizar
            top_n: Número de palabras clave a extraer

        Returns:
            Lista de tuplas (palabra, frecuencia)
        """
        try:
            # Extraer palabras
            words = re.findall(r'\b\w+\b', text.lower())

            # Filtrar stop words y palabras muy cortas
            meaningful_words = [
                w for w in words
                if w not in self.stop_words and len(w) > 3
            ]

            # Contar frecuencias
            word_freq = Counter(meaningful_words)

            # Retornar top N
            return word_freq.most_common(top_n)

        except Exception as e:
            logger.error(f"Error extrayendo palabras clave: {e}")
            return []

    def generate_bullet_points(self, text: str, max_points: int = 8) -> List[str]:
        """
        Genera resumen en formato de bullet points

        Args:
            text: Texto a resumir
            max_points: Número máximo de puntos

        Returns:
            Lista de puntos principales
        """
        try:
            # Dividir en frases
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

            if len(sentences) <= max_points:
                return sentences

            # Calcular puntuación por frase (similar a extractivo)
            keywords = self.extract_keywords(text, top_n=20)
            keyword_set = set([k[0] for k in keywords])

            sentence_scores = []
            for sentence in sentences:
                words = re.findall(r'\b\w+\b', sentence.lower())
                score = sum(1 for w in words if w in keyword_set)
                sentence_scores.append((sentence, score))

            # Ordenar por puntuación y tomar top N
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = sentence_scores[:max_points]

            # Mantener orden original
            original_order = {sent: i for i, (sent, _) in enumerate(sentence_scores)}
            top_sentences.sort(key=lambda x: sentences.index(x[0]))

            return [sent for sent, _ in top_sentences]

        except Exception as e:
            logger.error(f"Error generando bullet points: {e}")
            return []

    def analyze_text(self, text: str) -> Dict:
        """
        Análisis completo del texto

        Args:
            text: Texto a analizar

        Returns:
            Diccionario con todos los análisis
        """
        return {
            'title': self.generate_title(text),
            'keywords': self.extract_keywords(text, top_n=10),
            'bullet_points': self.generate_bullet_points(text),
            'stats': {
                'words': len(text.split()),
                'characters': len(text),
                'sentences': len(re.split(r'[.!?]+', text)),
                'avg_word_length': sum(len(w) for w in text.split()) / len(text.split()) if text.split() else 0,
                'unique_words': len(set(text.lower().split()))
            }
        }

    def format_markdown(self, video_name: str, transcripcion: str, resumen: str,
                       analysis: Dict, stats: Dict) -> str:
        """
        Formatea todo en un documento Markdown bonito

        Args:
            video_name: Nombre del video
            transcripcion: Texto de la transcripción
            resumen: Texto del resumen
            analysis: Resultado del análisis de texto
            stats: Estadísticas del procesamiento

        Returns:
            Documento Markdown formateado
        """
        md = f"""# 🎬 {analysis['title']}

**Video:** {video_name}
**Fecha:** {stats.get('timestamp', 'N/A')}

---

## 📊 Resumen Ejecutivo

{resumen}

---

## 🔑 Puntos Clave

"""
        # Añadir bullet points
        for i, point in enumerate(analysis['bullet_points'], 1):
            md += f"{i}. {point}\n"

        md += f"""

---

## 🏷️ Palabras Clave

"""
        # Añadir keywords
        keywords_text = ', '.join([f"**{word}** ({count})" for word, count in analysis['keywords'][:10]])
        md += keywords_text + "\n"

        md += f"""

---

## 📈 Estadísticas

### Transcripción Original
- **Palabras:** {stats['transcripcion']['palabras']:,}
- **Caracteres:** {stats['transcripcion']['caracteres']:,}
- **Líneas:** {stats['transcripcion']['lineas']:,}

### Resumen Generado
- **Palabras:** {stats['resumen']['palabras']:,}
- **Caracteres:** {stats['resumen']['caracteres']:,}
- **Compresión:** {(1 - stats['compresion']['ratio_palabras'])*100:.1f}% reducción

---

## 📝 Transcripción Completa

{transcripcion}

---

*Generado automáticamente por Sistema de Resumen de Videos*
"""
        return md


def main():
    """Ejemplo de uso"""
    analyzer = TextAnalyzer()

    texto = """
    Las redes sociales han transformado la forma en que conocemos a otras personas.
    En solo 30 segundos podemos saber mucho sobre alguien.
    Esta nueva forma de conocer personas traspasa las pantallas.
    Mi generación es más tolerante gracias a las redes sociales.
    Ya no buscamos etiquetas para las personas.
    """

    print("=" * 70)
    print("ANÁLISIS DE TEXTO")
    print("=" * 70)

    analysis = analyzer.analyze_text(texto)

    print(f"\n📌 TÍTULO: {analysis['title']}")

    print(f"\n🔑 PALABRAS CLAVE:")
    for word, count in analysis['keywords'][:5]:
        print(f"   - {word}: {count}")

    print(f"\n📋 PUNTOS PRINCIPALES:")
    for i, point in enumerate(analysis['bullet_points'][:3], 1):
        print(f"   {i}. {point}")


if __name__ == "__main__":
    main()
