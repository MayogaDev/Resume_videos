# 🎓 TUTORIAL: Cómo Entrenar Tu Modelo Paso a Paso

## 📍 ESTÁS AQUÍ - Guía Visual Completa

Este tutorial te guiará **paso a paso** desde cero hasta tener tu modelo entrenado.

---

## ⏱️ TIEMPO ESTIMADO TOTAL: 30-60 minutos

---

## 🚀 MÉTODO RÁPIDO (Recomendado para empezar)

### ✅ PASO 1: Abrir Terminal (1 min)

```powershell
# En VS Code, abre una nueva terminal (Ctrl + `)
# Navega a la carpeta del proyecto
cd "d:\UNSA\UNSA\X SEMESTRE\Trabajo Interdisciplinar III\Resume videos - proyect"
```

---

### ✅ PASO 2: Activar Entorno Virtual (1 min)

```powershell
# Si aún no lo has creado
python -m venv venv

# Activar
.\venv\Scripts\Activate.ps1

# Deberías ver (venv) al inicio de tu línea de comando
```

---

### ✅ PASO 3: Verificar Instalación (2 min)

```powershell
# Verificar que todo está instalado
python check_installation.py

# Deberías ver todos los ✅ verdes
# Si hay errores ❌, instala las dependencias:
pip install -r requirements.txt
```

---

### ✅ PASO 4: Ejecutar Script de Entrenamiento (20-40 min)

```powershell
# Ir a la carpeta src
cd src

# Ejecutar entrenamiento automático
python entrenar_completo.py --rapido
```

**¿Qué hace este comando?**
1. 📥 Descarga dataset XSum (5000 ejemplos)
2. 🔄 Tokeniza y prepara los datos
3. 🏋️ Entrena el modelo (500 pasos)
4. 💾 Guarda el modelo entrenado

**Mientras entrena verás:**
```
Step 100: Loss: 2.345, ROUGE-1: 0.234
Step 200: Loss: 1.987, ROUGE-1: 0.267
Step 300: Loss: 1.756, ROUGE-1: 0.289
...
```

---

### ✅ PASO 5: Probar el Modelo Entrenado (5 min)

```powershell
# Abrir Python
python
```

```python
from inference import VideoSummarizer

# Cargar tu modelo entrenado
summarizer = VideoSummarizer(model_path="../models/mt5-video-summarizer")

# Probar con un texto
texto = """
En este video explicaremos las redes neuronales artificiales.
Las redes neuronales son modelos inspirados en el cerebro humano.
Están compuestas por capas de neuronas que procesan información.
Durante el entrenamiento, la red ajusta sus pesos para minimizar errores.
Las redes neuronales se usan en reconocimiento de imágenes y lenguaje natural.
"""

resumen = summarizer.summarize(texto)
print(f"Resumen: {resumen}")
```

---

## 🎯 MÉTODO DETALLADO (Para entender cada paso)

### PASO 1: Preparar el Dataset

```powershell
cd src
python
```

```python
from prepare_dataset import DatasetPreparator

# Crear preparador
preparator = DatasetPreparator(model_name="google/mt5-small")

# Descargar dataset
print("Descargando dataset XSum (esto puede tomar 5-10 minutos)...")
dataset = preparator.load_public_dataset(
    dataset_name="xsum",
    language="en",
    num_samples=5000
)

print(f"Dataset cargado: {len(dataset['train'])} ejemplos")

# Ver un ejemplo
ejemplo = dataset['train'][0]
print(f"\nDocumento: {ejemplo['document'][:200]}...")
print(f"Resumen: {ejemplo['summary']}")
```

---

### PASO 2: Tokenizar el Dataset

```python
# Tokenizar (esto toma 5-10 minutos)
print("Tokenizando dataset...")
tokenized_dataset = preparator.prepare_dataset(dataset)

# Guardar
preparator.save_dataset(tokenized_dataset, "../data/processed/xsum_tokenized")
print("✅ Dataset listo para entrenar!")
```

---

### PASO 3: Entrenar el Modelo

```python
from train_model import SummaryTrainer

# Crear entrenador
trainer = SummaryTrainer(
    model_name="google/mt5-small",
    output_dir="../models/mt5-video-summarizer"
)

# Entrenar (esto toma 15-30 minutos)
print("Iniciando entrenamiento...")
trainer.train(
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    num_train_epochs=1,
    batch_size=4,
    learning_rate=5e-5,
    max_steps=500,  # Solo 500 pasos para prueba
    save_steps=100,
    eval_steps=100
)

print("✅ Modelo entrenado!")
```

---

### PASO 4: Evaluar el Modelo

```python
# Evaluar en test set
if "test" in tokenized_dataset:
    metrics = trainer.evaluate(tokenized_dataset["test"])
    
    print("\n📊 Métricas en Test Set:")
    print(f"   ROUGE-1: {metrics['eval_rouge1']:.4f}")
    print(f"   ROUGE-2: {metrics['eval_rouge2']:.4f}")
    print(f"   ROUGE-L: {metrics['eval_rougeL']:.4f}")
