"""
Video Processing Service
Servicio principal para procesamiento de videos
"""
import time
from pathlib import Path
from typing import Dict, Optional
import logging

from backend.core.transcription import VideoTranscriber
from backend.database.connection import DatabaseManager
from backend.database.models import Video, Transcription, Summary

logger = logging.getLogger(__name__)


class VideoProcessorService:
    """Servicio de procesamiento de videos (transcripción + resumen)"""

    def __init__(
        self,
        db_path: str = "database/resume_videos.db",
        whisper_model: str = "base",
        summarizer_model: Optional[str] = None
    ):
        """
        Inicializa el servicio de procesamiento

        Args:
            db_path: Ruta a la base de datos
            whisper_model: Modelo de Whisper a usar
            summarizer_model: Ruta al modelo de resumen (opcional)
        """
        self.db = DatabaseManager(db_path)
        self.transcriber = VideoTranscriber(model_size=whisper_model, language="es")
        self.summarizer = None  # Se cargará cuando se necesite

        # Lazy loading del modelo de resumen
        if summarizer_model:
            self._load_summarizer(summarizer_model)

        logger.info("Servicio de procesamiento inicializado")

    def _load_summarizer(self, model_path: str):
        """Carga el modelo de resumen (lazy loading)"""
        try:
            # Importar dinámicamente para evitar dependencias
            from backend.core.summarization import VideoSummarizer
            self.summarizer = VideoSummarizer(model_path)
            logger.info(f"Modelo de resumen cargado: {model_path}")
        except Exception as e:
            logger.error(f"Error al cargar modelo de resumen: {e}")
            raise

    def process_video(
        self,
        video_path: str,
        create_summary: bool = True,
        save_outputs: bool = True
    ) -> Dict:
        """
        Procesa un video completo: transcripción + resumen

        Args:
            video_path: Ruta al video
            create_summary: Si crear resumen (requiere modelo cargado)
            save_outputs: Si guardar en base de datos

        Returns:
            Diccionario con resultados del procesamiento
        """
        start_time = time.time()
        video_path = str(Path(video_path).resolve())

        logger.info(f"Procesando video: {Path(video_path).name}")

        try:
            # 1. Registrar video en DB
            video_file = Path(video_path)
            video = None

            if save_outputs:
                # Verificar si ya existe
                existing_video = Video.get_by_filepath(self.db, video_path)
                if existing_video:
                    video = existing_video
                    logger.info(f"Video ya existe en DB: ID {video.id}")
                else:
                    video = Video.create(
                        self.db,
                        filename=video_file.name,
                        filepath=video_path,
                        file_size=video_file.stat().st_size
                    )
                    logger.info(f"Video registrado en DB: ID {video.id}")

            # 2. Transcribir video
            logger.info("Iniciando transcripción...")
            transcription_start = time.time()

            transcript_result = self.transcriber.transcribe_video(
                video_path,
                save_transcript=False,  # No guardar JSON, usamos DB
                cleanup_audio=True
            )

            transcription_time = time.time() - transcription_start

            # 3. Guardar transcripción en DB
            transcription = None
            if save_outputs and video:
                transcription = Transcription.create(
                    self.db,
                    video_id=video.id,
                    text=transcript_result['text'],
                    language=transcript_result['language'],
                    model_used=transcript_result['model_size'],
                    word_count=transcript_result['stats']['total_words'],
                    char_count=transcript_result['stats']['total_characters'],
                    segments_count=transcript_result['stats']['total_segments'],
                    processing_time=transcription_time
                )
                logger.info(f"Transcripción guardada en DB: ID {transcription.id}")

            # 4. Generar resumen (opcional)
            summary_result = None
            summary_time = 0

            if create_summary:
                if not self.summarizer:
                    logger.warning("Modelo de resumen no cargado, saltando generación de resumen")
                else:
                    logger.info("Iniciando generación de resumen...")
                    summary_start = time.time()

                    summary_text = self.summarizer.generate_summary(
                        transcript_result['text'],
                        max_length=150
                    )

                    summary_time = time.time() - summary_start

                    # Calcular compression ratio
                    compression_ratio = len(summary_text.split()) / transcript_result['stats']['total_words']

                    summary_result = {
                        'text': summary_text,
                        'compression_ratio': compression_ratio,
                        'processing_time': summary_time
                    }

                    # Guardar en DB
                    if save_outputs and transcription:
                        Summary.create(
                            self.db,
                            transcription_id=transcription.id,
                            summary_text=summary_text,
                            model_used=self.summarizer.model_name if hasattr(self.summarizer, 'model_name') else 'unknown',
                            max_length=150,
                            compression_ratio=compression_ratio,
                            processing_time=summary_time
                        )
                        logger.info("Resumen guardado en DB")

            # 5. Resultado final
            total_time = time.time() - start_time

            result = {
                'success': True,
                'video': {
                    'path': video_path,
                    'filename': video_file.name,
                    'size_mb': round(video_file.stat().st_size / (1024 * 1024), 2)
                },
                'transcription': {
                    'text': transcript_result['text'],
                    'language': transcript_result['language'],
                    'model': transcript_result['model_size'],
                    'stats': transcript_result['stats'],
                    'time': round(transcription_time, 2)
                },
                'summary': summary_result,
                'total_time': round(total_time, 2)
            }

            logger.info(f"Procesamiento completado en {total_time:.2f}s")
            return result

        except Exception as e:
            logger.error(f"Error durante el procesamiento: {e}")
            return {
                'success': False,
                'error': str(e),
                'video_path': video_path
            }

    def get_video_history(self, video_path: str) -> Optional[Dict]:
        """
        Obtiene el historial de procesamiento de un video

        Args:
            video_path: Ruta al video

        Returns:
            Diccionario con historial o None si no existe
        """
        video = Video.get_by_filepath(self.db, str(Path(video_path).resolve()))
        if not video:
            return None

        transcription = Transcription.get_by_video_id(self.db, video.id)
        summary = Summary.get_by_transcription_id(self.db, transcription.id) if transcription else None

        return {
            'video': video,
            'transcription': transcription,
            'summary': summary
        }

    def get_database_stats(self) -> Dict:
        """Obtiene estadísticas de la base de datos"""
        return self.db.get_stats()
