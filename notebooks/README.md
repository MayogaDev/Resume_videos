# 📓 Notebooks de Jupyter - Proyecto de Resumen de Videos

Este directorio contiene notebooks de Jupyter para entrenar y experimentar con el modelo de resumen de videos.

---

## 📚 Notebooks Disponibles

### 1️⃣ `entrenar_mt5_colab_pro.ipynb`
**Notebook principal para entrenar el modelo mT5 en Google Colab Pro**

#### 🎯 Características:
- ✅ Optimizado para GPUs de Google Colab (T4, V100, A100)
- ✅ Configuración automática según GPU detectada
- ✅ Checkpoints automáticos guardados en Google Drive
- ✅ Early stopping inteligente
- ✅ Monitoreo con TensorBoard en tiempo real
- ✅ Evaluación con métricas ROUGE
- ✅ Sistema de recuperación automática
- ✅ Compresión y descarga del modelo entrenado
- ✅ **NUEVO:** Sistema de fallback para ROUGE (soluciona errores de carga)
- ✅ **NUEVO:** Verificación automática de dependencias

#### ⏱️ Tiempo de Entrenamiento:
| GPU | VRAM | Tiempo Estimado | Batch Size |
|-----|------|-----------------|------------|
| T4 | 16GB | 6-8 horas | 4 |
| V100 | 16GB | 4-5 horas | 8 |
| A100 | 40GB | 2-3 horas | 16 |

#### 📊 Resultados Esperados:
- **ROUGE-1:** 0.40-0.45
- **ROUGE-2:** 0.16-0.20
- **ROUGE-L:** 0.32-0.38
- **Loss final:** 0.8-1.0

---

## 🚀 Cómo Usar

### **Opción 1: Google Colab (Recomendado)**

