# 🎥 Sistema de Resumen de Videos Educativos

Sistema completo de resumen automático de videos educativos usando **Transformers** y **Whisper**. Extrae texto de videos, entrena modelos con fine-tuning y genera resúmenes concisos.

## 📋 Descripción del Proyecto

Este proyecto implementa un pipeline end-to-end para:
1. **Extraer audio** de videos educativos
2. **Transcribir** el audio a texto usando Whisper (OpenAI)
3. **Entrenar modelos** Transformer (T5/mT5) con fine-tuning
4. **Generar resúmenes** automáticos de las transcripciones

Ideal para proyectos académicos de procesamiento de lenguaje natural y aprendizaje automático.

## 🏗️ Arquitectura

```
Video → Audio → Transcripción → Modelo Transformer → Resumen
         ↓           ↓                    ↓
      (Whisper)   (Dataset)         (T5/mT5 + Fine-tuning)
```

### Modelos Utilizados

1. **Whisper** (OpenAI): Transcripción de audio a texto
   - Multilingüe (español, inglés, etc.)
   - Modelos: tiny, base, small, medium, large

2. **T5/mT5** (Google): Resumen de texto
   - T5: Para textos en inglés
   - mT5: Para español y múltiples idiomas
   - Fine-tuning con datasets específicos

## 📁 Estructura del Proyecto

```
Resume videos - proyect/
├── src/
│   ├── transcribe_video.py    # Extracción de audio y transcripción
│   ├── prepare_dataset.py     # Preparación de datos para entrenamiento
│   ├── train_model.py          # Fine-tuning del modelo
│   ├── inference.py            # Generación de resúmenes
│   └── pipeline.py             # Pipeline completo
├── data/
│   ├── raw/                    # Datos crudos
│   └── processed/              # Datos procesados
├── models/                     # Modelos entrenados
├── videos/                     # Videos a procesar
├── notebooks/                  # Jupyter notebooks para experimentación
├── requirements.txt            # Dependencias
└── README.md                   # Esta documentación
```

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.8+
- FFmpeg (para procesamiento de audio/video)
- CUDA (opcional, para GPU)

#### Instalar FFmpeg (Windows)

```powershell
# Usando Chocolatey
choco install ffmpeg

# O descarga desde: https://ffmpeg.org/download.html
```

### 2. Configurar Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Instalación de PyTorch

```powershell
# Con GPU (CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Sin GPU (CPU only)
pip install torch torchvision torchaudio
```

## 📖 Uso

### Opción 1: Pipeline Completo (Recomendado para Aprendizaje)

Procesa videos desde cero, entrena el modelo y genera resúmenes:

```powershell
cd src
python pipeline.py --mode full --video-dir ../videos --epochs 3
```

### Opción 2: Solo Inferencia (Modelo Pre-entrenado)

Si ya tienes un modelo entrenado:

```powershell
cd src
python pipeline.py --mode inference --video mi_video.mp4 --model-path ../models/video-summarizer
```

### Opción 3: Paso a Paso

#### Paso 1: Transcribir Videos

```powershell
cd src
python transcribe_video.py
```

Modifica el archivo para especificar tus videos:
```python
transcriber = VideoTranscriber(model_size="base", language="es")
transcriber.batch_transcribe("../videos")
```

#### Paso 2: Preparar Dataset

```powershell
python prepare_dataset.py
```

Esto descargará un dataset público (XSum o MLSUM) para entrenamiento.

#### Paso 3: Entrenar Modelo

```powershell
python train_model.py
```

Ajusta hiperparámetros en el código:
```python
trainer.train(
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    num_train_epochs=3,
    batch_size=4,  # Ajustar según tu GPU
    learning_rate=5e-5
)
```

#### Paso 4: Generar Resúmenes

```powershell
python inference.py
```

```python
summarizer = VideoSummarizer(model_path="../models/mt5-video-summarizer")
summary = summarizer.summarize(texto)
print(summary)
```

## 🧪 Experimentación con Notebooks

Usa los notebooks de Jupyter para experimentar:

```powershell
jupyter notebook
```

Crea notebooks en la carpeta `notebooks/` para:
- Análisis exploratorio de datos
- Pruebas de modelos
- Visualización de métricas
- Comparación de hiperparámetros

## 📊 Datasets Recomendados

### Para Español
- **MLSUM**: Dataset de resumen en español
- **WikiLingua**: Resúmenes multilingües
- **Custom**: Crear tu propio dataset con transcripciones y resúmenes manuales

