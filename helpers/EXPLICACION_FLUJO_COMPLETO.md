# 🎓 EXPLICACIÓN COMPLETA: Cómo Funciona Todo el Sistema

## 📚 CONCEPTOS BÁSICOS PRIMERO

### ¿Qué es un Dataset?
Un **dataset** es como una **base de datos de ejemplos** que le enseñas a tu modelo.

**Ejemplo de un dataset de resumen:**
```
Ejemplo 1:
  - Texto original: "Las redes neuronales son modelos inspirados en el cerebro humano..."
  - Resumen correcto: "Las redes neuronales imitan el cerebro humano."

Ejemplo 2:
  - Texto original: "El machine learning permite a las computadoras aprender..."
  - Resumen correcto: "Machine learning permite aprender de datos."

... (miles de ejemplos más)
```

### ¿Qué es un Modelo?
Un **modelo** es como un **cerebro artificial** que aprende patrones de los ejemplos.

**Tipos de modelos en este proyecto:**

1. **Whisper** - Convierte audio → texto
2. **T5/mT5** - Convierte texto largo → texto corto (resumen)

---

## 🔄 FLUJO COMPLETO DEL SISTEMA (DE PRINCIPIO A FIN)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO                           │
└─────────────────────────────────────────────────────────────┘

FASE 1: PREPARACIÓN
─────────────────────────────────────────────────────────────
📹 Video educativo (mi_clase.mp4)
    ↓
🎵 Whisper extrae el audio
    ↓
📝 Whisper transcribe: "En esta clase veremos..."
    ↓
💾 Se guarda: mi_clase_transcript.json


FASE 2: OBTENER DATASET DE ENTRENAMIENTO
─────────────────────────────────────────────────────────────
Opción A: Dataset Público (más fácil)
    📥 Descargar XSum/MLSUM
    ↓
    Ya tiene miles de pares: [texto, resumen]

Opción B: Tu propio dataset
    📝 Tus transcripciones
    ↓
    ✍️ Crear resúmenes manualmente
    ↓
    Formar pares: [transcripción, resumen]


FASE 3: PREPARAR LOS DATOS
─────────────────────────────────────────────────────────────
📊 Dataset con 5000 ejemplos:
    [texto1, resumen1]
    [texto2, resumen2]
    ...
    [texto5000, resumen5000]
    ↓
🔤 Tokenización (convertir palabras a números)
    "Las redes neuronales" → [345, 1234, 5678]
    ↓
📦 Dataset tokenizado listo


FASE 4: ENTRENAMIENTO (FINE-TUNING)
─────────────────────────────────────────────────────────────
🧠 Modelo T5 Pre-entrenado (ya sabe lenguaje general)
    ↓
📚 Le mostramos nuestro dataset
    ↓
🏋️ Modelo practica:
    - Ve texto1 → intenta crear resumen1
    - Compara su resumen con el resumen1 correcto
    - Ajusta sus "neuronas" para hacerlo mejor
    - Repite con texto2, texto3... miles de veces
    ↓
✅ Modelo Fine-tuned (ahora es especialista en resumir)


FASE 5: USAR EL MODELO ENTRENADO
─────────────────────────────────────────────────────────────
📝 Nueva transcripción: "El deep learning utiliza..."
    ↓
🧠 Modelo entrenado procesa
    ↓
📄 Resumen generado: "Deep learning usa redes profundas"
```

---

## 🎯 EXPLICACIÓN DETALLADA PASO POR PASO

### 📍 PASO 1: ¿De dónde viene el video?

```
TÚ tienes:
📹 video1.mp4 - Clase sobre redes neuronales (10 minutos)
📹 video2.mp4 - Clase sobre machine learning (15 minutos)
📹 video3.mp4 - Clase sobre deep learning (12 minutos)
```

---

### 📍 PASO 2: Convertir video a texto (Whisper)

```python
from transcribe_video import VideoTranscriber

transcriber = VideoTranscriber(model_size="base", language="es")
transcript = transcriber.transcribe_video("video1.mp4")
```

**¿Qué hace Whisper?**
```
📹 video1.mp4 (audio: "Hola, hoy veremos redes neuronales...")
           ↓
    🎧 Whisper escucha
           ↓
📝 Texto: "Hola, hoy veremos redes neuronales. Las redes 
           neuronales son modelos inspirados en el cerebro
           humano que pueden aprender patrones de datos..."

