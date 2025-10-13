"""
Video Transcription Module
Extrae audio de videos y los transcribe usando Whisper
"""
import os
import whisper
from moviepy.editor import VideoFileClip
from pathlib import Path
import json
from typing import Optional, Dict
from tqdm import tqdm


class VideoTranscriber:
    """Clase para transcribir videos usando Whisper"""
    
    def __init__(self, model_size: str = "base", language: str = "es"):
        """
        Inicializa el transcriptor
        
        Args:
            model_size: Tamaño del modelo Whisper (tiny, base, small, medium, large)
            language: Idioma del video (es, en, etc.)
        """
        print(f"Cargando modelo Whisper ({model_size})...")
        self.model = whisper.load_model(model_size)
        self.language = language
        
    def extract_audio(self, video_path: str, audio_path: Optional[str] = None) -> str:
        """
        Extrae el audio de un video
        
        Args:
            video_path: Ruta del video
            audio_path: Ruta donde guardar el audio (opcional)
            
        Returns:
            Ruta del archivo de audio extraído
        """
        if audio_path is None:
            audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
            
        print(f"Extrayendo audio de {video_path}...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        
        return audio_path
    
    def transcribe_audio(self, audio_path: str) -> Dict:
        """
        Transcribe un archivo de audio
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            Diccionario con la transcripción y metadatos
        """
        print(f"Transcribiendo {audio_path}...")
        result = self.model.transcribe(
            audio_path,
            language=self.language,
            verbose=False
        )
        
        return result
    
    def transcribe_video(self, video_path: str, save_transcript: bool = True) -> Dict:
        """
        Pipeline completo: extrae audio y transcribe
        
        Args:
            video_path: Ruta del video
            save_transcript: Si guardar la transcripción en JSON
            
        Returns:
            Diccionario con la transcripción
        """
        # Extraer audio
        audio_path = self.extract_audio(video_path)
        
        # Transcribir
        transcript = self.transcribe_audio(audio_path)
        
        # Guardar transcripción
        if save_transcript:
            json_path = video_path.rsplit('.', 1)[0] + '_transcript.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(transcript, f, ensure_ascii=False, indent=2)
            print(f"Transcripción guardada en {json_path}")
        
        # Limpiar archivo de audio temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return transcript
    
    def batch_transcribe(self, video_dir: str, output_dir: Optional[str] = None):
        """
        Transcribe múltiples videos de un directorio
        
        Args:
            video_dir: Directorio con los videos
            output_dir: Directorio de salida para transcripciones
        """
        if output_dir is None:
            output_dir = os.path.join(video_dir, 'transcripts')
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Buscar videos
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        videos = []
        for ext in video_extensions:
            videos.extend(Path(video_dir).glob(f'*{ext}'))
        
        print(f"Encontrados {len(videos)} videos para transcribir")
        
        for video_path in tqdm(videos, desc="Transcribiendo videos"):
            try:
                transcript = self.transcribe_video(str(video_path), save_transcript=False)
                
                # Guardar en output_dir
                json_filename = video_path.stem + '_transcript.json'
                json_path = os.path.join(output_dir, json_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(transcript, f, ensure_ascii=False, indent=2)
                    
            except Exception as e:
                print(f"Error procesando {video_path}: {e}")


def main():
    """Ejemplo de uso"""
    # Crear transcriptor
    transcriber = VideoTranscriber(model_size="base", language="es")
    
    # Transcribir un video individual
    # video_path = "videos/mi_video.mp4"
    # transcript = transcriber.transcribe_video(video_path)
    # print(f"Texto transcrito: {transcript['text']}")
    
    # Transcribir múltiples videos
    video_directory = "videos"
    transcriber.batch_transcribe(video_directory)


if __name__ == "__main__":
    main()
