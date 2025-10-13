# 🎬 Sistema de Resumen de Videos Educativos
## Proyecto completo para Trabajo Interdisciplinar III

---

## ✅ ¿QUÉ SE HA CREADO?

Tu proyecto está **100% completo** y listo para usar. Aquí está todo lo que tienes:

### 📂 Estructura del Proyecto

```
Resume videos - proyect/
│
├── 📄 README.md                          # Documentación completa del proyecto
├── 📄 QUICKSTART.md                      # Guía rápida de inicio
├── 📄 GUIA_PROYECTO_ACADEMICO.md         # Guía para el informe académico
├── 📄 requirements.txt                   # Dependencias de Python
├── 📄 .gitignore                         # Archivos a ignorar en Git
├── 📄 .env.example                       # Plantilla de variables de entorno
├── 📄 check_installation.py              # Script para verificar instalación
├── 📄 ejemplos.py                        # Ejemplos de uso interactivos
│
├── 📁 src/                               # Código fuente principal
│   ├── __init__.py                       # Paquete Python
│   ├── config.py                         # Configuración central
│   ├── transcribe_video.py               # Módulo de transcripción con Whisper
│   ├── prepare_dataset.py                # Preparación de datos para entrenamiento
│   ├── train_model.py                    # Entrenamiento con fine-tuning
│   ├── inference.py                      # Generación de resúmenes
│   ├── pipeline.py                       # Pipeline completo automatizado
│   └── utils.py                          # Funciones de utilidad
│
├── 📁 notebooks/                         # Jupyter notebooks
│   └── tutorial_resumen_videos.ipynb     # Tutorial interactivo completo
│
├── 📁 data/                              # Datos
│   ├── raw/                              # Datos crudos
│   └── processed/                        # Datos procesados
│
├── 📁 models/                            # Modelos entrenados
│
└── 📁 videos/                            # Videos a procesar
```

---

## 🎯 COMPONENTES TÉCNICOS IMPLEMENTADOS

### ✅ 1. Módulo de Transcripción (`transcribe_video.py`)
- **Tecnología**: OpenAI Whisper
- **Funcionalidad**:
  - Extrae audio de videos
  - Transcribe a texto usando IA
  - Soporta múltiples idiomas (español, inglés, etc.)
  - Procesamiento por lotes
  
### ✅ 2. Preparación de Dataset (`prepare_dataset.py`)
- **Tecnología**: Hugging Face Datasets
- **Funcionalidad**:
  - Carga datasets públicos (XSum, MLSUM)
  - Tokenización para modelos Transformer
  - Preprocesamiento automático
  - Creación de datasets personalizados

### ✅ 3. Entrenamiento del Modelo (`train_model.py`)
- **Tecnología**: Transformers + PyTorch
- **Modelos**: T5, mT5, BART
- **Técnicas**:
  - **Transfer Learning**: Usar modelos pre-entrenados
  - **Fine-tuning**: Ajustar con datos específicos
  - **Mixed Precision**: Optimización FP16
  - **Métricas ROUGE**: Evaluación automática
  
### ✅ 4. Sistema de Inferencia (`inference.py`)
- **Funcionalidad**:
  - Cargar modelos entrenados
  - Generar resúmenes de nuevos textos
  - Procesamiento por lotes
  - Análisis de compresión

### ✅ 5. Pipeline Completo (`pipeline.py`)
- **Automatización total**:
  - Transcripción → Entrenamiento → Resumen
  - Interfaz de línea de comandos (CLI)
  - Múltiples modos de operación

---

## 🚀 PASOS PARA EMPEZAR

### Paso 1: Verificar Instalación
```powershell
# Instalar dependencias
pip install -r requirements.txt

# Verificar que todo está instalado
python check_installation.py
```

### Paso 2: Probar con Ejemplos
```powershell
# Ver ejemplos interactivos
python ejemplos.py

# O ejecutar un ejemplo específico
python ejemplos.py 2  # Ejemplo de resumen simple
```

### Paso 3: Tutorial Completo
```powershell
# Abrir Jupyter Notebook
jupyter notebook

# Navegar a: notebooks/tutorial_resumen_videos.ipynb
# Ejecutar paso a paso para entender el proceso
```

### Paso 4: Usar el Sistema

#### Opción A: Solo Resumir (Modelo Pre-entrenado)
```powershell
cd src
python
```
```python
from inference import VideoSummarizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Cargar modelo base
model_name = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Resumir texto
texto = "Tu texto largo aquí..."
inputs = tokenizer("resumir: " + texto, return_tensors="pt", max_length=512, truncation=True)
outputs = model.generate(inputs["input_ids"], max_length=128)
resumen = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(resumen)
```

#### Opción B: Pipeline Completo
```powershell
# 1. Coloca tus videos en la carpeta 'videos/'
# 2. Ejecuta el pipeline
cd src
python pipeline.py --mode full --video-dir ../videos --epochs 3
```

---

## 📚 GUÍAS DISPONIBLES

