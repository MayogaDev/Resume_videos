# 🎨 DIAGRAMAS VISUALES DEL FLUJO

## 📊 DIAGRAMA 1: Vista General del Sistema

```
╔══════════════════════════════════════════════════════════════╗
║                    TU PROYECTO COMPLETO                      ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────┐
│   TUS        │
│   VIDEOS     │  ← Tienes 5 videos de clases
│ 📹 📹 📹 📹 📹 │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  WHISPER (Modelo 1)                          │
│  Convierte: Audio → Texto                    │
│  🎵 → 📝                                      │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ TRANSCRIPCIÓN│
│              │  ← "En esta clase veremos redes neuronales..."
│ 📝 📝 📝 📝 📝 │
└──────┬───────┘
       │
       │   ┌─────────────────────────────────────┐
       │   │  DATASET PÚBLICO                    │
       │   │  5000 pares [texto, resumen]        │
       │   │  📊 📊 📊 📊 📊                       │
       │   └──────┬──────────────────────────────┘
       │          │
       └──────────┼───────────► JUNTAR
                  │
                  ▼
       ┌──────────────────────────┐
       │  T5/mT5 BASE             │
       │  (Modelo 2 - Sin Entrenar)│
       │  🧠                       │
       └──────┬───────────────────┘
              │
              ▼
       ┌──────────────────────────┐
       │  ENTRENAMIENTO           │
       │  (Fine-tuning)           │
       │  🏋️ 🏋️ 🏋️               │
       │  3 horas                 │
       └──────┬───────────────────┘
              │
              ▼
       ┌──────────────────────────┐
       │  T5/mT5 ENTRENADO        │
       │  (Modelo 2 - Especialista)│
       │  ✅ 🧠                   │
       └──────┬───────────────────┘
              │
              ▼
       ┌──────────────────────────┐
       │  NUEVA TRANSCRIPCIÓN     │
       │  📝 "El deep learning..." │
       └──────┬───────────────────┘
              │
              ▼
       ┌──────────────────────────┐
       │  RESUMEN GENERADO        │
       │  📄 "Deep learning usa..." │
       └──────────────────────────┘
```

---

## 📊 DIAGRAMA 2: Proceso de Entrenamiento Detallado

```
╔══════════════════════════════════════════════════════════════╗
║              CÓMO APRENDE EL MODELO (FINE-TUNING)            ║
╚══════════════════════════════════════════════════════════════╝

ANTES DEL ENTRENAMIENTO:
════════════════════════════════════════════════════════════════

    Modelo T5 Base
    ┌─────────────────────────────────────┐
    │  Sabe lenguaje general              │
    │  Pero NO sabe resumir bien          │
    │  🧠 (cerebro básico)                │
    └─────────────────────────────────────┘

    Texto: "Las redes neuronales son modelos inspirados..."
           ↓
    Resumen generado: "redes modelos" ❌ MALO


DURANTE EL ENTRENAMIENTO:
════════════════════════════════════════════════════════════════

    Iteración 1:
    ────────────
    📊 Dataset ejemplo 1:
       Input: "Las redes neuronales son modelos..."
       Target: "Las redes neuronales imitan el cerebro"
    
    🧠 Modelo intenta:
       Output: "redes modelos"
    
    ❌ Comparación:
       Target:  "Las redes neuronales imitan el cerebro"
       Output:  "redes modelos"
       Error:   ALTO (muy diferente)
    
    🔧 Ajuste:
       Modifica pesos internos
       Loss: 2.5
    
    ────────────────────────────────────────────────────────
    
    Iteración 100:
    ──────────────
    📊 Dataset ejemplo 100:
       Input: "El machine learning permite..."
       Target: "Machine learning aprende de datos"
    
    🧠 Modelo intenta:
       Output: "Machine learning datos"
    
    ⚠️ Comparación:
       Target:  "Machine learning aprende de datos"
       Output:  "Machine learning datos"
       Error:   MEDIO (casi bien)
    
    🔧 Ajuste:
       Modifica pesos un poco
       Loss: 1.8
    
    ────────────────────────────────────────────────────────
    
    Iteración 500:
    ──────────────
    📊 Dataset ejemplo 500:
       Input: "Las redes neuronales son modelos..."
       Target: "Las redes neuronales imitan el cerebro"
    
    🧠 Modelo intenta:
       Output: "Las redes neuronales imitan el cerebro"
    
    ✅ Comparación:
       Target:  "Las redes neuronales imitan el cerebro"
       Output:  "Las redes neuronales imitan el cerebro"
       Error:   BAJO (casi perfecto!)
    
    🔧 Ajuste:
       Ajuste mínimo
       Loss: 0.8


DESPUÉS DEL ENTRENAMIENTO:
════════════════════════════════════════════════════════════════

    Modelo T5 Fine-tuned
    ┌─────────────────────────────────────┐
    │  Sabe lenguaje general              │
    │  + Especialista en resumir          │
    │  ✅ 🧠 (cerebro experto)            │
    └─────────────────────────────────────┘

    Texto: "Las redes neuronales son modelos inspirados..."
           ↓
    Resumen generado: "Las redes neuronales imitan el cerebro" ✅ BUENO
```

