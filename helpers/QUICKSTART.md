# 🚀 Guía Rápida de Inicio

## Instalación en 5 minutos

### 1. Instalar FFmpeg

```powershell
# Windows con Chocolatey
choco install ffmpeg

# O descargar desde: https://ffmpeg.org/download.html
```

### 2. Crear entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Instalar PyTorch

```powershell
# Con GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Sin GPU
pip install torch torchvision torchaudio
```

## Uso Rápido

### Opción A: Resumir un video (inferencia solamente)

```powershell
cd src

# 1. Transcribir
python
>>> from transcribe_video import VideoTranscriber
>>> transcriber = VideoTranscriber(model_size="base", language="es")
>>> transcript = transcriber.transcribe_video("../videos/mi_video.mp4")
>>> print(transcript['text'])

# 2. Resumir (necesitas modelo entrenado primero)
>>> from inference import VideoSummarizer
>>> summarizer = VideoSummarizer(model_path="../models/video-summarizer")
>>> resumen = summarizer.summarize(transcript['text'])
>>> print(resumen)
```

### Opción B: Entrenar tu propio modelo

```powershell
cd src

# 1. Preparar dataset
python prepare_dataset.py

# 2. Entrenar modelo (esto tomará tiempo)
python train_model.py

# 3. Usar modelo entrenado
python inference.py
```

### Opción C: Pipeline completo

```powershell
cd src
python pipeline.py --mode full --video-dir ../videos --epochs 3
```

## Primeros Pasos Recomendados

1. **Empieza con el notebook**: `notebooks/tutorial_resumen_videos.ipynb`
   - Abre Jupyter: `jupyter notebook`
   - Ejecuta celda por celda para entender el proceso

2. **Prueba con modelo pre-entrenado**:
   - Antes de entrenar, prueba el modelo base de Hugging Face
   - Esto te da una idea del resultado esperado

3. **Entrena con datos pequeños**:
   - Usa `num_samples=1000` en prepare_dataset.py
   - Usa `max_steps=100` en train_model.py
   - Esto te permite iterar rápido

4. **Escala gradualmente**:
   - Aumenta el dataset progresivamente
   - Prueba diferentes modelos (mt5-small → mt5-base)
   - Ajusta hiperparámetros

## Comandos Útiles

```powershell
# Ver estructura del proyecto
tree /F

# Verificar instalación de PyTorch
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

# Verificar instalación de Whisper
python -c "import whisper; print(whisper.__version__)"

# Listar modelos disponibles
python -c "from transformers import AutoModel; print('Transformers instalado correctamente')"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Desactivar entorno virtual
deactivate
```

## Solución Rápida de Problemas

### Error: "FFmpeg not found"
```powershell
choco install ffmpeg
# O agregar a PATH
```

### Error: "CUDA out of memory"
- Reduce `batch_size=2` en train_model.py
- Usa modelo más pequeño: `mt5-small`

### Error: "Module not found"
```powershell
pip install -r requirements.txt
```

### El modelo tarda mucho
- Usa CPU si no tienes GPU (será más lento pero funciona)
- Reduce `num_samples` y `max_steps`

## Recursos Adicionales

- README.md: Documentación completa
- notebooks/: Tutoriales interactivos
- src/config.py: Configuración central
- src/utils.py: Utilidades

## ¿Necesitas Ayuda?

1. Lee el README.md completo
2. Revisa el notebook tutorial
3. Consulta la documentación de Hugging Face
4. Ajusta los parámetros en config.py

¡Buena suerte con tu proyecto! 🎓