💾 Se guarda en: video1_transcript.json
```

**Resultado:**
```json
{
  "text": "Hola, hoy veremos redes neuronales. Las redes neuronales son modelos...",
  "language": "es",
  "duration": 600.5
}
```

---

### 📍 PASO 3: Obtener un Dataset para entrenar

Ahora necesitas un **dataset** = miles de ejemplos para enseñarle al modelo.

#### **Opción A: Dataset Público (RECOMENDADO para empezar)**

```python
from prepare_dataset import DatasetPreparator

preparator = DatasetPreparator(model_name="google/mt5-small")

# Descargar dataset XSum (noticias BBC con resúmenes)
dataset = preparator.load_public_dataset(
    dataset_name="xsum",
    language="en",
    num_samples=5000
)
```

**¿Qué contiene el dataset XSum?**
```
Dataset XSum:
┌─────────────────────────────────────────────────────────┐
│ Ejemplo 1:                                              │
│   document: "The BBC's Andrew Marr show featured..."    │
│   summary: "BBC show discusses politics."               │
├─────────────────────────────────────────────────────────┤
│ Ejemplo 2:                                              │
│   document: "Scientists have discovered a new..."       │
│   summary: "New species discovered in Amazon."          │
├─────────────────────────────────────────────────────────┤
│ ... 5000 ejemplos más ...                               │
└─────────────────────────────────────────────────────────┘

Dividido en:
  - train: 3500 ejemplos (para entrenar)
  - validation: 750 ejemplos (para validar durante entrenamiento)
  - test: 750 ejemplos (para probar al final)
```

#### **Opción B: Tu Propio Dataset**

```python
# TUS DATOS:
datos = [
    {
        "document": "Transcripción completa de video1...",
        "summary": "Resumen que TÚ escribiste manualmente"
    },
    {
        "document": "Transcripción completa de video2...",
        "summary": "Resumen que TÚ escribiste manualmente"
    },
    # ... más ejemplos
]
```

---

### 📍 PASO 4: Preparar el Dataset (Tokenización)

**¿Por qué tokenizar?**
Los modelos no entienden palabras, solo números.

```python
tokenized_dataset = preparator.prepare_dataset(dataset)
```

**¿Qué hace la tokenización?**
```
ANTES (texto):
"Las redes neuronales aprenden patrones"

           ↓ TOKENIZACIÓN ↓

DESPUÉS (números):
[345, 1234, 5678, 2345, 6789]

Cada número representa una palabra o parte de palabra.
```

**Ejemplo completo:**
```python
# Original
texto = "resumir: Las redes neuronales son modelos inspirados en el cerebro"
resumen = "Las redes neuronales imitan el cerebro"

# Tokenizado
input_ids = [23, 345, 1234, 5678, 234, 567, ...]  # Texto
labels = [345, 1234, 5678, 2134, ...]             # Resumen
```

---

### 📍 PASO 5: Entrenar el Modelo (FINE-TUNING)

**¿Qué es Transfer Learning?**
```
🧠 Modelo T5 Pre-entrenado:
   Ya fue entrenado por Google con MILLONES de textos
   Ya sabe:
   - Gramática
   - Vocabulario
   - Estructura del lenguaje
   
   PERO NO SABE hacer resúmenes específicos de tu dominio
```

**¿Qué es Fine-tuning?**
```
🎓 Fine-tuning = "Especialización"

Tomas el modelo pre-entrenado y le enseñas tu tarea específica:

1. Le muestras ejemplos de TU dataset
2. El modelo ajusta sus "pesos" (neuronas)
3. Se vuelve especialista en resumir
```

**Proceso de entrenamiento:**
```python
from train_model import SummaryTrainer

trainer = SummaryTrainer(
    model_name="google/mt5-small",  # Modelo pre-entrenado
    output_dir="../models/mi-modelo"
)

trainer.train(
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    num_train_epochs=3,
    batch_size=4
)
```

**¿Qué pasa durante el entrenamiento?**
```
ITERACIÓN 1:
─────────────────────────────────────
📝 Input: "Las redes neuronales son modelos..."
🧠 Modelo intenta: "redes modelos"
✅ Correcto: "Las redes neuronales imitan el cerebro"
❌ Error detectado: "redes modelos" ≠ "Las redes neuronales imitan el cerebro"
🔧 Ajusta sus pesos para mejorar

ITERACIÓN 2:
─────────────────────────────────────
📝 Input: "El machine learning permite..."
🧠 Modelo intenta: "Machine learning aprende datos"
✅ Correcto: "Machine learning permite aprender de datos"
📊 Error menor, está mejorando
🔧 Ajusta sus pesos un poco más

... (miles de iteraciones) ...