---

## 📊 DIAGRAMA 3: ¿Qué es un Dataset?

```
╔══════════════════════════════════════════════════════════════╗
║                ESTRUCTURA DE UN DATASET                      ║
╚══════════════════════════════════════════════════════════════╝

Dataset XSum (5000 ejemplos):

┌─────────────────────────────────────────────────────────────┐
│  Ejemplo #1                                                 │
├─────────────────────────────────────────────────────────────┤
│  document (texto largo):                                    │
│  "The full cost of damage in Newton Stewart, one of the     │
│   areas worst affected, is still being assessed. Repair     │
│   work is ongoing in Hawick and many roads in Peeblesshire  │
│   remain badly affected by standing water..."               │
│                                                             │
│  summary (resumen correcto):                                │
│  "Clean-up operations are continuing across the Scottish    │
│   Borders after flooding caused by Storm Frank."            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Ejemplo #2                                                 │
├─────────────────────────────────────────────────────────────┤
│  document (texto largo):                                    │
│  "A fire alarm went off at the Holiday Inn in Hope Street   │
│   at about 04:20 BST on Saturday and guests were asked to   │
│   leave the hotel. Two men, aged 35 and 36, were arrested   │
│   outside the hotel..."                                     │
│                                                             │
│  summary (resumen correcto):                                │
│  "Two men have been arrested after a city centre hotel was  │
│   evacuated in a security alert."                           │
└─────────────────────────────────────────────────────────────┘

... (4998 ejemplos más) ...


DIVISIÓN DEL DATASET:
═══════════════════════════════════════════════════════════════

Total: 5000 ejemplos

├─ TRAIN (70%): 3500 ejemplos
│  └─ Usado para entrenar el modelo
│
├─ VALIDATION (15%): 750 ejemplos
│  └─ Usado para validar durante entrenamiento
│  └─ Detectar si el modelo está aprendiendo bien
│
└─ TEST (15%): 750 ejemplos
   └─ Usado para evaluar al final
   └─ Medir qué tan bien funciona el modelo
```

---

## 📊 DIAGRAMA 4: Tokenización Explicada

```
╔══════════════════════════════════════════════════════════════╗
║          ¿POR QUÉ CONVERTIR TEXTO A NÚMEROS?                 ║
╚══════════════════════════════════════════════════════════════╝

PROBLEMA:
─────────
Los modelos de IA solo entienden números, no texto.


SOLUCIÓN: TOKENIZACIÓN
────────────────────────

PASO 1: Texto original
───────────────────────
"Las redes neuronales aprenden patrones"


PASO 2: Dividir en tokens (palabras/subpalabras)
─────────────────────────────────────────────────
["Las", "redes", "neuronales", "aprenden", "patrones"]


PASO 3: Convertir cada token a un número (ID)
──────────────────────────────────────────────
Vocabulario del modelo:
  "Las"         → 345
  "redes"       → 1234
  "neuronales"  → 5678
  "aprenden"    → 2345
  "patrones"    → 6789


PASO 4: Secuencia de números
─────────────────────────────
[345, 1234, 5678, 2345, 6789]

         ↓

PASO 5: El modelo procesa estos números
────────────────────────────────────────
🧠 Modelo: [345, 1234, 5678, 2345, 6789]
           ↓ (procesamiento interno)
           ↓
     [89, 234, 567, 890]


PASO 6: Convertir números de vuelta a texto (Detokenización)
─────────────────────────────────────────────────────────────
[89, 234, 567, 890] → ["Las", "redes", "aprenden", "patrones"]
                    → "Las redes aprenden patrones"


RESULTADO FINAL:
────────────────
Input:  "Las redes neuronales aprenden patrones"
Output: "Las redes aprenden patrones" ✅
```

---

## 📊 DIAGRAMA 5: Comparación Modelo Base vs Fine-tuned

```
╔══════════════════════════════════════════════════════════════╗
║       ANTES Y DESPUÉS DEL FINE-TUNING (COMPARACIÓN)          ║
╚══════════════════════════════════════════════════════════════╝


MODELO BASE (Sin Fine-tuning):
═══════════════════════════════════════════════════════════════

    🧠 T5 Base
    └─ Entrenado por Google con millones de textos
    └─ Sabe gramática, vocabulario, estructura
    └─ PERO no especializado en resumir

    Prueba 1:
    ─────────
    Input:  "Las redes neuronales son modelos computacionales..."
    Output: "redes neuronales modelos"
    Calidad: ⭐⭐ (2/5) - Malo
    
    Prueba 2:
    ─────────
    Input:  "El machine learning es una rama de la IA..."
    Output: "machine learning IA"
    Calidad: ⭐⭐ (2/5) - Malo
    
    ROUGE-1: 0.15 ❌


DESPUÉS DE FINE-TUNING:
═══════════════════════════════════════════════════════════════

    ✅ 🧠 T5 Fine-tuned
    └─ Entrenado por Google (base)
    └─ + Entrenado por TI con 5000 ejemplos
    └─ Especialista en resumir

    Prueba 1:
    ─────────
    Input:  "Las redes neuronales son modelos computacionales..."
    Output: "Las redes neuronales son modelos que imitan el cerebro"
    Calidad: ⭐⭐⭐⭐⭐ (5/5) - Excelente
    
    Prueba 2:
    ─────────
    Input:  "El machine learning es una rama de la IA..."
    Output: "Machine learning permite aprender de datos automáticamente"
    Calidad: ⭐⭐⭐⭐ (4/5) - Muy Bueno
    
    ROUGE-1: 0.45 ✅


MEJORA:
═══════════════════════════════════════════════════════════════

    Calidad:    ⭐⭐ → ⭐⭐⭐⭐⭐
    ROUGE-1:    0.15 → 0.45 (3x mejor)
    Utilidad:   ❌ → ✅
```