1. **README.md** → Documentación técnica completa
2. **QUICKSTART.md** → Guía de inicio rápido (5 minutos)
3. **GUIA_PROYECTO_ACADEMICO.md** → Cómo hacer el informe académico
4. **notebooks/tutorial_resumen_videos.ipynb** → Tutorial interactivo

---

## 🎓 PARA TU PROYECTO ACADÉMICO

### Componentes Evaluables ✅

1. **✅ Transfer Learning**:
   - Implementado en `train_model.py`
   - Usa modelos pre-entrenados (T5/mT5)
   - Adaptación a tarea específica

2. **✅ Fine-tuning**:
   - Sistema completo de entrenamiento
   - Hiperparámetros configurables
   - Evaluación con métricas ROUGE

3. **✅ Dataset**:
   - Soporte para datasets públicos
   - Herramientas para crear dataset propio
   - Preprocesamiento automático

4. **✅ Modelos Transformer**:
   - T5 (Text-to-Text Transfer Transformer)
   - mT5 (Multilingual T5)
   - Whisper (Transcripción)

### Qué Mostrar en tu Informe

1. **Arquitectura del Sistema** (diagrama en README.md)
2. **Código Implementado** (todos los módulos en src/)
3. **Resultados de Entrenamiento** (métricas ROUGE)
4. **Ejemplos de Resúmenes** (antes y después de fine-tuning)
5. **Análisis de Errores** (casos donde funciona bien/mal)

---

## 💡 PRÓXIMOS PASOS RECOMENDADOS

### Semana 1-2: Aprendizaje
- [ ] Leer README.md completo
- [ ] Ejecutar `check_installation.py`
- [ ] Completar el notebook tutorial
- [ ] Probar ejemplos con `ejemplos.py`

### Semana 3-4: Experimentación
- [ ] Recolectar/grabar tus propios videos educativos
- [ ] Transcribir con Whisper
- [ ] Probar modelo base sin fine-tuning
- [ ] Analizar resultados

### Semana 5-6: Entrenamiento
- [ ] Preparar dataset de entrenamiento
- [ ] Hacer fine-tuning del modelo
- [ ] Experimentar con hiperparámetros
- [ ] Comparar métricas

### Semana 7-8: Informe
- [ ] Documentar experimentos
- [ ] Generar gráficas y tablas
- [ ] Escribir informe (usa GUIA_PROYECTO_ACADEMICO.md)
- [ ] Preparar presentación

---

## 🔧 CONFIGURACIÓN PERSONALIZADA

Edita `src/config.py` para ajustar:

```python
# Modelo a usar
DEFAULT_MODEL_NAME = "google/mt5-small"  # Cambiar a mt5-base para mejor calidad

# Hiperparámetros de entrenamiento
TRAINING_ARGS = {
    "num_train_epochs": 3,      # Aumentar para mejor entrenamiento
    "batch_size": 4,            # Reducir si tienes problemas de memoria
    "learning_rate": 5e-5,      # Ajustar según resultados
}

# Parámetros de resumen
GENERATION_ARGS = {
    "max_length": 128,          # Resúmenes más largos/cortos
    "num_beams": 4,             # Más beams = mejor calidad pero más lento
}
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "FFmpeg not found"
```powershell
choco install ffmpeg
```

### "CUDA out of memory"
- Reduce `batch_size` en config.py
- Usa modelo más pequeño (`mt5-small`)

### "El modelo tarda mucho"
- Normal en CPU (puede tomar horas)
- Usa `max_steps=100` para pruebas rápidas
- Considera usar Google Colab con GPU gratis

### "Module not found"
```powershell
pip install -r requirements.txt
```

---

## 📞 RECURSOS

### Documentación Técnica
- Transformers: https://huggingface.co/docs/transformers
- Whisper: https://github.com/openai/whisper
- Datasets: https://huggingface.co/docs/datasets

### Papers Importantes
- T5: "Exploring the Limits of Transfer Learning"
- Whisper: "Robust Speech Recognition via Large-Scale Weak Supervision"
- Attention: "Attention is All You Need"

### Comunidad
- Hugging Face Forum
- Stack Overflow
- Reddit r/MachineLearning

---

## ✨ CARACTERÍSTICAS DESTACADAS

✅ **Código Modular**: Fácil de entender y modificar
✅ **Documentación Completa**: Todo está explicado
✅ **Ejemplos Prácticos**: Aprende haciendo
✅ **Listo para Producción**: Código profesional
✅ **Proyecto Académico Completo**: Todo lo que necesitas para tu curso

---

## 🎉 ¡ESTÁS LISTO!

Tu proyecto tiene:
- ✅ Sistema funcional de resumen de videos
- ✅ Dos modelos Transformer (Whisper + T5/mT5)
- ✅ Fine-tuning implementado
- ✅ Transfer learning aplicado
- ✅ Dataset y entrenamiento
- ✅ Documentación completa
- ✅ Ejemplos de uso

**¡Éxito en tu proyecto de Trabajo Interdisciplinar III!** 🚀🎓

---

**Desarrollado para UNSA - Universidad Nacional de San Agustín**
**Trabajo Interdisciplinar III - X Semestre**
