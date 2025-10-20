"""
Video Summarization Module
Genera resúmenes de transcripciones usando mT5 (multilingual T5)

Características:
- Soporte para modelos pre-entrenados y fine-tuned
- Configuración flexible de parámetros
- Manejo de textos largos con chunking
- Logging detallado
"""
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import List, Dict, Optional
import json
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoSummarizer:
    """Genera resúmenes de transcripciones usando mT5"""

    def __init__(
        self,
        model_path: str = "google/mt5-small",
        device: Optional[str] = None,
        max_input_length: int = 512,
        cache_dir: Optional[str] = None
    ):
        """
        Inicializa el resumidor con mT5

        Args:
            model_path: Modelo HuggingFace o ruta local
                       - "google/mt5-small" (300M params, rápido)
                       - "google/mt5-base" (580M params, equilibrado)
                       - "models/mt5-fine-tuned" (modelo entrenado local)
            device: 'cuda', 'cpu', 'cuda:0', etc. Auto-detect si None
            max_input_length: Longitud máxima del input en tokens
            cache_dir: Directorio para cachear modelos
        """
        self.model_path = model_path
        self.model_name = model_path  # Para identificación en DB
        self.max_input_length = max_input_length

        # Auto-detectar device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        logger.info(f"Inicializando VideoSummarizer con {model_path}")
        logger.info(f"Device: {self.device}")

        try:
            # Cargar tokenizer y modelo
            logger.info("Cargando tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                cache_dir=cache_dir,
                use_fast=False  # Usar tokenizer lento para evitar problemas con SentencePiece
            )

            logger.info("Cargando modelo...")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_path,
                cache_dir=cache_dir
            )

            # Mover a device
            self.model = self.model.to(self.device)
            self.model.eval()  # Modo evaluación

            logger.info("✅ Modelo cargado exitosamente")

        except Exception as e:
            logger.error(f"Error al cargar modelo: {e}")
            raise
        
    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        num_beams: int = 4,
        temperature: float = 1.0,
        top_p: float = 0.9,
        repetition_penalty: float = 2.0,
        length_penalty: float = 1.0,
        no_repeat_ngram_size: int = 3,
        early_stopping: bool = True,
        prefix: str = "summarize: "
    ) -> str:
        """
        Genera un resumen del texto

        Args:
            text: Texto a resumir
            max_length: Longitud máxima del resumen en tokens
            min_length: Longitud mínima del resumen en tokens
            num_beams: Número de beams (1-8). Más = mejor calidad
            temperature: Temperatura (0.7-1.3). 1.0 = neutral
            top_p: Nucleus sampling (0.8-0.95)
            repetition_penalty: Penalización repetición (1.0-3.0)
            length_penalty: Penalización longitud (0.5-2.0)
            no_repeat_ngram_size: No repetir n-gramas
            early_stopping: Detener cuando todos los beams terminan
            prefix: Prefijo para tarea ("resume: " o "resumir: ")

        Returns:
            Texto del resumen generado
        """
        if not text or len(text.strip()) < 50:
            logger.warning("Texto muy corto para resumir")
            return text

        try:
            # Preparar input con prefix
            input_text = f"{prefix}{text}"

            # Tokenizar
            inputs = self.tokenizer(
                input_text,
                max_length=self.max_input_length,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)

            # Generar resumen
            logger.info("Generando resumen...")
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty,
                    length_penalty=length_penalty,
                    no_repeat_ngram_size=no_repeat_ngram_size,
                    early_stopping=early_stopping,
                    do_sample=temperature != 1.0
                )

            # Decodificar
            summary = self.tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )

            logger.info(f"✅ Resumen generado: {len(summary.split())} palabras")
            return summary.strip()

        except Exception as e:
            logger.error(f"Error al generar resumen: {e}")
            raise

    def generate_summary(self, text: str, **kwargs) -> str:
        """Alias de summarize() para compatibilidad"""
        return self.summarize(text, **kwargs)
    
    def summarize_batch(self, texts: List[str], **kwargs) -> List[str]:
        """
        Genera resúmenes para múltiples textos
        
        Args:
            texts: Lista de textos a resumir
            **kwargs: Argumentos para el método summarize
            
        Returns:
            Lista de resúmenes
        """
        summaries = []
        for text in texts:
            summary = self.summarize(text, **kwargs)
            summaries.append(summary)
        
        return summaries
    
    def summarize_transcript(self, 
                           transcript_path: str,
                           save_summary: bool = True) -> Dict:
        """
        Resume una transcripción desde un archivo JSON
        
        Args:
            transcript_path: Ruta del archivo de transcripción
            save_summary: Si guardar el resumen en un archivo
            
        Returns:
            Diccionario con transcripción y resumen
        """
        # Cargar transcripción
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        # Obtener texto
        text = transcript.get('text', '')
        
        # Generar resumen
        summary = self.summarize(text)
        
        result = {
            'filename': Path(transcript_path).stem,
            'original_text': text,
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary),
            'compression_ratio': len(summary) / len(text) if len(text) > 0 else 0
        }
        
        # Guardar resumen
        if save_summary:
            summary_path = transcript_path.replace('_transcript.json', '_summary.json')
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Resumen guardado en {summary_path}")
        
        return result
    
    def batch_summarize_transcripts(self, 
                                   transcript_dir: str,
                                   output_dir: Optional[str] = None):
        """
        Resume múltiples transcripciones de un directorio
        
        Args:
            transcript_dir: Directorio con transcripciones
            output_dir: Directorio de salida para resúmenes
        """
        if output_dir is None:
            output_dir = transcript_dir
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Buscar transcripciones
        transcripts = list(Path(transcript_dir).glob('*_transcript.json'))
        
        print(f"Encontradas {len(transcripts)} transcripciones para resumir")
        
        results = []
        for transcript_path in transcripts:
            try:
                result = self.summarize_transcript(str(transcript_path), save_summary=True)
                results.append(result)
                
                print(f"\n{result['filename']}:")
                print(f"  Texto original: {result['original_length']} caracteres")
                print(f"  Resumen: {result['summary_length']} caracteres")
                print(f"  Compresión: {result['compression_ratio']:.2%}")
                print(f"  Resumen: {result['summary'][:100]}...")
                
            except Exception as e:
                print(f"Error procesando {transcript_path}: {e}")
        
        # Guardar resumen consolidado
        summary_file = Path(output_dir) / "all_summaries.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\nResumen consolidado guardado en {summary_file}")
        
        return results


def main():
    """Ejemplo de uso"""
    # Inicializar resumidor
    summarizer = VideoSummarizer(model_path="models/mt5-video-summarizer")
    
    # Opción 1: Resumir un texto directo
    texto_ejemplo = """
    En este video explicaremos el concepto de redes neuronales artificiales.
    Las redes neuronales son modelos computacionales inspirados en el cerebro humano.
    Están compuestas por capas de neuronas artificiales que procesan información.
    Cada neurona recibe entradas, las procesa y genera una salida.
    Las redes neuronales se entrenan con datos para aprender patrones.
    Se utilizan en muchas aplicaciones como reconocimiento de imágenes y procesamiento de lenguaje natural.
    """
    
    resumen = summarizer.summarize(texto_ejemplo)
    print("Texto original:")
    print(texto_ejemplo)
    print("\nResumen generado:")
    print(resumen)
    
    # Opción 2: Resumir transcripciones de un directorio
    # summarizer.batch_summarize_transcripts("videos/transcripts")
    
    # Opción 3: Resumir una transcripción específica
    # result = summarizer.summarize_transcript("videos/mi_video_transcript.json")
    # print(f"Resumen: {result['summary']}")


if __name__ == "__main__":
    main()
