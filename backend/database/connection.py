"""
Database Connection Manager
Gestión de conexiones a SQLite
"""
import sqlite3
from pathlib import Path
from typing import Optional
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gestor de conexiones a la base de datos"""

    def __init__(self, db_path: str = "database/resume_videos.db"):
        """
        Inicializa el gestor de base de datos

        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"Base de datos inicializada: {self.db_path}")

    def _init_database(self):
        """Inicializa la base de datos y crea las tablas si no existen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabla de videos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT UNIQUE NOT NULL,
                    file_size INTEGER,
                    duration REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabla de transcripciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    language TEXT,
                    model_used TEXT,
                    word_count INTEGER,
                    char_count INTEGER,
                    segments_count INTEGER,
                    processing_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
                )
            """)

            # Tabla de resúmenes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcription_id INTEGER NOT NULL,
                    summary_text TEXT NOT NULL,
                    model_used TEXT,
                    max_length INTEGER,
                    compression_ratio REAL,
                    processing_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcription_id) REFERENCES transcriptions (id) ON DELETE CASCADE
                )
            """)

            # Tabla de procesamiento (historial)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    transcription_id INTEGER,
                    summary_id INTEGER,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    total_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE,
                    FOREIGN KEY (transcription_id) REFERENCES transcriptions (id) ON DELETE SET NULL,
                    FOREIGN KEY (summary_id) REFERENCES summaries (id) ON DELETE SET NULL
                )
            """)

            # Índices para mejorar rendimiento
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_filepath ON videos(filepath)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transcriptions_video ON transcriptions(video_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_summaries_transcription ON summaries(transcription_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_video ON processing_history(video_id)")

            conn.commit()
            logger.info("Esquema de base de datos creado/verificado correctamente")

    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión a la base de datos

        Uso:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(...)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Ejecuta una consulta SELECT y retorna los resultados

        Args:
            query: Consulta SQL
            params: Parámetros de la consulta

        Returns:
            Lista de resultados
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Ejecuta una consulta INSERT/UPDATE/DELETE

        Args:
            query: Consulta SQL
            params: Parámetros de la consulta

        Returns:
            ID del último registro insertado o número de filas afectadas
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if query.strip().upper().startswith('INSERT') else cursor.rowcount

    def get_stats(self) -> dict:
        """
        Obtiene estadísticas de la base de datos

        Returns:
            Diccionario con estadísticas
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total de videos
            cursor.execute("SELECT COUNT(*) FROM videos")
            stats['total_videos'] = cursor.fetchone()[0]

            # Total de transcripciones
            cursor.execute("SELECT COUNT(*) FROM transcriptions")
            stats['total_transcriptions'] = cursor.fetchone()[0]

            # Total de resúmenes
            cursor.execute("SELECT COUNT(*) FROM summaries")
            stats['total_summaries'] = cursor.fetchone()[0]

            # Tamaño total de videos
            cursor.execute("SELECT SUM(file_size) FROM videos")
            result = cursor.fetchone()[0]
            stats['total_size_bytes'] = result if result else 0
            stats['total_size_mb'] = round(stats['total_size_bytes'] / (1024 * 1024), 2)

            # Promedio de compression ratio
            cursor.execute("SELECT AVG(compression_ratio) FROM summaries")
            result = cursor.fetchone()[0]
            stats['avg_compression_ratio'] = round(result, 2) if result else 0

            return stats

    def clear_database(self):
        """Elimina todos los datos de la base de datos (mantiene estructura)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM processing_history")
            cursor.execute("DELETE FROM summaries")
            cursor.execute("DELETE FROM transcriptions")
            cursor.execute("DELETE FROM videos")
            conn.commit()
            logger.warning("Base de datos limpiada completamente")