```

---

## 📊 ENTENDER LOS RESULTADOS

### ¿Qué significa cada métrica?

**ROUGE-1** (0.0 - 1.0)
- Mide overlap de palabras individuales
- > 0.30 = Bueno
- > 0.40 = Muy bueno
- > 0.50 = Excelente

**ROUGE-2** (0.0 - 1.0)
- Mide overlap de pares de palabras
- > 0.15 = Bueno
- > 0.20 = Muy bueno
- > 0.30 = Excelente

**ROUGE-L** (0.0 - 1.0)
- Mide secuencias comunes más largas
- > 0.25 = Bueno
- > 0.35 = Muy bueno
- > 0.45 = Excelente

**Loss** (valor numérico)
- Debe bajar durante el entrenamiento
- Inicio: 2-3
- Final: 0.5-1.5 (depende del dataset)

---

## 🎯 OPCIONES DE DATASETS

### Para ESPAÑOL:

```python
# MLSUM - Noticias en español
dataset = preparator.load_public_dataset(
    dataset_name="mlsum",
    language="es",
    num_samples=5000
)
```

### Para INGLÉS:

```python
# XSum - Noticias BBC (resúmenes cortos)
dataset = preparator.load_public_dataset(
    dataset_name="xsum",
    language="en",
    num_samples=5000
)

# CNN/DailyMail - Noticias (resúmenes más largos)
dataset = preparator.load_public_dataset(
    dataset_name="cnn_dailymail",
    language="en",
    num_samples=5000
)
```

---

## ⚙️ CONFIGURACIONES DE ENTRENAMIENTO

### 🏃 RÁPIDO (10-20 min) - Para pruebas

```python
trainer.train(
    num_train_epochs=1,
    batch_size=4,
    max_steps=500
)
```

### 🚶 NORMAL (1-2 horas) - Balance

```python
trainer.train(
    num_train_epochs=3,
    batch_size=4,
    max_steps=-1  # Todas las épocas
)
```

### 🐢 COMPLETO (4-8 horas) - Mejor calidad

```python
trainer.train(
    num_train_epochs=5,
    batch_size=8,  # Si tienes GPU potente
    max_steps=-1
)
```

### 💾 POCO RAM/GPU (más lento pero funciona)

```python
trainer.train(
    num_train_epochs=3,
    batch_size=2,  # Batch pequeño
    max_steps=-1
)
```

---

## 🔍 MONITOREAR EL PROGRESO

Durante el entrenamiento verás algo como:

```
{'loss': 2.341, 'learning_rate': 4.9e-05, 'epoch': 0.1}
Step 100/500 | Loss: 2.234 | Time: 12.3s
{'eval_loss': 2.123, 'eval_rouge1': 0.234, 'eval_rouge2': 0.156, 'eval_rougeL': 0.189}
{'loss': 1.987, 'learning_rate': 4.7e-05, 'epoch': 0.2}
Step 200/500 | Loss: 1.956 | Time: 12.1s
...
```

**Señales de buen entrenamiento:**
- ✅ Loss disminuye progresivamente
- ✅ ROUGE-1/2/L aumentan
- ✅ eval_loss más bajo que loss

**Señales de problemas:**
- ❌ Loss sube o se queda igual
- ❌ ROUGE no mejora
- ❌ Errores de memoria

---

## 🎓 PARA TU PROYECTO ACADÉMICO

### Experimentos Recomendados:

1. **Baseline: Modelo sin fine-tuning**
   ```python
   # Probar modelo base
   from transformers import AutoModelForSeq2SeqLM
   model = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-small")
   # Generar resúmenes y guardar métricas
   ```

2. **Experimento 1: Fine-tuning con 1000 ejemplos**
   ```python
   dataset = preparator.load_public_dataset("xsum", "en", num_samples=1000)
   # Entrenar y evaluar
   ```

3. **Experimento 2: Fine-tuning con 5000 ejemplos**
   ```python
   dataset = preparator.load_public_dataset("xsum", "en", num_samples=5000)
   # Entrenar y evaluar
   ```

4. **Experimento 3: Diferentes learning rates**
   ```python
   # Probar: 1e-5, 5e-5, 1e-4
   ```

### En tu informe incluye:

- 📊 Tabla comparativa de métricas
- 📈 Gráficas de loss y ROUGE durante entrenamiento
- 📝 Ejemplos de resúmenes (buenos y malos)
- 🔍 Análisis de errores
- 💡 Conclusiones y mejoras futuras

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Cuánto tiempo toma descargar el dataset?**
R: 5-15 minutos dependiendo de tu conexión

**P: ¿Puedo pausar el entrenamiento?**
R: Sí, puedes detenerlo (Ctrl+C) y reanudar desde el último checkpoint guardado

**P: ¿Qué hacer si me quedo sin memoria?**
R: Reduce batch_size a 2 o incluso 1

**P: ¿Necesito GPU?**
R: No es obligatorio, pero GPU es 5-10x más rápido

**P: ¿Puedo usar mis propios videos?**
R: Sí! Transcríbelos con Whisper y crea resúmenes manualmente

**P: ¿Cuántos datos necesito?**
R: Mínimo 1000 ejemplos, ideal 5000-10000

---

## ✅ CHECKLIST FINAL

Antes de considerar completado:

- [ ] Dataset descargado y tokenizado
- [ ] Modelo entrenado al menos 500 steps
- [ ] Métricas ROUGE > 0.30
- [ ] Modelo guardado en models/
- [ ] Probado con inference.py
- [ ] Ejemplos de resúmenes generados
- [ ] Comparado con modelo base
- [ ] Documentado para el informe

---

## 🎉 ¡LISTO!

Ahora tienes tu modelo entrenado y funcionando. 

**Próximos pasos:**
1. Genera resúmenes de tus videos
2. Analiza los resultados
3. Documenta todo en tu informe
4. Prepara tu presentación

**¡Éxito en tu proyecto!** 🚀🎓

---

**¿Necesitas más ayuda?**
- Lee `README.md` para documentación completa
- Revisa `GUIA_PROYECTO_ACADEMICO.md` para el informe
- Ejecuta `python ejemplos.py` para más ejemplos
