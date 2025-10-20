"""
Database Models
Modelos de datos para videos, transcripciones y resúmenes
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from .connection import DatabaseManager


@dataclass
class Video:
    """Modelo de datos para videos"""
    filename: str
    filepath: str
    file_size: int
    duration: Optional[float] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, db: DatabaseManager, **kwargs) -> 'Video':
        """Crea un nuevo video en la base de datos"""
        video_id = db.execute_update(
            """INSERT INTO videos (filename, filepath, file_size, duration)
               VALUES (?, ?, ?, ?)""",
            (kwargs['filename'], kwargs['filepath'], kwargs['file_size'], kwargs.get('duration'))
        )
        kwargs['id'] = video_id
        return cls(**kwargs)

    @classmethod
    def get_by_id(cls, db: DatabaseManager, video_id: int) -> Optional['Video']:
        """Obtiene un video por ID"""
        result = db.execute_query("SELECT * FROM videos WHERE id = ?", (video_id,))
        if result:
            return cls(**dict(result[0]))
        return None

    @classmethod
    def get_by_filepath(cls, db: DatabaseManager, filepath: str) -> Optional['Video']:
        """Obtiene un video por ruta de archivo"""
        result = db.execute_query("SELECT * FROM videos WHERE filepath = ?", (filepath,))
        if result:
            return cls(**dict(result[0]))
        return None

    @classmethod
    def get_all(cls, db: DatabaseManager, limit: int = 100) -> list['Video']:
        """Obtiene todos los videos"""
        results = db.execute_query(
            "SELECT * FROM videos ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [cls(**dict(row)) for row in results]


@dataclass
class Transcription:
    """Modelo de datos para transcripciones"""
    video_id: int
    text: str
    language: str
    model_used: str
    word_count: int
    char_count: int
    segments_count: int
    processing_time: float
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def create(cls, db: DatabaseManager, **kwargs) -> 'Transcription':
        """Crea una nueva transcripción en la base de datos"""
        transcription_id = db.execute_update(
            """INSERT INTO transcriptions
               (video_id, text, language, model_used, word_count, char_count, segments_count, processing_time)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                kwargs['video_id'], kwargs['text'], kwargs['language'],
                kwargs['model_used'], kwargs['word_count'], kwargs['char_count'],
                kwargs['segments_count'], kwargs['processing_time']
            )
        )
        kwargs['id'] = transcription_id
        return cls(**kwargs)

    @classmethod
    def get_by_id(cls, db: DatabaseManager, transcription_id: int) -> Optional['Transcription']:
        """Obtiene una transcripción por ID"""
        result = db.execute_query("SELECT * FROM transcriptions WHERE id = ?", (transcription_id,))
        if result:
            return cls(**dict(result[0]))
        return None

    @classmethod
    def get_by_video_id(cls, db: DatabaseManager, video_id: int) -> Optional['Transcription']:
        """Obtiene la transcripción de un video"""
        result = db.execute_query(
            "SELECT * FROM transcriptions WHERE video_id = ? ORDER BY created_at DESC LIMIT 1",
            (video_id,)
        )
        if result:
            return cls(**dict(result[0]))
        return None


@dataclass
class Summary:
    """Modelo de datos para resúmenes"""
    transcription_id: int
    summary_text: str
    model_used: str
    max_length: int
    compression_ratio: float
    processing_time: float
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def create(cls, db: DatabaseManager, **kwargs) -> 'Summary':
        """Crea un nuevo resumen en la base de datos"""
        summary_id = db.execute_update(
            """INSERT INTO summaries
               (transcription_id, summary_text, model_used, max_length, compression_ratio, processing_time)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                kwargs['transcription_id'], kwargs['summary_text'], kwargs['model_used'],
                kwargs['max_length'], kwargs['compression_ratio'], kwargs['processing_time']
            )
        )
        kwargs['id'] = summary_id
        return cls(**kwargs)

    @classmethod
    def get_by_id(cls, db: DatabaseManager, summary_id: int) -> Optional['Summary']:
        """Obtiene un resumen por ID"""
        result = db.execute_query("SELECT * FROM summaries WHERE id = ?", (summary_id,))
        if result:
            return cls(**dict(result[0]))
        return None

    @classmethod
    def get_by_transcription_id(cls, db: DatabaseManager, transcription_id: int) -> Optional['Summary']:
        """Obtiene el resumen de una transcripción"""
        result = db.execute_query(
            "SELECT * FROM summaries WHERE transcription_id = ? ORDER BY created_at DESC LIMIT 1",
            (transcription_id,)
        )
        if result:
            return cls(**dict(result[0]))
        return None
