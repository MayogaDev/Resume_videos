# 📚 Guía para Proyecto Académico

## Trabajo Interdisciplinar III - UNSA

Esta guía te ayudará a estructurar tu proyecto final para obtener la mejor calificación.

## 🎯 Objetivos del Proyecto

1. ✅ Implementar un sistema funcional de resumen de videos
2. ✅ Aplicar técnicas de Transfer Learning y Fine-tuning
3. ✅ Usar datasets para entrenamiento
4. ✅ Evaluar modelos con métricas apropiadas
5. ✅ Documentar el proceso completo

## 📋 Estructura del Informe Recomendada

### 1. Introducción (2-3 páginas)
- **Problema**: Videos educativos largos requieren mucho tiempo
- **Solución propuesta**: Sistema automático de resumen
- **Objetivos específicos**:
  - Transcribir audio a texto con Whisper
  - Entrenar modelo de resumen con fine-tuning
  - Evaluar calidad de resúmenes

### 2. Marco Teórico (4-5 páginas)

#### 2.1 Transformers
- Arquitectura Transformer (Attention is All You Need)
- Self-attention mechanism
- Encoder-Decoder architecture

#### 2.2 Modelos de Resumen
- **T5 (Text-to-Text Transfer Transformer)**:
  - Arquitectura encoder-decoder
  - Pre-entrenado en C4 dataset
  - Tarea de resumen como traducción
  
- **mT5 (Multilingual T5)**:
  - Extensión multilingüe de T5
  - Soporta 101 idiomas incluyendo español

- **Whisper**:
  - Modelo de reconocimiento de voz
  - Arquitectura encoder-decoder
  - Entrenado en 680,000 horas de audio

#### 2.3 Transfer Learning y Fine-tuning
- **Transfer Learning**: Usar conocimiento de una tarea para otra
- **Fine-tuning**: Ajustar modelo pre-entrenado con datos específicos
- **Ventajas**:
  - Requiere menos datos
  - Converge más rápido
  - Mejor rendimiento

### 3. Metodología (5-6 páginas)

#### 3.1 Arquitectura del Sistema
```
[Diagrama del pipeline completo]

Video → [Whisper] → Transcripción → [T5/mT5] → Resumen
         Audio       Texto             Fine-tuned
```

#### 3.2 Dataset
- **Dataset de entrenamiento**: XSum / MLSUM
  - Características
  - Tamaño
  - Distribución
  
- **Preprocesamiento**:
  - Tokenización
  - Padding y truncation
  - Format T5 (prefix "resumir:")

#### 3.3 Modelo Base
- **Modelo seleccionado**: google/mt5-small
- **Arquitectura**:
  - Encoder: 8 capas
  - Decoder: 8 capas
  - Hidden size: 512
  - Attention heads: 6
  - Parámetros: ~300M

#### 3.4 Entrenamiento
- **Hiperparámetros**:
  ```python
  learning_rate = 5e-5
  batch_size = 4
  num_epochs = 3
  warmup_steps = 500
  max_input_length = 512
  max_target_length = 128
  ```

- **Hardware usado**:
  - CPU/GPU
  - Memoria RAM
  - Tiempo de entrenamiento

- **Técnicas de optimización**:
  - Mixed precision training (FP16)
  - Gradient accumulation
  - Learning rate scheduling

#### 3.5 Evaluación
- **Métricas**:
  - **ROUGE-1**: Overlap de unigramas
  - **ROUGE-2**: Overlap de bigramas
  - **ROUGE-L**: Subsecuencia común más larga
  
- **Baseline**: Modelo sin fine-tuning
- **Modelo mejorado**: Después de fine-tuning

### 4. Resultados y Análisis (4-5 páginas)

#### 4.1 Resultados Cuantitativos

**Tabla 1: Métricas de Evaluación**

| Modelo | ROUGE-1 | ROUGE-2 | ROUGE-L | Tiempo |
|--------|---------|---------|---------|--------|
| Baseline (sin fine-tuning) | X.XX | X.XX | X.XX | Xs |
| Fine-tuned (1 época) | X.XX | X.XX | X.XX | Xs |
| Fine-tuned (3 épocas) | X.XX | X.XX | X.XX | Xs |

**Gráficas**:
- Evolución de loss durante entrenamiento
- Evolución de métricas ROUGE
- Comparación de modelos

#### 4.2 Resultados Cualitativos

**Ejemplos de resúmenes generados**:

```
Video 1: "Introducción a Redes Neuronales"
Transcripción (500 palabras): ...
Resumen generado (50 palabras): ...
Evaluación: [Analizar calidad, coherencia, información relevante]
```

#### 4.3 Análisis de Errores
- Casos donde el modelo funciona bien
- Casos de fallo (texto muy técnico, idioma mezclado, etc.)
- Limitaciones identificadas

### 5. Conclusiones (2 páginas)

- ✅ **Logros alcanzados**:
  - Sistema funcional de resumen de videos
  - Fine-tuning exitoso del modelo
  - Mejora en métricas ROUGE

- 📊 **Resultados principales**:
  - Mejora de X% en ROUGE-1
  - Reducción de texto en Y%
  - Tiempo de procesamiento: Z minutos/video

- 🔍 **Limitaciones**:
  - Depende de calidad del audio
  - Funciona mejor con ciertos tipos de videos
  - Requiere recursos computacionales

- 🚀 **Trabajo futuro**:
  - Probar con modelos más grandes (mT5-base, mT5-large)
  - Crear dataset personalizado con videos académicos
  - Implementar interfaz web
  - Agregar resumen por secciones del video
  - Integrar generación de subtítulos

