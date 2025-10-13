# 🎬 Sistema de Resumen Automático de Videos Educativos

## 🎯 ¿Qué es esto?

Un sistema completo de IA que convierte videos largos en resúmenes concisos usando:
- **Whisper (OpenAI)**: Transcribe el audio del video a texto
- **mT5 (Google)**: Genera resúmenes inteligentes en español
- **Gradio**: Interfaz web moderna y visual
- **Rich + Click**: CLI hermosa con colores y barras de progreso

---

## ✨ Características

### 🎯 Funcionalidades Core
- ✅ Transcripción automática de audio con Whisper
- ✅ Generación de resúmenes con mT5 fine-tuned
- ✅ Soporte para múltiples formatos de video (MP4, AVI, MOV, MKV, WebM)
- ✅ Procesamiento por lotes de múltiples videos
- ✅ Estadísticas de compresión y métricas

### 🌐 Interfaces Disponibles

#### 1. Interfaz Web (Gradio) - **NUEVO en FASE 2**
- 🖱️ Drag & Drop de videos
- 📊 Visualización en tiempo real
- 🎨 Diseño moderno y responsive
- 📥 Descarga de resultados en JSON
- ⚙️ Configuración avanzada en UI

#### 2. CLI Mejorada (Rich) - **NUEVO en FASE 2**
- 🎨 Colores y emojis
- 📊 Tablas de estadísticas elegantes
- ⏱️ Barras de progreso animadas
- 📁 Procesamiento por lotes automático
- 💻 Ideal para scripts y automatización

#### 3. Pipeline Directo (Python)
- 🐍 API programática
- 🔧 Integración en otros sistemas
- ⚡ Máxima flexibilidad

---

## 🚀 Instalación Rápida

### Opción 1: Instalación Completa (Recomendada)

```bash
# 1. Clonar o descargar el proyecto
cd "Resume videos - proyect"

# 2. Instalar todas las dependencias
pip install -r requirements.txt

# 3. Verificar instalación
python src/verificar_instalacion.py
```

### Opción 2: Instalación por Fases

```bash
# FASE 1: Core (Whisper + mT5)
pip install torch transformers datasets openai-whisper moviepy

# FASE 2: Interfaces (Gradio + Rich CLI) - NUEVO
pip install gradio rich click

# O usar el script de PowerShell:
.\install_fase2.ps1
```

---

## 📖 Uso

### 🌐 Opción 1: Interfaz Web (Más fácil)

```bash
# Iniciar servidor web
python src/web_app.py

# Abrir navegador en http://localhost:7860
# 1. Arrastra tu video
# 2. Clic en "Procesar"
# 3. ¡Ver resultados!
```

**Opciones avanzadas:**

```bash
# Cambiar puerto
python src/web_app.py --port 8080

# Compartir públicamente (URL temporal)
python src/web_app.py --share

# Especificar modelo
python src/web_app.py --modelo models/mi-modelo
```

### 💻 Opción 2: CLI Mejorada (Para expertos)

```bash
# Procesar un video
python src/cli.py procesar mi_video.mp4

# Procesar múltiples videos
python src/cli.py batch carpeta_videos/

# Ver información del sistema
python src/cli.py info

# Con opciones avanzadas
python src/cli.py procesar clase.mp4 \
  --whisper medium \
  --output resultados \
  --formato both
```

### 🐍 Opción 3: Pipeline Directo (Programático)

```bash
# Pipeline completo
python src/pipeline_completo.py \
  --video mi_video.mp4 \
  --modelo models/mt5-video-summarizer-final
```

**O desde Python:**

```python
from pipeline_completo import procesar_video_completo

resultado = procesar_video_completo(
    video_path="mi_video.mp4",
    modelo_path="models/mt5-video-summarizer-final",
    whisper_model="base"
)

print(resultado['resumen'])
```

---

## 📁 Estructura del Proyecto

