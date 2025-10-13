# 🚀 GUÍA DE ENTRENAMIENTO ROBUSTO - RTX 3050

## ✅ Hardware Detectado
- **GPU**: NVIDIA GeForce RTX 3050 Laptop GPU
- **VRAM**: 4.00 GB
- **CUDA**: 12.8
- **PyTorch**: 2.7.1+cu128

---

## 📋 ARCHIVOS CREADOS

### 1. `check_gpu.py`
Verifica que la GPU esté disponible y funcionando.

```powershell
python check_gpu.py
```

### 2. `src/config_rtx3050.py`
Configuración optimizada para tu RTX 3050 (4GB VRAM):
- **Modelo**: mT5-small (300M parámetros, multilingüe)
- **Dataset**: MLSUM en español
- **Batch size**: 2 (optimizado para 4GB)
- **Gradient accumulation**: 8 (simula batch_size=16)
- **FP16**: Activado (precisión mixta para ahorrar memoria)
- **Samples**: 10,000 entrenamiento / 1,000 validación

### 3. `src/train_robusto_rtx3050.py`
Script de entrenamiento con:
- ✅ Checkpoints automáticos cada 500 steps
- ✅ Early stopping (si no mejora en 3 evaluaciones)
- ✅ Manejo robusto de errores
- ✅ Logging detallado
- ✅ Limpieza automática de memoria
- ✅ TensorBoard para monitoreo

---

## 🎯 CONFIGURACIÓN ACTUAL

```python
MODELO: google/mt5-small (español optimizado)
DATASET: MLSUM - 10,000 ejemplos
BATCH SIZE: 2 (efectivo: 16 con gradient accumulation)
ÉPOCAS: 3
FP16: Activado
MAX INPUT: 512 tokens
MAX OUTPUT: 128 tokens
```

### ⏱️ Tiempo Estimado
Con 10,000 ejemplos: **4-6 horas**

---

## 🚀 CÓMO ENTRENAR

### Paso 1: Verificar GPU
```powershell
python check_gpu.py
```

Deberías ver:
```
✓ GPU detectada: NVIDIA GeForce RTX 3050 Laptop GPU
✓ VRAM Total: 4.00 GB
✅ GPU lista para entrenamiento!
```

### Paso 2: Iniciar Entrenamiento
```powershell
cd src
python train_robusto_rtx3050.py
```

El script te mostrará:
1. Configuración completa
2. Verificación de GPU
3. Confirmación para iniciar
4. Progreso en tiempo real

### Paso 3: Monitorear (Opcional)
En otra terminal, ejecuta:
```powershell
tensorboard --logdir ./logs
```

Abre tu navegador en: http://localhost:6006

---

## 📊 QUÉ ESPERAR DURANTE EL ENTRENAMIENTO

### Fase 1: Preparación (5-10 min)
```
📥 Descargando dataset MLSUM...
🔤 Tokenizando dataset...
🧠 Cargando modelo mT5-small...
```

### Fase 2: Entrenamiento (4-6 horas)
```
Step 50/3750   | Loss: 2.5 | LR: 1e-5
Step 100/3750  | Loss: 2.1 | LR: 2e-5
...
Step 500/3750  | Loss: 1.5 | Evaluando...
  - ROUGE-1: 0.25
  - ROUGE-2: 0.10
  - Guardando checkpoint...
...
Step 3750/3750 | Loss: 0.9 | ✅ Completado
```

### Fase 3: Evaluación Final (5 min)
```
📊 RESULTADOS FINALES
  ROUGE-1: 0.42
  ROUGE-2: 0.18
  ROUGE-L: 0.35
```

---

## 💾 CHECKPOINTS AUTOMÁTICOS

El modelo se guarda automáticamente:
- **Cada 500 steps**: `models/mt5-small-mlsum-es-rtx3050/checkpoint-500/`
- **Mejor modelo**: Se guarda el de mejor ROUGE-1
- **Al finalizar**: `models/mt5-small-mlsum-es-rtx3050/`

Si se interrumpe el entrenamiento:
```powershell
# El trainer detecta checkpoints automáticamente
python train_robusto_rtx3050.py
# Te preguntará si quieres reanudar
```

---

## ⚠️ POSIBLES PROBLEMAS Y SOLUCIONES