### 6. Referencias

```
[1] Vaswani, A., et al. (2017). "Attention is All You Need"
[2] Raffel, C., et al. (2020). "Exploring the Limits of Transfer Learning with T5"
[3] Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper)
[4] Lin, C. Y. (2004). "ROUGE: A Package for Automatic Evaluation of Summaries"
[5] Xue, L., et al. (2021). "mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer"
```

## 📊 Componentes Evaluables

### 1. Componente Técnico (40%)
- ✅ Implementación correcta del pipeline
- ✅ Fine-tuning del modelo
- ✅ Uso de datasets apropiados
- ✅ Código limpio y documentado

### 2. Experimentación y Análisis (30%)
- ✅ Comparación de modelos
- ✅ Análisis de hiperparámetros
- ✅ Evaluación con métricas
- ✅ Visualización de resultados

### 3. Documentación (20%)
- ✅ Informe completo y bien estructurado
- ✅ Código comentado
- ✅ README con instrucciones claras
- ✅ Jupyter notebooks explicativos

### 4. Presentación (10%)
- ✅ Demo funcional
- ✅ Explicación clara de conceptos
- ✅ Respuesta a preguntas

## 🎨 Sugerencias para Destacar

### 1. Dataset Personalizado
Crea tu propio dataset con videos educativos:
```python
# Estructura
data/
  videos/
    clase1.mp4
    clase2.mp4
  transcripts/
    clase1_transcript.json
  summaries/
    clase1_summary.json (resumen manual para evaluación)
```

### 2. Comparación de Modelos
Compara múltiples modelos:
- mT5-small vs mT5-base
- T5 vs BART vs PEGASUS
- Con y sin fine-tuning

### 3. Análisis de Hiperparámetros
Experimenta con diferentes configuraciones:
- Learning rate: [1e-5, 5e-5, 1e-4]
- Batch size: [2, 4, 8]
- Épocas: [1, 3, 5]
- Max length: [64, 128, 256]

### 4. Interfaz Web (Bonus)
Crea una interfaz simple con Streamlit:
```python
import streamlit as st
from inference import VideoSummarizer

st.title("Resumidor de Videos Educativos")
video_file = st.file_uploader("Sube tu video")

if video_file:
    # Procesar y mostrar resumen
    summary = process_video(video_file)
    st.write(summary)
```

### 5. Análisis Cualitativo Profundo
- Coherencia del resumen
- Información relevante capturada
- Factualidad (sin alucinaciones)
- Longitud apropiada

## 📅 Cronograma Sugerido

**Semana 1-2**: Setup y Entendimiento
- ✅ Instalar dependencias
- ✅ Estudiar Transformers y T5
- ✅ Ejecutar notebook tutorial
- ✅ Probar con modelo base

**Semana 3-4**: Preparación de Datos
- ✅ Recolectar/seleccionar videos
- ✅ Transcribir con Whisper
- ✅ Preparar dataset de entrenamiento
- ✅ Análisis exploratorio

**Semana 5-6**: Entrenamiento
- ✅ Fine-tuning del modelo
- ✅ Experimentar con hiperparámetros
- ✅ Guardar mejores modelos
- ✅ Evaluar con métricas

**Semana 7-8**: Análisis y Documentación
- ✅ Analizar resultados
- ✅ Generar gráficas
- ✅ Escribir informe
- ✅ Preparar presentación

**Semana 9**: Finalización
- ✅ Revisar código
- ✅ Pulir documentación
- ✅ Preparar demo
- ✅ Ensayar presentación

## 🎓 Rúbrica de Evaluación (Ejemplo)

| Criterio | Excelente (4) | Bueno (3) | Regular (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------|------------------|
| Implementación | Sistema completo y funcional | Funciona con errores menores | Funciona parcialmente | No funciona |
| Fine-tuning | Modelo entrenado correctamente con mejoras medibles | Entrenado pero con mejoras mínimas | Intento de entrenamiento | No implementado |
| Dataset | Dataset apropiado y bien preparado | Dataset adecuado | Dataset inadecuado | Sin dataset |
| Evaluación | Múltiples métricas y análisis profundo | Métricas básicas | Evaluación superficial | Sin evaluación |
| Documentación | Completa y profesional | Buena pero incompleta | Básica | Deficiente |
| Código | Limpio, comentado y modular | Funcional pero mejorable | Desorganizado | Mal estructurado |

## 💡 Tips Finales

1. **Empieza simple**: Primero haz que funcione, luego optimiza
2. **Documenta todo**: Cada experimento, cada resultado
3. **Guarda checkpoints**: No pierdas horas de entrenamiento
4. **Usa Git**: Control de versiones desde el inicio
5. **Prueba frecuentemente**: No esperes al final para probar
6. **Pide feedback**: Muestra avances a tu profesor
7. **Tiempo para debugging**: Siempre hay errores inesperados
8. **Backup**: Guarda tu trabajo en la nube

## 📞 Recursos de Ayuda

- **Documentación oficial**:
  - Hugging Face: https://huggingface.co/docs
  - Whisper: https://github.com/openai/whisper
  
- **Tutoriales**:
  - Fine-tuning T5: https://huggingface.co/docs/transformers/tasks/summarization
  - ROUGE metrics: https://huggingface.co/spaces/evaluate-metric/rouge

- **Comunidad**:
  - Hugging Face Forum
  - Stack Overflow
  - Reddit r/MachineLearning

¡Éxito en tu proyecto! 🚀🎓
