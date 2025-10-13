"""
Inference Module
Usa el modelo entrenado para generar resúmenes de nuevas transcripciones
"""
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import List, Dict, Optional
import json
from pathlib import Path


class VideoSummarizer:
    """Clase para generar resúmenes de videos usando el modelo entrenado"""
    
    def __init__(self, model_path: str = "models/mt5-video-summarizer"):
        """
        Inicializa el resumidor
        
        Args:
            model_path: Ruta del modelo entrenado
        """
        print(f"Cargando modelo desde {model_path}...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Modelo cargado en {self.device}")
        
    def summarize(self,
                 text: str,
                 max_length: int = 128,
                 min_length: int = 30,
                 num_beams: int = 4,
                 length_penalty: float = 2.0,
                 early_stopping: bool = True) -> str:
        """
        Genera un resumen del texto
        
        Args:
            text: Texto a resumir
            max_length: Longitud máxima del resumen
            min_length: Longitud mínima del resumen
            num_beams: Número de beams para beam search
            length_penalty: Penalización por longitud
            early_stopping: Detener early si se completa
            
        Returns:
            Texto del resumen generado
        """
        # Agregar prefix para T5/mT5
        input_text = "resumir: " + text
        
        # Tokenizar
        inputs = self.tokenizer(
            input_text,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generar resumen
        with torch.no_grad():
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                num_beams=num_beams,
                length_penalty=length_penalty,
                early_stopping=early_stopping
            )
        
        # Decodificar
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return summary
    
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
