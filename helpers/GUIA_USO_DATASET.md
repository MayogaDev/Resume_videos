# 📚 GUÍA COMPLETA: Usar Dataset para Entrenar el Modelo

## 🎯 OPCIÓN 1: Dataset Público (MÁS FÁCIL - RECOMENDADO)

### Paso 1: Descargar y Preparar Dataset

```powershell
cd src
python
```

```python
from prepare_dataset import DatasetPreparator

# Crear preparador
preparator = DatasetPreparator(model_name="google/mt5-small")

# OPCIÓN A: Dataset en INGLÉS (XSum - Noticias BBC)
print("Descargando dataset XSum...")
dataset = preparator.load_public_dataset(
    dataset_name="xsum",
    language="en",
    num_samples=5000  # Empieza con 5000 para pruebas rápidas
)

# OPCIÓN B: Dataset en ESPAÑOL (MLSUM - Noticias)
# print("Descargando dataset MLSUM...")
# dataset = preparator.load_public_dataset(
#     dataset_name="mlsum",
#     language="es",
#     num_samples=5000
# )

print(f"\n✅ Dataset cargado!")
print(f"   Entrenamiento: {len(dataset['train'])} ejemplos")
print(f"   Validación: {len(dataset['validation'])} ejemplos")
print(f"   Test: {len(dataset['test'])} ejemplos")

# Ver un ejemplo
print("\n📄 Ejemplo del dataset:")
ejemplo = dataset['train'][0]
print(f"Documento: {ejemplo['document'][:200]}...")
print(f"Resumen: {ejemplo['summary']}")
```

### Paso 2: Preprocesar el Dataset

```python
# Tokenizar y preparar para el modelo
print("\n🔄 Preprocesando dataset...")
tokenized_dataset = preparator.prepare_dataset(
    dataset,
    text_column="document",
    summary_column="summary",
    max_input_length=512,
    max_target_length=128
)

# Guardar el dataset procesado
output_dir = "../data/processed/xsum_tokenized"
preparator.save_dataset(tokenized_dataset, output_dir)
print(f"\n✅ Dataset guardado en: {output_dir}")
```

### Paso 3: Entrenar el Modelo

```python
from train_model import SummaryTrainer

# Crear entrenador
trainer = SummaryTrainer(
    model_name="google/mt5-small",
    output_dir="../models/mt5-video-summarizer"
)

# ENTRENAMIENTO RÁPIDO (para pruebas - 10-20 minutos)
print("\n🏋️ Iniciando entrenamiento de prueba...")
trainer.train(
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    num_train_epochs=1,
    batch_size=4,
    learning_rate=5e-5,
    max_steps=500,  # Solo 500 pasos para prueba rápida
    save_steps=100,
    eval_steps=100
)

# ENTRENAMIENTO COMPLETO (mejor calidad - varias horas)
# trainer.train(
#     train_dataset=tokenized_dataset["train"],
#     eval_dataset=tokenized_dataset["validation"],
#     num_train_epochs=3,
#     batch_size=4,
#     learning_rate=5e-5,
#     save_steps=1000,
#     eval_steps=1000
# )

print("\n✅ ¡Entrenamiento completado!")
print("   Modelo guardado en: ../models/mt5-video-summarizer")
```

---

## 🎯 OPCIÓN 2: Crear Tu Propio Dataset (PARA PROYECTO ACADÉMICO)

### Paso 1: Preparar tus Videos y Transcripciones

```powershell
# 1. Coloca tus videos en la carpeta 'videos/'
# 2. Transcríbelos con Whisper
cd src
python
```

```python
from transcribe_video import VideoTranscriber

# Transcribir todos los videos
transcriber = VideoTranscriber(model_size="base", language="es")
transcriber.batch_transcribe("../videos", output_dir="../data/transcripts")

print("✅ Videos transcritos!")
```

### Paso 2: Crear Resúmenes Manualmente

Ahora necesitas crear resúmenes de referencia. Tienes dos opciones:

**Opción A: Manualmente (recomendado para proyecto académico)**
```python
# Para cada transcripción, crea un resumen manual
# Estructura del archivo: data/summaries/video1_summary.json
{
  "filename": "video1",
  "original_text": "Texto completo de la transcripción...",
  "summary": "Tu resumen manual aquí (2-3 oraciones principales)"
}
```

