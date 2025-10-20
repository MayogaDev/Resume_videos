-- Schema de Base de Datos para Sistema de Resumen de Videos
-- SQLite Database Schema

-- Tabla de videos
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT UNIQUE NOT NULL,
    file_size INTEGER,
    duration REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de transcripciones
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
);

-- Tabla de resúmenes
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
);

-- Tabla de historial de procesamiento
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
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_videos_filepath ON videos(filepath);
CREATE INDEX IF NOT EXISTS idx_transcriptions_video ON transcriptions(video_id);
CREATE INDEX IF NOT EXISTS idx_summaries_transcription ON summaries(transcription_id);
CREATE INDEX IF NOT EXISTS idx_history_video ON processing_history(video_id);

-- Triggers para actualizar timestamps
CREATE TRIGGER IF NOT EXISTS update_videos_timestamp
AFTER UPDATE ON videos
BEGIN
    UPDATE videos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
