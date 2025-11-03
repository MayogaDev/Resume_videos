"""
Video Transcription Module
Extrae audio de videos y los transcribe usando Whisper

Mejoras:
- Validación de archivos de entrada
- Manejo robusto de errores
- Soporte para videos largos con chunks
- Limpieza automática de archivos temporales
- Logging detallado
"""
import os
import whisper
from pathlib import Path
import json
from typing import Optional, Dict, Union
from tqdm import tqdm
import logging

# Configurar directorio de caché de modelos Whisper
PROJECT_ROOT = Path(__file__).parent.parent.parent
WHISPER_CACHE_DIR = PROJECT_ROOT / "models" / "whisper"
WHISPER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["WHISPER_CACHE_DIR"] = str(WHISPER_CACHE_DIR)

# Compatibilidad con MoviePy 1.x y 2.x
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    try:
        from moviepy import VideoFileClip
    except ImportError:
        raise ImportError(
            "MoviePy no está instalado. Por favor ejecuta: pip install moviepy"
        )


class VideoTranscriber:
    """Clase para transcribir videos usando Whisper"""

    # Configuración de formatos soportados
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
    SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']
    WHISPER_MODELS = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']

    def __init__(self, model_size: str = "base", language: str = "es", verbose: bool = True):
        """
        Inicializa el transcriptor

        Args:
            model_size: Tamaño del modelo Whisper (tiny, base, small, medium, large)
            language: Idioma del video (es, en, etc.)
            verbose: Si mostrar mensajes detallados
        """
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Validar modelo
        if model_size not in self.WHISPER_MODELS:
            raise ValueError(
                f"Modelo '{model_size}' no soportado. "
                f"Opciones válidas: {', '.join(self.WHISPER_MODELS)}"
            )

        self.logger.info(f"Cargando modelo Whisper ({model_size})...")
        self.logger.info(f"Directorio de caché: {WHISPER_CACHE_DIR}")
        try:
            self.model = whisper.load_model(
                model_size,
                download_root=str(WHISPER_CACHE_DIR)
            )
            self.logger.info("Modelo cargado exitosamente desde caché local")
        except Exception as e:
            self.logger.error(f"Error al cargar modelo Whisper: {e}")
            raise

        self.language = language
        self.model_size = model_size
        self.verbose = verbose

    def _validate_video_file(self, video_path: str) -> None:
        """
        Valida que el archivo de video existe y tiene formato soportado

        Args:
            video_path: Ruta del video

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado
        """
        path = Path(video_path)

        if not path.exists():
            raise FileNotFoundError(f"El archivo no existe: {video_path}")

        if not path.is_file():
            raise ValueError(f"La ruta no es un archivo: {video_path}")

        if path.suffix.lower() not in self.SUPPORTED_VIDEO_FORMATS:
            raise ValueError(
                f"Formato de video no soportado: {path.suffix}\n"
                f"Formatos soportados: {', '.join(self.SUPPORTED_VIDEO_FORMATS)}"
            )

        # Verificar tamaño del archivo
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb == 0:
            raise ValueError(f"El archivo está vacío: {video_path}")

        self.logger.info(f"Video validado: {path.name} ({file_size_mb:.2f} MB)")
        
    def extract_audio(self, video_path: str, audio_path: Optional[str] = None) -> str:
        """
        Extrae el audio de un video

        Args:
            video_path: Ruta del video
            audio_path: Ruta donde guardar el audio (opcional)

        Returns:
            Ruta del archivo de audio extraído

        Raises:
            FileNotFoundError: Si el video no existe
            ValueError: Si el video no tiene audio o formato no soportado
            RuntimeError: Si hay error durante la extracción
        """
        # Validar archivo
        self._validate_video_file(video_path)

        # Generar ruta de audio si no se proporciona
        if audio_path is None:
            path = Path(video_path)
            audio_path = str(path.parent / f"{path.stem}.mp3")

        self.logger.info(f"Extrayendo audio de: {Path(video_path).name}")

        try:
            video = VideoFileClip(video_path)

            # Verificar que el video tenga audio
            if video.audio is None:
                video.close()
                raise ValueError(f"El video no tiene pista de audio: {video_path}")

            # Extraer audio (compatible con MoviePy 1.x y 2.x)
            try:
                # MoviePy 2.x - sin verbose ni logger
                video.audio.write_audiofile(
                    audio_path,
                    codec='libmp3lame',
                    bitrate='192k',
                    logger=None
                )
            except TypeError:
                # MoviePy 1.x - con verbose y logger
                video.audio.write_audiofile(
                    audio_path,
                    verbose=False,
                    logger=None,
                    codec='libmp3lame',
                    bitrate='192k'
                )
            video.close()

            # Verificar que el audio se creó correctamente
            if not os.path.exists(audio_path):
                raise RuntimeError(f"No se pudo crear el archivo de audio: {audio_path}")

            audio_size_mb = Path(audio_path).stat().st_size / (1024 * 1024)
            self.logger.info(f"Audio extraído exitosamente: {Path(audio_path).name} ({audio_size_mb:.2f} MB)")

            return audio_path

        except Exception as e:
            self.logger.error(f"Error al extraer audio: {e}")
            # Limpiar archivo de audio si se creó parcialmente
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass
            raise RuntimeError(f"Error al extraer audio de {video_path}: {e}")
    
    def transcribe_audio(self, audio_path: str, **kwargs) -> Dict:
        """
        Transcribe un archivo de audio

        Args:
            audio_path: Ruta del archivo de audio
            **kwargs: Argumentos adicionales para whisper.transcribe()
                - temperature: float o lista de floats para muestreo
                - compression_ratio_threshold: umbral para detectar fallas
                - logprob_threshold: umbral de probabilidad logarítmica
                - no_speech_threshold: umbral para detectar silencio

        Returns:
            Diccionario con la transcripción y metadatos

        Raises:
            FileNotFoundError: Si el archivo de audio no existe
            RuntimeError: Si hay error durante la transcripción
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

        self.logger.info(f"Transcribiendo audio: {Path(audio_path).name}")
        self.logger.info(f"Idioma configurado: {self.language}")

        try:
            # Configuración por defecto para mejor calidad
            transcribe_options = {
                'language': self.language,
                'verbose': self.verbose,
                'temperature': 0.0,  # Más determinístico
                'compression_ratio_threshold': 2.4,
                'logprob_threshold': -1.0,
                'no_speech_threshold': 0.6,
            }

            # Sobrescribir con kwargs si se proporcionan
            transcribe_options.update(kwargs)

            result = self.model.transcribe(audio_path, **transcribe_options)

            # Validar resultado
            if not result or 'text' not in result:
                raise RuntimeError("La transcripción no devolvió texto")

            text = result['text'].strip()
            if not text:
                self.logger.warning("La transcripción resultó en texto vacío")
            else:
                word_count = len(text.split())
                self.logger.info(f"Transcripción completada: {word_count} palabras")

            return result

        except Exception as e:
            self.logger.error(f"Error durante la transcripción: {e}")
            raise RuntimeError(f"Error al transcribir {audio_path}: {e}")
    
    def transcribe_video(
        self,
        video_path: str,
        save_transcript: bool = True,
        output_dir: Optional[str] = None,
        cleanup_audio: bool = True
    ) -> Dict:
        """
        Pipeline completo: extrae audio y transcribe

        Args:
            video_path: Ruta del video
            save_transcript: Si guardar la transcripción en JSON
            output_dir: Directorio de salida (opcional, por defecto junto al video)
            cleanup_audio: Si eliminar el archivo de audio temporal después

        Returns:
            Diccionario con la transcripción y metadatos

        Raises:
            FileNotFoundError: Si el video no existe
            RuntimeError: Si hay error durante el proceso
        """
        video_path = str(Path(video_path).resolve())  # Convertir a ruta absoluta
        self.logger.info(f"=== Iniciando transcripción de video ===")
        self.logger.info(f"Video: {Path(video_path).name}")

        audio_path = None
        try:
            # Extraer audio
            self.logger.info("[1/2] Extrayendo audio...")
            audio_path = self.extract_audio(video_path)

            # Transcribir
            self.logger.info("[2/2] Transcribiendo audio...")
            transcript = self.transcribe_audio(audio_path)

            # Agregar metadatos adicionales
            transcript['video_path'] = video_path
            transcript['video_name'] = Path(video_path).name
            transcript['model_size'] = self.model_size
            transcript['language'] = self.language

            # Calcular estadísticas
            text = transcript.get('text', '')
            transcript['stats'] = {
                'total_characters': len(text),
                'total_words': len(text.split()),
                'total_segments': len(transcript.get('segments', []))
            }

            # Guardar transcripción
            if save_transcript:
                if output_dir is None:
                    output_dir = Path(video_path).parent
                else:
                    output_dir = Path(output_dir)
                    output_dir.mkdir(parents=True, exist_ok=True)

                json_filename = Path(video_path).stem + '_transcript.json'
                json_path = output_dir / json_filename

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(transcript, f, ensure_ascii=False, indent=2)

                self.logger.info(f"Transcripción guardada en: {json_path}")

            self.logger.info("=== Transcripción completada exitosamente ===")
            return transcript

        except Exception as e:
            self.logger.error(f"Error durante la transcripción del video: {e}")
            raise

        finally:
            # Limpiar archivo de audio temporal
            if cleanup_audio and audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                    self.logger.info(f"Audio temporal eliminado: {Path(audio_path).name}")
                except Exception as e:
                    self.logger.warning(f"No se pudo eliminar audio temporal: {e}")
    
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
