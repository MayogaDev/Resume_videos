# Sistema de Resumen Automático de Videos

> Sistema modular de IA para transcripción y resumen de videos educativos usando Whisper y mT5

## Arquitectura del Proyecto

```
Resume_videos/
├── backend/              # Backend - API REST + Lógica de negocio
├── frontend/             # Frontend - Interfaces web y CLI
├── database/             # Base de datos SQLite
├── docs/                 # Documentación completa
├── config/               # Configuraciones
├── scripts/              # Scripts de utilidad
├── tests/                # Tests y datos de prueba
├── outputs/              # Resultados generados
└── README.md             # Este archivo
```

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r config/requirements.txt

# 3. Verificar instalación
python scripts/verify_installation.py
```

## Inicio Rápido

### Opción 1: Interfaz Web (Gradio)
```bash
python scripts/main.py web
# Abrir http://localhost:7860
```

### Opción 2: API REST (Flask)
```bash
# Terminal 1: Iniciar servidor
python scripts/main.py api

# Terminal 2: Hacer peticiones
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"video_path": "tests/test_data/videotest_resumen.mp4"}'
```

### Opción 3: CLI
```bash
python frontend/cli/cli.py procesar tests/test_data/videotest_resumen.mp4
```

### Opción 4: Python Directo
```python
from backend.services.video_processor import VideoProcessorService

processor = VideoProcessorService(whisper_model="base")
result = processor.process_video("video.mp4")

print(result['transcription']['text'])
print(result['summary']['text'])
```

## Características

- **Transcripción precisa** con OpenAI Whisper
- **Resúmenes inteligentes** con mT5 fine-tuned
- **API REST** para integración
- **Interfaz Web** moderna con Gradio
- **CLI avanzada** con Rich
- **Base de datos SQLite** para persistencia
- **Procesamiento por lotes**
- **Historial completo**

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Inicio rápido (5 minutos) |
| [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md) | Estructura detallada del proyecto |
| [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) | Guía de migración |
| [docs/api/README.md](docs/api/README.md) | Documentación API REST |
| [docs/README.md](docs/README.md) | Índice completo de documentación |

## Uso del Sistema

### Verificar Instalación
```bash
python scripts/verify_installation.py
```

### Iniciar Componentes
```bash
# API REST
python scripts/main.py api

# Interfaz Web
python scripts/main.py web

# Verificación del sistema
python scripts/main.py verify
```

### Procesar Videos
```bash
# CLI con un video
python frontend/cli/cli.py procesar video.mp4

# CLI con múltiples videos
python frontend/cli/cli.py batch carpeta_videos/

# Ver estadísticas
python frontend/cli/cli.py stats
```

## API REST - Endpoints

```bash
GET  /api/health              # Health check
GET  /api/stats               # Estadísticas de la BD
POST /api/process             # Procesar video
GET  /api/video/history       # Historial de un video
GET  /api/videos              # Listar todos los videos
```

Ver documentación completa en [docs/api/README.md](docs/api/README.md)

## Tecnologías

- **Backend**: Python 3.8+, Flask, SQLite
- **IA**: Whisper (OpenAI), mT5 (Hugging Face), PyTorch
- **Frontend**: Gradio, Rich, Click
- **Testing**: pytest

## Configuración

Las configuraciones están en `config/`:
- `config.yaml` - Configuración principal
- `requirements.txt` - Dependencias Python
- `.env.example` - Template de variables de entorno

```bash
# Copiar y configurar .env
cp config/.env.example .env
# Editar .env con tus valores
```

## Base de Datos

El sistema usa SQLite con 4 tablas:
- `videos` - Información de videos
- `transcriptions` - Transcripciones
- `summaries` - Resúmenes
- `processing_history` - Historial

Ver detalles en [database/README.md](database/README.md)

## Desarrollo

### Estructura de Módulos

```python
# Backend
from backend.core.transcription import VideoTranscriber
from backend.core.summarization import VideoSummarizer
from backend.services.video_processor import VideoProcessorService
from backend.database.connection import DatabaseManager
from backend.database.models import Video, Transcription, Summary

# API
from backend.api.app import app, run_server
```

### Tests
```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=backend tests/
```

## Roadmap

### ✅ Fase 1 & 2: Completadas
- [x] Core funcional (Whisper + mT5)
- [x] Arquitectura modular
- [x] API REST
- [x] Interfaces Web/CLI
- [x] Base de datos SQLite

### 🔄 Fase 3: En Progreso
- [ ] Tests completos
- [ ] Docker & Docker Compose
- [ ] CI/CD
- [ ] Optimización de rendimiento

### 📋 Fase 4: Futuro
- [ ] Soporte multi-usuario
- [ ] Procesamiento asíncrono (Celery)
- [ ] Frontend React completo
- [ ] Deploy en la nube

## Contribuir

1. Fork el proyecto
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## Licencia

Proyecto educativo - Universidad Nacional de San Agustín (UNSA)
Trabajo Interdisciplinar III - X Semestre
Octubre 2025

## Soporte

- **Documentación**: [docs/](docs/)
- **Guía rápida**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Ejemplos**: [docs/notebooks/](docs/notebooks/)
- **Issues**: Reportar en el repositorio

---

**¡Transforma tus videos largos en resúmenes concisos con IA!** 🎬✨