**Opción B: Usar GPT para generar resúmenes de referencia**
```python
# Requiere API key de OpenAI
from openai import OpenAI
import json
import os

client = OpenAI(api_key="tu-api-key")

def generar_resumen_referencia(texto):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en resumir textos académicos."},
            {"role": "user", "content": f"Resume este texto en 2-3 oraciones: {texto}"}
        ]
    )
    return response.choices[0].message.content

# Procesar transcripciones
transcripts_dir = "../data/transcripts"
for file in os.listdir(transcripts_dir):
    if file.endswith("_transcript.json"):
        with open(os.path.join(transcripts_dir, file), 'r') as f:
            data = json.load(f)
            texto = data['text']
            resumen = generar_resumen_referencia(texto)
            
            # Guardar
            summary_data = {
                "filename": file.replace("_transcript.json", ""),
                "original_text": texto,
                "summary": resumen
            }
            
            summary_file = file.replace("_transcript.json", "_summary.json")
            with open(f"../data/summaries/{summary_file}", 'w') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)

print("✅ Resúmenes de referencia creados!")
```

### Paso 3: Convertir a Dataset de Entrenamiento

```python
from datasets import Dataset, DatasetDict
import json
import os

# Cargar todos los pares texto-resumen
data = []
summaries_dir = "../data/summaries"

for file in os.listdir(summaries_dir):
    if file.endswith("_summary.json"):
        with open(os.path.join(summaries_dir, file), 'r') as f:
            summary_data = json.load(f)
            data.append({
                "document": summary_data["original_text"],
                "summary": summary_data["summary"]
            })

# Dividir en train/validation/test (70/15/15)
import random
random.shuffle(data)

n = len(data)
train_size = int(0.7 * n)
val_size = int(0.15 * n)

train_data = data[:train_size]
val_data = data[train_size:train_size+val_size]
test_data = data[train_size+val_size:]

# Crear dataset
dataset = DatasetDict({
    'train': Dataset.from_list(train_data),
    'validation': Dataset.from_list(val_data),
    'test': Dataset.from_list(test_data)
})

print(f"✅ Dataset personalizado creado!")
print(f"   Train: {len(train_data)} ejemplos")
print(f"   Validation: {len(val_data)} ejemplos")
print(f"   Test: {len(test_data)} ejemplos")

# Ahora tokeniza y entrena igual que en la Opción 1
from prepare_dataset import DatasetPreparator

preparator = DatasetPreparator(model_name="google/mt5-small")
tokenized_dataset = preparator.prepare_dataset(dataset)
preparator.save_dataset(tokenized_dataset, "../data/processed/custom_dataset")
```

---

## 🎯 OPCIÓN 3: Combinar Dataset Público + Tu Dataset

```python
from datasets import concatenate_datasets

# Cargar dataset público
preparator = DatasetPreparator(model_name="google/mt5-small")
public_dataset = preparator.load_public_dataset("xsum", "en", num_samples=3000)

# Cargar tu dataset personalizado
custom_dataset = load_from_disk("../data/processed/custom_dataset")

# Combinar
combined_train = concatenate_datasets([
    public_dataset['train'], 
    custom_dataset['train']
])

combined_dataset = DatasetDict({
    'train': combined_train,
    'validation': public_dataset['validation'],
    'test': custom_dataset['test']
})

print(f"✅ Dataset combinado: {len(combined_train)} ejemplos de entrenamiento")
```

---

## 📊 DATASETS PÚBLICOS DISPONIBLES

### Para ESPAÑOL:
```python
# 1. MLSUM (Noticias en español)
dataset = preparator.load_public_dataset("mlsum", "es", num_samples=5000)

# 2. WikiLingua (Wikipedia multilingüe)
from datasets import load_dataset
dataset = load_dataset("wiki_lingua", "spanish")
```

### Para INGLÉS:
```python
# 1. XSum (Noticias BBC - resúmenes extremos)
dataset = preparator.load_public_dataset("xsum", "en", num_samples=5000)

# 2. CNN/DailyMail (Noticias - resúmenes largos)
dataset = preparator.load_public_dataset("cnn_dailymail", "en", num_samples=5000)

# 3. SAMSum (Conversaciones y diálogos)
from datasets import load_dataset
dataset = load_dataset("samsum")
```

---

## 🚀 SCRIPT COMPLETO: Todo en Uno

Guarda este script como `entrenar_completo.py`:

```python
"""
Script completo para entrenar el modelo con un dataset
"""
from prepare_dataset import DatasetPreparator
from train_model import SummaryTrainer
import sys

def main():
    print("="*60)
    print("ENTRENAMIENTO COMPLETO DEL MODELO")
    print("="*60)
    
    # Paso 1: Cargar y preparar dataset
    print("\n[1/3] Cargando dataset...")
    preparator = DatasetPreparator(model_name="google/mt5-small")
    
    dataset = preparator.load_public_dataset(
        dataset_name="xsum",
        language="en",
        num_samples=5000  # Ajustar según tu hardware
    )
    
    print(f"   ✅ Dataset cargado: {len(dataset['train'])} ejemplos")
    
    # Paso 2: Tokenizar
    print("\n[2/3] Tokenizando dataset...")
    tokenized_dataset = preparator.prepare_dataset(dataset)
    preparator.save_dataset(tokenized_dataset, "../data/processed/xsum_tokenized")
    print("   ✅ Dataset tokenizado y guardado")
    
    # Paso 3: Entrenar
    print("\n[3/3] Entrenando modelo...")
    trainer = SummaryTrainer(
        model_name="google/mt5-small",
        output_dir="../models/mt5-video-summarizer"
    )
    
    # Entrenamiento rápido para pruebas
    trainer.train(
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        num_train_epochs=1,
        batch_size=4,
        learning_rate=5e-5,
        max_steps=500,  # Cambiar a -1 para entrenamiento completo
        save_steps=100,
        eval_steps=100
    )
    
    print("\n" + "="*60)
    print("✅ ¡ENTRENAMIENTO COMPLETADO!")
    print("="*60)
    print(f"Modelo guardado en: ../models/mt5-video-summarizer")
    print("\nPróximos pasos:")
    print("1. Evaluar el modelo en el test set")
    print("2. Generar resúmenes con inference.py")
    print("3. Comparar con el modelo base sin fine-tuning")

if __name__ == "__main__":
    main()
```

Ejecutar:
```powershell
cd src
python entrenar_completo.py
```

---

## ⚙️ AJUSTAR HIPERPARÁMETROS

### Para PRUEBAS RÁPIDAS (10-30 minutos):
```python
trainer.train(
    num_train_epochs=1,
    batch_size=4,
    max_steps=500,  # Solo 500 pasos
    learning_rate=5e-5
)
```

### Para ENTRENAMIENTO NORMAL (2-4 horas):
```python
trainer.train(
    num_train_epochs=3,
    batch_size=4,
    max_steps=-1,  # Todas las épocas
    learning_rate=5e-5
)
```

### Para MEJOR CALIDAD (8-12 horas):
```python
trainer.train(
    num_train_epochs=5,
    batch_size=8,  # Más batch si tienes GPU con más memoria
    max_steps=-1,
    learning_rate=3e-5
)
```

### Si tienes PROBLEMAS DE MEMORIA:
```python
trainer.train(
    num_train_epochs=3,
    batch_size=2,  # Reducir batch size
    max_steps=-1,
    learning_rate=5e-5
)
```

---

## 📊 MONITOREAR EL ENTRENAMIENTO

Durante el entrenamiento verás:
```
Step 100: Loss: 2.345, ROUGE-1: 0.234, ROUGE-L: 0.189
Step 200: Loss: 1.987, ROUGE-1: 0.267, ROUGE-L: 0.215
Step 300: Loss: 1.756, ROUGE-1: 0.289, ROUGE-L: 0.234
...
```

**¿Qué significa?**
- **Loss bajando** → El modelo está aprendiendo ✅
- **ROUGE subiendo** → Los resúmenes mejoran ✅
- **Loss estable/subiendo** → Reduce learning rate o detén el entrenamiento

---

## 🎓 PARA TU PROYECTO ACADÉMICO

**Recomendación:**
1. **Empieza con dataset público** (XSum o MLSUM) para aprender
2. **Crea tu dataset pequeño** (10-20 videos) para personalizar
3. **Combina ambos** para mejor rendimiento
4. **Compara métricas** antes y después del fine-tuning

**En tu informe muestra:**
- Tamaño del dataset usado
- Distribución (train/val/test)
- Hiperparámetros elegidos
- Evolución de métricas durante entrenamiento
- Comparación modelo base vs fine-tuned

---

## ✅ CHECKLIST DE ENTRENAMIENTO

- [ ] Dataset descargado/preparado
- [ ] Dataset tokenizado y guardado
- [ ] Modelo entrenado al menos 500 steps
- [ ] Métricas guardadas en logs
- [ ] Modelo guardado correctamente
- [ ] Probado con inferencia en nuevos textos
- [ ] Comparado con modelo base

¡Ahora tienes todo para entrenar tu modelo! 🚀