ITERACIÓN 5000:
─────────────────────────────────────
📝 Input: "Las redes neuronales son modelos..."
🧠 Modelo intenta: "Las redes neuronales imitan el cerebro"
✅ Correcto: "Las redes neuronales imitan el cerebro"
🎉 ¡Casi perfecto!
```

**Métricas durante entrenamiento:**
```
Step 100: Loss: 2.345 (alto = malo)
Step 200: Loss: 1.987 (bajando = bueno ✅)
Step 300: Loss: 1.756 (sigue bajando ✅)
...
Step 500: Loss: 0.856 (bajo = excelente ✅)

ROUGE-1: 0.45 (cuánto coincide con resumen correcto)
```

---

### 📍 PASO 6: Modelo Entrenado Guardado

```
Después del entrenamiento, tienes:

📁 models/mi-modelo/
   ├── pytorch_model.bin       # Cerebro del modelo (pesos)
   ├── config.json              # Configuración
   ├── tokenizer_config.json    # Cómo tokenizar
   └── training_args.bin        # Argumentos usados

Este modelo YA SABE resumir textos similares a tu dataset
```

---

### 📍 PASO 7: Usar el Modelo (Inferencia)

Ahora puedes usar tu modelo entrenado para resumir NUEVOS textos:

```python
from inference import VideoSummarizer

# Cargar modelo entrenado
summarizer = VideoSummarizer(model_path="../models/mi-modelo")

# Transcripción NUEVA de un video
texto_nuevo = """
En esta clase aprenderemos sobre el aprendizaje profundo.
El aprendizaje profundo es una técnica de machine learning
que utiliza redes neuronales con múltiples capas ocultas.
Estas redes pueden aprender representaciones jerárquicas
de los datos de manera automática sin necesidad de
ingeniería manual de características.
"""

# Generar resumen
resumen = summarizer.summarize(texto_nuevo)
print(resumen)
# Output: "El aprendizaje profundo usa redes neuronales
#          multicapa para aprender de datos automáticamente."
```

---

## 🔍 COMPARACIÓN: ANTES vs DESPUÉS del Fine-tuning

### SIN Fine-tuning (Modelo Base):
```python
modelo_base = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-small")

texto = "Las redes neuronales artificiales son modelos..."
resumen = modelo_base.generate(...)
# Output: "redes neuronales modelos"  ❌ Malo
```

### CON Fine-tuning (Tu Modelo):
```python
modelo_tuneado = VideoSummarizer(model_path="mi-modelo")

texto = "Las redes neuronales artificiales son modelos..."
resumen = modelo_tuneado.summarize(texto)
# Output: "Las redes neuronales son modelos inspirados 
#          en el cerebro que aprenden de datos"  ✅ Bueno
```

---

## 📊 FLUJO DE DATOS VISUAL

```
┌─────────────────────────────────────────────────────────────┐
│                     DATOS                                    │
└─────────────────────────────────────────────────────────────┘

1. VIDEO
   📹 mi_video.mp4 (binario)

2. AUDIO
   🎵 audio extraído (WAV)

3. TRANSCRIPCIÓN
   📝 "En esta clase veremos redes neuronales..." (texto)

4. DATASET
   📊 5000 pares [texto, resumen] (estructura)

5. DATASET TOKENIZADO
   🔢 [[345, 1234, ...], [23, 456, ...]] (números)

6. MODELO BASE
   🧠 T5 pre-entrenado (pesos iniciales)

7. ENTRENAMIENTO
   🏋️ Ajustar pesos con dataset (proceso)

8. MODELO ENTRENADO
   ✅ Modelo fine-tuned (pesos ajustados)

9. INFERENCIA
   📄 Nuevo texto → Resumen (aplicación)
```

---

## 🎯 ANALOGÍA PARA ENTENDER MEJOR

**Imagina que enseñas a alguien a resumir:**

### Paso 1: Enseñar conceptos básicos (Pre-entrenamiento)
```
👨‍🎓 Estudiante aprende:
   - Leer
   - Escribir
   - Gramática
   - Vocabulario
   
Esto es como el modelo T5 pre-entrenado.
Ya sabe lenguaje, pero NO sabe resumir.
```

### Paso 2: Enseñar a resumir (Fine-tuning)
```
📚 Le das 5000 ejemplos:
   
   Ejemplo 1:
   📄 Texto: "Había una vez un reino lejano donde..."
   ✅ Resumen correcto: "Cuento de un reino mágico"
   
   Ejemplo 2:
   📄 Texto: "Las proteínas son moléculas..."
   ✅ Resumen correcto: "Las proteínas son moléculas esenciales"
   
   ... más ejemplos ...