### Para Inglés
- **XSum**: Resúmenes extremos de noticias BBC
- **CNN/DailyMail**: Resúmenes de noticias
- **SAMSum**: Conversaciones y resúmenes

## 🎯 Modelos Recomendados

| Modelo | Idioma | Tamaño | Uso Recomendado |
|--------|--------|--------|-----------------|
| `google/mt5-small` | Multilingüe | ~300MB | Pruebas rápidas |
| `google/mt5-base` | Multilingüe | ~1GB | Producción (español) |
| `t5-small` | Inglés | ~240MB | Pruebas (inglés) |
| `t5-base` | Inglés | ~850MB | Producción (inglés) |
| `facebook/bart-base` | Inglés | ~560MB | Alternativa a T5 |

## ⚙️ Configuración Avanzada

### Hiperparámetros de Entrenamiento

```python
# En train_model.py
trainer.train(
    num_train_epochs=3,           # Número de épocas
    batch_size=4,                 # Tamaño de batch (ajustar según memoria)
    learning_rate=5e-5,           # Tasa de aprendizaje
    warmup_steps=500,             # Pasos de warmup
    max_input_length=512,         # Longitud máxima del input
    max_target_length=128,        # Longitud máxima del resumen
)
```

### Parámetros de Generación

```python
# En inference.py
summary = summarizer.summarize(
    text,
    max_length=128,               # Longitud máxima del resumen
    min_length=30,                # Longitud mínima
    num_beams=4,                  # Beam search (más = mejor calidad)
    length_penalty=2.0,           # Penalización por longitud
    early_stopping=True
)
```

## 📈 Métricas de Evaluación

El sistema usa **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation):

- **ROUGE-1**: Overlap de unigramas
- **ROUGE-2**: Overlap de bigramas
- **ROUGE-L**: Subsecuencia común más larga

```python
# Las métricas se calculan automáticamente durante el entrenamiento
# y se guardan en models/video-summarizer/
```

## 🐛 Solución de Problemas

### Error: FFmpeg no encontrado

```powershell
# Instalar FFmpeg
choco install ffmpeg
# O agregar a PATH manualmente
```

### Error: CUDA out of memory

```python
# Reducir batch_size en train_model.py
batch_size=2  # En lugar de 4
```

### Modelo muy lento en CPU

```python
# Usar modelos más pequeños
model_name="google/mt5-small"  # En lugar de mt5-base
whisper_model="tiny"           # En lugar de base
```

## 📚 Recursos Adicionales

### Documentación
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Whisper](https://github.com/openai/whisper)
- [Datasets](https://huggingface.co/docs/datasets)

### Tutoriales
- [Fine-tuning T5 para resumen](https://huggingface.co/docs/transformers/tasks/summarization)
- [Evaluación con ROUGE](https://huggingface.co/spaces/evaluate-metric/rouge)

### Papers
- [Exploring the Limits of Transfer Learning with T5](https://arxiv.org/abs/1910.10683)
- [BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)
- [Whisper: Robust Speech Recognition](https://arxiv.org/abs/2212.04356)

## 🎓 Para Proyecto Académico

### Componentes Evaluables

1. **Preprocesamiento**: 
   - Extracción y limpieza de audio
   - Transcripción con Whisper
   - Preparación de dataset

2. **Modelo de ML**:
   - Fine-tuning de T5/mT5
   - Transfer learning
   - Optimización de hiperparámetros

3. **Evaluación**:
   - Métricas ROUGE
   - Comparación de modelos
   - Análisis de resultados

4. **Aplicación**:
   - Pipeline funcional
   - Interfaz de usuario (opcional)
   - Documentación completa

### Sugerencias de Mejoras

1. **Dataset Personalizado**: Crear tu propio dataset con videos y resúmenes manuales
2. **Web Interface**: Agregar Flask/Streamlit para UI web
3. **Múltiples Modelos**: Comparar T5, BART, PEGASUS
4. **Segmentación**: Resumir por secciones del video
5. **Multi-idioma**: Entrenar para varios idiomas simultáneamente

## 🤝 Contribuciones

Este es un proyecto académico. Siéntete libre de:
- Agregar nuevas funcionalidades
- Mejorar la documentación
- Reportar issues
- Optimizar el código

## 📝 Licencia

Proyecto académico para Trabajo Interdisciplinar III - UNSA

## 👤 Autor

Proyecto desarrollado para el curso de Trabajo Interdisciplinar III
Universidad Nacional de San Agustín (UNSA)

---

**¡Buena suerte con tu proyecto! 🚀**