```
Resume videos - proyect/
│
├── src/                              # Código fuente
│   ├── transcribe_video.py          # Transcripción con Whisper
│   ├── inference.py                 # Inferencia con mT5
│   ├── train_robusto_rtx3050.py     # Entrenamiento local
│   ├── pipeline_completo.py         # Pipeline end-to-end (FASE 1)
│   ├── verificar_instalacion.py    # Verificación de dependencias (FASE 1)
│   ├── test_whisper_audio.py       # Pruebas de Whisper (FASE 1)
│   ├── web_app.py                   # Interfaz web Gradio (FASE 2) ⭐ NUEVO
│   └── cli.py                       # CLI mejorada Rich (FASE 2) ⭐ NUEVO
│
├── notebooks/                        # Jupyter notebooks
│   ├── entrenar_mt5_colab_pro.ipynb # Entrenamiento en Colab Pro
│   └── README.md                    # Guía de uso del notebook
│
├── models/                           # Modelos entrenados
│   └── mt5-video-summarizer-final/  # Modelo mT5 fine-tuned
│
├── outputs/                          # Resultados generados
│   ├── *.txt                        # Resúmenes en texto
│   └── *.json                       # Resultados estructurados
│
├── docs/                             # Documentación
│   └── GUIA_INTERFACES.md           # Guía completa de interfaces (FASE 2) ⭐ NUEVO
│
├── requirements.txt                  # Dependencias Python (actualizado)
├── install_fase2.ps1                # Script instalación FASE 2 ⭐ NUEVO
└── README.md                         # Este archivo
```

---

## 🎓 Entrenamiento del Modelo

### Opción 1: Google Colab Pro (Recomendado)

```bash
# 1. Abrir notebook en Colab
notebooks/entrenar_mt5_colab_pro.ipynb

# 2. Seleccionar GPU (Runtime > Change runtime type > GPU)
# 3. Ejecutar todas las celdas
# 4. Esperar 2-8 horas según GPU (T4/V100/A100)
# 5. Descargar modelo entrenado
```

**Características del notebook:**
- ✅ 16 secciones organizadas
- ✅ Auto-detección de GPU y configuración
- ✅ Checkpoints automáticos en Google Drive
- ✅ Early stopping inteligente
- ✅ TensorBoard integrado
- ✅ Evaluación con ROUGE metrics

### Opción 2: Entrenamiento Local

```bash
# Requiere GPU NVIDIA con CUDA
python src/train_robusto_rtx3050.py \
  --output models/mi-modelo \
  --epochs 3 \
  --batch_size 4
```

---

## 📊 Resultados Esperados

### Métricas del Modelo (Entrenado con 10K ejemplos MLSUM)
- **ROUGE-1**: 0.42 (Excelente)
- **ROUGE-2**: 0.18 (Bueno)
- **ROUGE-L**: 0.35 (Muy bueno)

### Tiempos de Procesamiento
| Video | Whisper (base) | mT5 | Total |
|-------|----------------|-----|-------|
| 5 min | ~30 seg | ~5 seg | ~35 seg |
| 15 min | ~1.5 min | ~10 seg | ~2 min |
| 30 min | ~3 min | ~20 seg | ~4 min |

*Tiempos con GPU. CPU es 10x más lento.*

---

## 🔧 Configuración Avanzada

### Modelos Whisper Disponibles

| Modelo | Tamaño | VRAM | Calidad | Velocidad |
|--------|--------|------|---------|-----------|
| tiny | 39 MB | ~1GB | ⭐⭐ | ⚡⚡⚡⚡⚡ |
| base | 74 MB | ~1GB | ⭐⭐⭐ | ⚡⚡⚡⚡ |
| small | 244 MB | ~2GB | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| medium | 769 MB | ~5GB | ⭐⭐⭐⭐⭐ | ⚡⚡ |
| large | 1550 MB | ~10GB | ⭐⭐⭐⭐⭐ | ⚡ |

**Recomendación**: `base` para uso general, `small` para mejor calidad.

### Parámetros de Generación