### 1. Error: "CUDA out of memory"
**Solución**: Edita `src/config_rtx3050.py`
```python
# Línea 57: Reduce batch size
"per_device_train_batch_size": 1,  # Era 2

# Línea 59: Aumenta gradient accumulation
"gradient_accumulation_steps": 16,  # Era 8

# O reduce samples:
"train_samples": 5000,  # Era 10000
```

### 2. Dataset muy lento de descargar
**Solución**: Usa menos samples
```python
"train_samples": 1000,   # Para prueba rápida (30 min)
"val_samples": 200,
```

### 3. Entrenamiento muy lento
**Solución**: Verifica que GPU esté en uso
```powershell
# Abre Task Manager > Rendimiento > GPU
# Debería mostrar uso de GPU1 (NVIDIA)
```

### 4. Error: "No module named 'evaluate'"
```powershell
pip install evaluate rouge-score
```

---

## 📈 INTERPRETACIÓN DE MÉTRICAS

### ROUGE Scores (0 a 1, más alto = mejor)
- **ROUGE-1**: Coincidencia de palabras individuales
  - < 0.30: Bajo
  - 0.30-0.40: Aceptable
  - 0.40-0.50: Bueno
  - > 0.50: Excelente

- **ROUGE-2**: Coincidencia de pares de palabras
  - < 0.15: Bajo
  - 0.15-0.25: Bueno
  - > 0.25: Excelente

- **ROUGE-L**: Secuencia común más larga
  - Similar a ROUGE-1

### Loss (pérdida)
- **Inicio**: ~2.5
- **Medio**: ~1.5
- **Final**: ~0.8-1.0 (ideal)

---

## 🎯 DESPUÉS DEL ENTRENAMIENTO

### 1. Probar el modelo
```powershell
cd src
python inference.py
```

### 2. Transcribir un video
```powershell
python transcribe_video.py --video ../videos/mi_video.mp4
```

### 3. Pipeline completo
```powershell
python pipeline.py --mode full --video ../videos/mi_video.mp4
```

---

## 📁 ESTRUCTURA DE SALIDA

```
models/mt5-small-mlsum-es-rtx3050/
├── checkpoint-500/          # Checkpoint en step 500
├── checkpoint-1000/         # Checkpoint en step 1000
├── checkpoint-1500/         # Checkpoint en step 1500
├── config.json              # Configuración del modelo
├── pytorch_model.bin        # Pesos del modelo final
├── tokenizer_config.json    # Configuración tokenizer
├── special_tokens_map.json
└── final_metrics.txt        # Métricas finales

logs/
├── training_20251006_143022.log  # Log detallado
└── runs/                         # TensorBoard logs
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Entrenar con MÁS datos (mejor calidad)
```python
# src/config_rtx3050.py
"train_samples": 50000,  # 20-24 horas
"val_samples": 5000,
```

### Entrenar MÁS RÁPIDO (para pruebas)
```python
"train_samples": 1000,   # 30-45 min
"val_samples": 200,
"num_train_epochs": 1,   # Solo 1 época
```

### Modelo MÁS PEQUEÑO (si hay problemas de memoria)
```python
"model_name": "google/mt5-small",  # Ya es el más pequeño
"max_input_length": 256,           # Reduce de 512 a 256
"max_target_length": 64,           # Reduce de 128 a 64
```

---

## 📞 MONITOREO EN TIEMPO REAL

### Ver uso de GPU
```powershell
# Windows
# Abre Task Manager > Rendimiento > GPU 1

# O usa:
nvidia-smi
```

### Ver logs en tiempo real
```powershell
# En otra terminal
Get-Content logs/training_*.log -Wait -Tail 50
```

### TensorBoard (visualización gráfica)
```powershell
tensorboard --logdir ./logs
# Abre: http://localhost:6006
```

---

## ✅ CHECKLIST PRE-ENTRENAMIENTO

- [ ] GPU detectada correctamente (`python check_gpu.py`)
- [ ] Dataset configurado (MLSUM español)
- [ ] Suficiente espacio en disco (~5GB)
- [ ] PC conectado a corriente (no batería)
- [ ] Tiempo disponible (4-6 horas)
- [ ] TensorBoard listo (opcional)

---

## 🎉 ¡LISTO PARA ENTRENAR!

```powershell
cd src
python train_robusto_rtx3050.py
```

**¡Buena suerte con tu entrenamiento!** 🚀
