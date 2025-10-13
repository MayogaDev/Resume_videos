# 🐛 Solución de Problemas en Google Colab

## Errores Comunes y Soluciones

### ❌ Error 1: FileNotFoundError con ROUGE

**Error completo:**
```
FileNotFoundError: Couldn't find a module script at /content/rouge/rouge.py. 
Module 'rouge' doesn't exist on the Hugging Face Hub either.
```

**Causa:**
El paquete `evaluate` a veces tiene problemas cargando la métrica `rouge` en Colab.

**✅ Solución (Ya implementada en el notebook):**

El notebook ahora tiene un sistema de fallback que prueba 3 métodos:

1. **Método 1 (Preferido):** `evaluate.load("rouge")`
2. **Método 2 (Alternativa):** `datasets.load_metric("rouge")`
3. **Método 3 (Último recurso):** Usar `rouge_score` directamente

El código se ve así:

```python
try:
    rouge = evaluate.load("rouge")
except Exception:
    try:
        from datasets import load_metric
        rouge = load_metric("rouge")
    except:
        from rouge_score import rouge_scorer
        # Crear wrapper personalizado
```

**Si aún falla, ejecuta manualmente:**

```python
# En una celda de Colab
!pip uninstall -y evaluate rouge-score
!pip install evaluate==0.4.1 rouge-score==0.1.2
```

Luego reinicia el runtime: `Runtime > Restart runtime`

---

### ❌ Error 2: CUDA Out of Memory (OOM)

**Error:**
```
RuntimeError: CUDA out of memory
```

**Causa:**
Batch size demasiado grande para la GPU disponible.

**✅ Soluciones:**

**Opción 1: Reducir batch size (rápido)**

Modifica la celda 4 (Configuración de Hiperparámetros):

```python
CONFIG = {
    # ... otras configuraciones
    "per_device_train_batch_size": 2,      # Reducir de 4/8 a 2
    "gradient_accumulation_steps": 8,      # Aumentar de 4 a 8
    "per_device_eval_batch_size": 4,       # Reducir evaluación
}
```

**Opción 2: Reducir ejemplos de entrenamiento**

```python
CONFIG = {
    # ... otras configuraciones
    "train_samples": 5000,  # Reducir de 10000 a 5000
    "val_samples": 500,
    "test_samples": 250,
}
```

**Opción 3: Usar GPU más grande**

En Colab: `Runtime > Change runtime type > GPU type > V100 o A100`
(Requiere Colab Pro)

---

### ❌ Error 3: Desconexión de Colab

**Problema:**
Colab se desconecta después de 90 minutos de inactividad.

**✅ Solución 1: Keep-Alive Script**

Ejecuta esto en la consola del navegador (F12):

```javascript
function ClickConnect(){
  console.log("Manteniéndose conectado...");
  document.querySelector("colab-connect-button").click()
}
setInterval(ClickConnect, 60000) // Cada 60 segundos
```

**✅ Solución 2: Usar Checkpoints**

El notebook guarda checkpoints cada 500 pasos en Google Drive. Si se desconecta:

1. Monta Drive de nuevo (Celda 3)
2. Ejecuta la celda 15: "Reanudar Entrenamiento desde Checkpoint"

---

### ❌ Error 4: Google Drive no se monta

**Error:**
```
MessageError: Error: credential propagation was unsuccessful
```

**✅ Solución:**

```python
from google.colab import drive

# Forzar montaje con autenticación
drive.flush_and_unmount()
drive.mount('/content/drive', force_remount=True)
```

Si persiste:
1. `Runtime > Disconnect and delete runtime`
2. Volver a ejecutar desde el inicio

---

### ❌ Error 5: Tokenizer demasiado lento

**Problema:**
La tokenización toma más de 10 minutos.

**✅ Solución:**

En la celda 6 (Tokenización), modifica:

```python
tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset['train'].column_names,
    num_proc=2,  # ⭐ Agregar esta línea para paralelización
    desc="Tokenizando dataset"
)
```

---

### ❌ Error 6: Import Error con transformers

**Error:**
```
ImportError: cannot import name 'XXX' from 'transformers'
```

**✅ Solución:**

```python
# Forzar reinstalación de versión específica
!pip uninstall -y transformers
!pip install transformers==4.36.0 --no-cache-dir
```

Luego: `Runtime > Restart runtime`

---

### ❌ Error 7: Dataset no se descarga

**Error:**
```
ConnectionError: Couldn't reach https://huggingface.co/datasets/mlsum
```