---

## 📊 DIAGRAMA 6: Timeline del Proyecto

```
╔══════════════════════════════════════════════════════════════╗
║              LÍNEA DE TIEMPO COMPLETA                        ║
╚══════════════════════════════════════════════════════════════╝

DÍA 1: Preparación (30 min)
═══════════════════════════════════════════════════════════════
⏰ 00:00 - Instalar dependencias
           pip install -r requirements.txt
           
⏰ 00:15 - Verificar instalación
           python check_installation.py
           
⏰ 00:30 ✅ Listo para empezar


DÍA 2-3: Transcripción (2 horas)
═══════════════════════════════════════════════════════════════
⏰ 00:00 - Preparar videos
           Coloca 5 videos en carpeta videos/
           
⏰ 00:30 - Transcribir con Whisper
           python src/transcribe_video.py
           
⏰ 02:00 ✅ 5 transcripciones listas


DÍA 4: Preparar Dataset (1 hora)
═══════════════════════════════════════════════════════════════
⏰ 00:00 - Descargar dataset público
           Dataset XSum descargando...
           
⏰ 00:30 - Tokenizar
           Procesando 5000 ejemplos...
           
⏰ 01:00 ✅ Dataset tokenizado guardado


DÍA 5-6: Entrenamiento (3-4 horas)
═══════════════════════════════════════════════════════════════
⏰ 00:00 - Iniciar entrenamiento
           python src/train_model.py
           
⏰ 01:00 - Step 100/3000 | Loss: 2.3
⏰ 02:00 - Step 1000/3000 | Loss: 1.5
⏰ 03:00 - Step 2000/3000 | Loss: 1.1
⏰ 04:00 - Step 3000/3000 | Loss: 0.9
           
⏰ 04:00 ✅ Modelo entrenado guardado


DÍA 7: Evaluación y Pruebas (1 hora)
═══════════════════════════════════════════════════════════════
⏰ 00:00 - Evaluar modelo
           ROUGE-1: 0.45 ✅
           
⏰ 00:30 - Probar con nuevos textos
           Generando resúmenes...
           
⏰ 01:00 ✅ Sistema funcionando


DÍA 8-10: Documentación (variable)
═══════════════════════════════════════════════════════════════
⏰ Escribir informe
⏰ Crear presentación
⏰ Preparar demo

✅ PROYECTO COMPLETO
```

---

## 🔑 CONCEPTOS CLAVE RESUMIDOS

```
╔══════════════════════════════════════════════════════════════╗
║                 GLOSARIO DE TÉRMINOS                         ║
╚══════════════════════════════════════════════════════════════╝

📝 WHISPER
   └─ Modelo de OpenAI
   └─ Convierte audio → texto
   └─ Ya está entrenado, solo usarlo

🧠 T5/mT5
   └─ Modelo de Google
   └─ Convierte texto largo → texto corto
   └─ Necesita fine-tuning para tu tarea

📊 DATASET
   └─ Colección de ejemplos
   └─ Cada ejemplo: [input, output esperado]
   └─ Usado para enseñar al modelo

🔤 TOKENIZACIÓN
   └─ Convertir texto → números
   └─ Los modelos solo entienden números
   └─ Reversible: números → texto

🏋️ FINE-TUNING
   └─ Especializar un modelo pre-entrenado
   └─ Entrenar con dataset específico
   └─ Modelo aprende tu tarea particular

📈 MÉTRICAS (ROUGE)
   └─ Miden calidad de resúmenes
   └─ Comparan con resúmenes correctos
   └─ Valores 0-1 (más alto = mejor)

🔧 TRANSFER LEARNING
   └─ Usar conocimiento previo del modelo
   └─ Modelo ya sabe lenguaje general
   └─ Solo ajustar para tarea específica

💾 CHECKPOINT
   └─ Guardado del modelo durante entrenamiento
   └─ Permite reanudar si se interrumpe
   └─ Se guarda cada N pasos

🎯 INFERENCIA
   └─ Usar el modelo entrenado
   └─ Dar input nuevo → obtener output
   └─ Es la "aplicación" del modelo
```

---

**¿Todo más claro ahora? 🎓**