1. **Sube el notebook a Google Colab:**
   - Ve a [Google Colab](https://colab.research.google.com/)
   - Click en `File > Upload notebook`
   - Selecciona `entrenar_mt5_colab_pro.ipynb`

2. **Configura GPU:**
   - `Runtime > Change runtime type`
   - Hardware accelerator: **GPU**
   - GPU type: **V100** o **A100** (Colab Pro)

3. **Ejecuta las celdas en orden:**
   - ▶️ Run all (Ctrl+F9)
   - O ejecuta celda por celda (Shift+Enter)

4. **Monitorea el progreso:**
   - TensorBoard se abre automáticamente
   - Revisa métricas en tiempo real

5. **Descarga el modelo:**
   - Al finalizar, se guarda en Google Drive
   - También puedes descargarlo directamente

### **Opción 2: Jupyter Local (Si tienes GPU potente)**

```bash
# Instalar Jupyter
pip install jupyter

# Iniciar Jupyter
jupyter notebook

# Abrir entrenar_mt5_colab_pro.ipynb
# Nota: Requiere GPU con mínimo 8GB VRAM
```

---

## 📋 Estructura del Notebook

### **Sección 1-3: Setup Inicial**
- Verificación de GPU
- Instalación de dependencias
- Montaje de Google Drive

### **Sección 4-6: Preparación de Datos**
- Configuración de hiperparámetros
- Carga del dataset MLSUM
- Tokenización

### **Sección 7-9: Configuración del Modelo**
- Carga del modelo mT5-small
- Setup de métricas ROUGE
- Configuración del trainer
- Inicio de TensorBoard

### **Sección 10-12: Entrenamiento**
- Entrenamiento principal
- Evaluación en test set
- Guardado del modelo

### **Sección 13-14: Pruebas**
- Inferencia con ejemplos
- Prueba con texto personalizado

### **Sección 15-16: Utilidades**
- Reanudar desde checkpoint
- Descargar modelo

---

## ⚙️ Configuración Personalizada

### Modificar hiperparámetros:

```python
# En la celda de "Configuración de Hiperparámetros":

CONFIG = {
    # Aumentar datos para mejor calidad
    "train_samples": 20000,  # Default: 10000
    
    # Más épocas para mejor aprendizaje
    "num_train_epochs": 5,   # Default: 3
    
    # Ajustar learning rate
    "learning_rate": 5e-5,   # Default: 3e-5
    
    # Batch size (según tu GPU)
    "per_device_train_batch_size": 8,  # Auto-detectado
}
```

### Usar modelo más grande:

```python
# Requiere GPU A100 con 40GB VRAM
CONFIG["model_name"] = "google/mt5-base"  # 580M parámetros
```

---

## 🔧 Solución de Problemas

### ❌ Error: "RuntimeError: CUDA out of memory"

**Solución:**
```python
# Reduce batch size
CONFIG["per_device_train_batch_size"] = 2
CONFIG["gradient_accumulation_steps"] = 8
```

### ❌ Error: "No GPU detected"

**Solución:**
1. Ve a `Runtime > Change runtime type`
2. Selecciona `GPU` en Hardware accelerator
3. Click `Save`
4. Reinicia el runtime

### ❌ Colab se desconecta

**Solución:**
- Los checkpoints se guardan automáticamente cada 500 pasos
- Ejecuta la celda "Reanudar desde checkpoint"
- El entrenamiento continuará desde donde se detuvo

### ⚠️ ROUGE scores muy bajos (<0.30)

**Solución:**
```python
# Aumenta datos y épocas
CONFIG["train_samples"] = 20000
CONFIG["num_train_epochs"] = 5
CONFIG["learning_rate"] = 5e-5
```

---

## 📊 Monitoreo del Entrenamiento

### **TensorBoard**
El notebook inicia TensorBoard automáticamente. Puedes ver:
- 📉 Loss de entrenamiento
- 📈 Métricas ROUGE (validation)
- 📊 Learning rate schedule
- ⚡ Samples per second

### **Logs en Drive**
Todos los logs se guardan en:
```
MyDrive/video_summarizer/logs/
```

### **Checkpoints**
Los checkpoints se guardan en:
```
MyDrive/video_summarizer/checkpoints/mt5-video-summarizer/
```

---

## 💾 Archivos Generados

Después del entrenamiento, encontrarás en tu Google Drive:

```
MyDrive/video_summarizer/
├── models/
│   └── mt5-video-summarizer-final/
│       ├── pytorch_model.bin (1.2 GB)
│       ├── config.json
│       ├── tokenizer.json
│       ├── special_tokens_map.json
│       └── tokenizer_config.json
├── checkpoints/
│   └── mt5-video-summarizer/
│       ├── checkpoint-500/
│       ├── checkpoint-1000/
│       └── checkpoint-1500/
└── logs/
    └── events.out.tfevents...
```

---

## 🚀 Después del Entrenamiento

### 1. Descargar el modelo

**Opción A: Desde Colab (automático)**
- La última celda comprime y descarga automáticamente

**Opción B: Desde Google Drive**
1. Ve a `MyDrive/video_summarizer/models/`
2. Click derecho en `mt5-video-summarizer-final`
3. Descargar

### 2. Usar el modelo localmente

```python
# src/inference.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Cargar modelo entrenado
model = AutoModelForSeq2SeqLM.from_pretrained("models/mt5-video-summarizer-final")
tokenizer = AutoTokenizer.from_pretrained("models/mt5-video-summarizer-final")

# Generar resumen
texto = "Tu texto aquí..."
inputs = tokenizer("resumir: " + texto, return_tensors="pt")
summary_ids = model.generate(inputs["input_ids"], max_length=128)
resumen = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print(resumen)
```

### 3. Integrar con tu proyecto

```bash
# Copiar modelo a tu proyecto
cp -r "Google Drive/video_summarizer/models/mt5-video-summarizer-final" "models/"

# Usar en pipeline
python src/pipeline.py --mode inference --video mi_video.mp4
```

---

## 📈 Mejores Prácticas

### ✅ Para mejor calidad:
1. **Más datos:** Aumenta `train_samples` a 20K-50K
2. **Más épocas:** Entrena 5-6 épocas en lugar de 3
3. **Mejor GPU:** Usa A100 si tienes Colab Pro+
4. **Ajusta LR:** Experimenta con learning rates 3e-5 a 5e-5

### ✅ Para entrenamiento más rápido:
1. **GPU potente:** A100 > V100 > T4
2. **Menos datos:** Usa 5K-10K ejemplos para pruebas
3. **Batch size:** Aumenta según VRAM disponible
4. **FP16:** Ya está habilitado por defecto

### ✅ Para evitar overfitting:
1. **Weight decay:** Aumenta a 0.05
2. **Early stopping:** Ya configurado (patience=3)
3. **Más validación:** Reduce `eval_steps` a 250

---

## 🎯 Próximos Pasos

Después de entrenar tu modelo:

1. ✅ **Integra con Whisper** para transcripción de videos
2. ✅ **Crea interfaz web** con Gradio
3. ✅ **Evalúa en tus propios datos** de videos educativos
4. ✅ **Optimiza hiperparámetros** según resultados
5. ✅ **Sube a Hugging Face Hub** (opcional) para compartir

---

## 📚 Recursos Adicionales

- [Documentación de Transformers](https://huggingface.co/docs/transformers)
- [Google Colab Pro](https://colab.research.google.com/signup)
- [Dataset MLSUM](https://huggingface.co/datasets/mlsum)
- [Modelo mT5](https://huggingface.co/google/mt5-small)
- [Métricas ROUGE](https://en.wikipedia.org/wiki/ROUGE_(metric))

---

## 💡 Tips

- 💾 **Guarda regularmente:** Los checkpoints se guardan automáticamente
- 🔄 **Experimenta:** Prueba diferentes hiperparámetros
- 📊 **Monitorea:** Revisa TensorBoard frecuentemente
- ⏰ **Planifica:** El entrenamiento puede tomar 2-8 horas
- 🌐 **Internet estable:** Importante para Colab

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa la sección "Tips y Solución de Problemas" en el notebook
2. Verifica que tengas GPU habilitada
3. Asegúrate de tener espacio en Google Drive (2GB mínimo)
4. Revisa los logs en `MyDrive/video_summarizer/logs/`

---

**¡Feliz entrenamiento! 🚀**