**✅ Solución:**

Verifica conexión de Colab:

```python
!curl -I https://huggingface.co
```

Si falla, prueba cambiar región de descarga:

```python
from datasets import load_dataset

# Usar mirror alternativo
dataset = load_dataset(
    "mlsum",
    "es",
    trust_remote_code=True,
    download_mode="force_redownload"  # ⭐ Forzar descarga
)
```

---

### ❌ Error 8: TensorBoard no se visualiza

**Problema:**
TensorBoard no muestra gráficas.

**✅ Solución:**

```python
# Recargar extensión
%reload_ext tensorboard

# Limpiar y reiniciar
!rm -rf logs/
%tensorboard --logdir {CONFIG['logging_dir']} --port 6006
```

---

### ❌ Error 9: Modelo no se guarda en Drive

**Problema:**
Los checkpoints no aparecen en Google Drive.

**✅ Solución:**

Verificar que Drive está montado:

```python
import os

drive_path = "/content/drive/MyDrive/video_summarizer"
if os.path.exists(drive_path):
    print(f"✅ Drive montado correctamente en: {drive_path}")
    print(f"📂 Archivos actuales: {os.listdir(drive_path)}")
else:
    print("❌ Drive no montado o ruta incorrecta")
    print("💡 Ejecuta de nuevo la celda 3 para montar Drive")
```

---

### ❌ Error 10: ROUGE scores = 0.0

**Problema:**
Todas las métricas ROUGE retornan 0.0.

**Posible causa:**
- Resúmenes vacíos
- Problema con tokenización
- Error en `compute_metrics`

**✅ Solución:**

Debuggear en celda aparte:

```python
# Probar generación manual
test_text = dataset['train'][0]['text']
test_inputs = tokenizer("resumir: " + test_text, return_tensors="pt", max_length=512, truncation=True)

# Mover a GPU si está disponible
test_inputs = {k: v.to(model.device) for k, v in test_inputs.items()}

# Generar
with torch.no_grad():
    outputs = model.generate(**test_inputs, max_length=128)

# Decodificar
generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Texto generado: {generated}")

# Si está vacío, hay un problema con el modelo
if not generated.strip():
    print("❌ El modelo no está generando texto")
    print("💡 Posibles causas:")
    print("   - Modelo no entrenado aún")
    print("   - Hiperparámetros incorrectos")
    print("   - Tokenización incorrecta")
```

---

## 🚀 Checklist Pre-Entrenamiento

Antes de iniciar el entrenamiento largo, verifica:

- [ ] ✅ GPU detectada (`torch.cuda.is_available()`)
- [ ] ✅ Google Drive montado (`/content/drive/MyDrive`)
- [ ] ✅ Dependencias instaladas (celda 2 ejecutada sin errores)
- [ ] ✅ Dataset cargado correctamente (10K+ ejemplos)
- [ ] ✅ ROUGE configurado sin errores (celda 7)
- [ ] ✅ Modelo cargado en memoria (~1.2 GB)
- [ ] ✅ Directorios de salida creados

---

## 📞 Soporte Rápido

### Reinicio completo (Solución universal)

Si todo falla, reinicio limpio:

```python
# 1. Limpiar todo
!rm -rf /root/.cache/huggingface
!rm -rf /content/drive/MyDrive/video_summarizer

# 2. Reiniciar runtime
# Runtime > Disconnect and delete runtime

# 3. Volver a ejecutar desde la celda 1
```

### Verificación rápida del estado

```python
import torch
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO GPU'}")
print(f"Drive: {'✅' if os.path.exists('/content/drive/MyDrive') else '❌'}")
print(f"Transformers: {transformers.__version__}")
print(f"Datasets: {datasets.__version__}")
print(f"Evaluate: {evaluate.__version__}")
```

---

## 💡 Tips para Entrenamiento Exitoso

1. **Usa Colab Pro**: GPU V100/A100 son 5-10x más rápidas
2. **Entrena de noche**: Menos riesgo de desconexión
3. **Revisa cada 30min**: Monitorea TensorBoard
4. **Guarda checkpoints**: Cada 500 pasos se guarda automáticamente
5. **Reduce ejemplos primero**: Prueba con 1K ejemplos para debug
6. **Aumenta batch size gradualmente**: Empieza en 2, sube a 4, 8...

---

**Última actualización:** Octubre 2025  
**Notebook versión:** entrenar_mt5_colab_pro.ipynb v2.0 (con fix de ROUGE)
