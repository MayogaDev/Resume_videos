# Base de Datos - Sistema de Resumen de Videos

## Estructura

La base de datos SQLite contiene 4 tablas principales:

### 1. `videos`
Almacena información de los videos procesados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (PK) |
| filename | TEXT | Nombre del archivo |
| filepath | TEXT | Ruta completa (UNIQUE) |
| file_size | INTEGER | Tamaño en bytes |
| duration | REAL | Duración en segundos |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Última actualización |

### 2. `transcriptions`
Almacena las transcripciones de los videos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (PK) |
| video_id | INTEGER | ID del video (FK) |
| text | TEXT | Texto completo transcrito |
| language | TEXT | Idioma detectado |
| model_used | TEXT | Modelo Whisper usado |
| word_count | INTEGER | Número de palabras |
| char_count | INTEGER | Número de caracteres |
| segments_count | INTEGER | Número de segmentos |
| processing_time | REAL | Tiempo de procesamiento |
| created_at | TIMESTAMP | Fecha de creación |

### 3. `summaries`
Almacena los resúmenes generados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (PK) |
| transcription_id | INTEGER | ID de transcripción (FK) |
| summary_text | TEXT | Texto del resumen |
| model_used | TEXT | Modelo usado |
| max_length | INTEGER | Longitud máxima |
| compression_ratio | REAL | Ratio de compresión |
| processing_time | REAL | Tiempo de procesamiento |
| created_at | TIMESTAMP | Fecha de creación |

### 4. `processing_history`
Historial de todos los procesamientos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (PK) |
| video_id | INTEGER | ID del video (FK) |
| transcription_id | INTEGER | ID transcripción (FK) |
| summary_id | INTEGER | ID resumen (FK) |
| status | TEXT | Estado (success/error) |
| error_message | TEXT | Mensaje de error |
| total_time | REAL | Tiempo total |
| created_at | TIMESTAMP | Fecha de creación |

## Ubicación

La base de datos se crea automáticamente en:
```
database/resume_videos.db
```

## Uso

### Desde Python

```python
from backend.database.connection import DatabaseManager
from backend.database.models import Video, Transcription, Summary

# Inicializar conexión
db = DatabaseManager("database/resume_videos.db")

# Obtener estadísticas
stats = db.get_stats()
print(f"Total videos: {stats['total_videos']}")

# Consultar videos
videos = Video.get_all(db, limit=10)
for video in videos:
    print(f"{video.filename} - {video.file_size} bytes")
```

### Desde CLI (SQLite)

```bash
# Abrir base de datos
sqlite3 database/resume_videos.db

# Consultas de ejemplo
SELECT * FROM videos;
SELECT * FROM transcriptions WHERE video_id = 1;
SELECT * FROM summaries ORDER BY created_at DESC LIMIT 5;

# Estadísticas
SELECT COUNT(*) as total FROM videos;
SELECT AVG(compression_ratio) as avg_compression FROM summaries;
```

## Mantenimiento

### Backup
```bash
sqlite3 database/resume_videos.db ".backup database/backup_YYYY-MM-DD.db"
```

### Limpiar datos
```python
from backend.database.connection import DatabaseManager

db = DatabaseManager()
db.clear_database()  # ¡CUIDADO! Elimina todos los datos
```

### Optimizar
```sql
VACUUM;
ANALYZE;
```

## Migraciones

Las migraciones futuras se almacenarán en `database/migrations/`.

Ejemplo de estructura:
```
migrations/
├── 001_initial_schema.sql
├── 002_add_user_table.sql
└── 003_add_indexes.sql
```