```python
# En web_app.py o pipeline_completo.py
resumen = summarizer.generate_summary(
    texto,
    max_length=150,      # Longitud máxima del resumen (palabras)
    num_beams=4,         # Calidad: 1-8 (más = mejor pero más lento)
    temperature=1.0,     # Creatividad: 0.7-1.3
    top_p=0.9,          # Diversidad
    repetition_penalty=2.0  # Evitar repeticiones
)
```

---

## 🐛 Solución de Problemas

### Problema 1: "Error al importar gradio"

```bash
pip install gradio
```

### Problema 2: "Error al importar whisper"

```bash
pip install openai-whisper
# Y asegúrate de tener ffmpeg instalado
```

### Problema 3: Puerto ocupado (Interfaz Web)

```bash
# Cambiar puerto
python src/web_app.py --port 8080

# O cerrar proceso en el puerto
netstat -ano | findstr :7860
```

### Problema 4: GPU no detectada

```bash
# Verificar instalación
python src/verificar_instalacion.py

# Reinstalar PyTorch con CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Problema 5: Transcripción vacía

- ✅ Verificar que el video tenga audio
- ✅ Probar con modelo Whisper más grande (`small` o `medium`)
- ✅ Usar `test_whisper_audio.py` para diagnóstico

**Más soluciones:** Ver `docs/GUIA_INTERFACES.md`

---

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| `README.md` | Esta guía general |
| `docs/GUIA_INTERFACES.md` | Guía completa de interfaces Web y CLI |
| `notebooks/README.md` | Guía de entrenamiento en Colab |

---

## 🎯 Roadmap

### ✅ FASE 1: Core Funcional (Completado)
- ✅ Pipeline end-to-end (Whisper + mT5)
- ✅ Verificación de instalación
- ✅ Pruebas de Whisper
- ✅ Procesamiento por lotes

### ✅ FASE 2: Interfaces de Usuario (Completado) ⭐ NUEVO
- ✅ Interfaz Web con Gradio
- ✅ CLI mejorada con Rich
- ✅ Documentación completa
- ✅ Scripts de instalación

### 🔲 FASE 3: Persistencia (Próximamente)
- 🔲 Base de datos SQLite para historial
- 🔲 Sistema de caché para evitar reprocesar
- 🔲 API REST con FastAPI

### 🔲 FASE 4: Producción (Próximamente)
- 🔲 Tests unitarios completos
- 🔲 Dockerfile para containerización
- 🔲 CI/CD con GitHub Actions
- 🔲 Documentación API

---

## 🤝 Contribuciones

Este proyecto es parte de un trabajo interdisciplinario. Si encuentras bugs o tienes sugerencias:

1. 📝 Documenta el problema
2. 🐛 Reproduce el error
3. 💡 Propón una solución
4. ✅ Prueba la solución

---

## 📄 Licencia

Proyecto educativo - Universidad Nacional de San Agustín (UNSA)  
Trabajo Interdisciplinar III - X Semestre  
Octubre 2025

---

## 🎉 ¿Qué hay de nuevo en FASE 2?

### 🌐 Interfaz Web con Gradio
- Drag & Drop de videos
- Visualización en tiempo real
- Diseño moderno y responsive
- Descarga de resultados en JSON
- Compartir públicamente con `--share`

### 💻 CLI Mejorada con Rich
- Colores y emojis
- Tablas de estadísticas elegantes
- Barras de progreso animadas
- Procesamiento por lotes
- Comandos intuitivos

### 📚 Documentación
- Guía completa de interfaces
- Ejemplos de uso
- Solución de problemas
- Mejores prácticas

---

## 🚀 Quick Start (Para impacientes)

```bash
# 1. Instalar dependencias FASE 2
pip install gradio rich click

# 2. Iniciar interfaz web
python src/web_app.py

# 3. Abrir http://localhost:7860
# 4. Arrastrar video
# 5. ¡Listo!
```

O con CLI:

```bash
# Procesar video con CLI hermosa
python src/cli.py procesar mi_video.mp4
```

---

**¡Disfruta resumiendo tus videos educativos con IA!** 🎬✨