👨‍🎓 Estudiante practica y mejora en resumir
```

### Paso 3: Evaluar (Validación)
```
📝 Le das un texto NUEVO:
   "El cambio climático afecta al planeta..."

👨‍🎓 Estudiante resume:
   "El cambio climático afecta al planeta"

👍 ¡Bien hecho! Aprendió a resumir.
```

---

## 🧮 ¿POR QUÉ NECESITAS TANTOS EJEMPLOS?

```
Con 10 ejemplos:
❌ Modelo memoriza, no aprende patrones

Con 100 ejemplos:
⚠️ Modelo aprende poco, resúmenes mediocres

Con 1,000 ejemplos:
✅ Modelo empieza a generalizar bien

Con 5,000+ ejemplos:
✅✅ Modelo aprende patrones robustos

Con 50,000+ ejemplos:
🏆 Modelo produce resúmenes excelentes
```

---

## 🔄 CICLO COMPLETO EN CÓDIGO

```python
# ============================================
# FLUJO COMPLETO EN 6 PASOS
# ============================================

# PASO 1: Transcribir video
from transcribe_video import VideoTranscriber
transcriber = VideoTranscriber()
transcript = transcriber.transcribe_video("video.mp4")
# Result: "En esta clase veremos..."

# PASO 2: Obtener dataset
from prepare_dataset import DatasetPreparator
preparator = DatasetPreparator()
dataset = preparator.load_public_dataset("xsum", "en", 5000)
# Result: 5000 pares [texto, resumen]

# PASO 3: Tokenizar
tokenized = preparator.prepare_dataset(dataset)
# Result: Números en lugar de palabras

# PASO 4: Entrenar
from train_model import SummaryTrainer
trainer = SummaryTrainer(model_name="google/mt5-small")
trainer.train(tokenized["train"], tokenized["validation"])
# Result: Modelo ajustado guardado

# PASO 5: Cargar modelo entrenado
from inference import VideoSummarizer
summarizer = VideoSummarizer("../models/mi-modelo")
# Result: Modelo listo para usar

# PASO 6: Resumir nuevo texto
resumen = summarizer.summarize(transcript['text'])
# Result: "Clase sobre redes neuronales"
```

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Por qué necesito un dataset si ya tengo Whisper?**
```
R: Whisper solo transcribe (audio → texto)
   NO resume (texto largo → texto corto)
   
   Para resumir necesitas OTRO modelo (T5)
   Y ese modelo T5 necesita APRENDER a resumir
   con ejemplos = DATASET
```

**P: ¿No puedo usar T5 directamente sin entrenar?**
```
R: Sí puedes, pero hará resúmenes MALOS:
   
   Modelo base sin fine-tuning:
   "redes neuronales" ❌
   
   Modelo con fine-tuning:
   "Las redes neuronales son modelos que imitan el cerebro" ✅
```

**P: ¿Cuánto tiempo toma entrenar?**
```
R: Depende:
   - CPU: 2-4 horas (más lento)
   - GPU: 20-40 minutos (más rápido)
   
   Con 500 pasos (prueba): 10-20 minutos
   Con dataset completo: 2-4 horas
```

**P: ¿Qué modelo usar?**
```
R: Para ESPAÑOL: google/mt5-small o mt5-base
   Para INGLÉS: t5-small o t5-base
   
   small = más rápido, calidad OK
   base = más lento, mejor calidad
```

---

## ✅ RESUMEN DEL FLUJO

```
1. VIDEO → Whisper → TEXTO (transcripción)
           ↓
2. DATASET (5000 ejemplos texto-resumen)
           ↓
3. TOKENIZAR (convertir palabras a números)
           ↓
4. ENTRENAR (fine-tuning del modelo T5)
           ↓
5. MODELO ENTRENADO (guardado en disco)
           ↓
6. INFERENCIA (usar modelo para nuevos textos)
```

**Modelos usados:**
- **Whisper**: Audio → Texto
- **T5/mT5**: Texto largo → Texto corto (después de fine-tuning)

**¿Por qué fine-tuning?**
- Modelo base: resúmenes genéricos ❌
- Modelo fine-tuned: resúmenes especializados ✅

**¿Qué es el dataset?**
- Colección de ejemplos para enseñar al modelo
- Cada ejemplo: [texto_largo, resumen_correcto]
- Más ejemplos = modelo más inteligente

---

¿Quedó más claro? 🎓
