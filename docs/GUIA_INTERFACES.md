# 🎬 Guía de Uso de las Interfaces de Usuario

## 📋 Tabla de Contenidos
1. [Interfaz Web (Gradio)](#interfaz-web-gradio)
2. [CLI Mejorada (Rich)](#cli-mejorada-rich)
3. [Instalación de Dependencias](#instalación)
4. [Ejemplos de Uso](#ejemplos)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🌐 Interfaz Web (Gradio)

### ¿Qué es?
Una interfaz web moderna y visual que se ejecuta en tu navegador. Perfecta para usuarios no técnicos.

### Características
- ✅ **Drag & Drop** de videos
- ✅ **Visualización en tiempo real** del progreso
- ✅ **Resultados en pestañas** (Resumen, Transcripción, Estadísticas)
- ✅ **Descarga de resultados** en JSON
- ✅ **Configuración avanzada** (modelos, longitud, calidad)
- ✅ **Responsive** (funciona en móviles y tablets)

### Instalación

```bash
# Instalar Gradio
pip install gradio

# O instalar todas las dependencias
pip install -r requirements.txt
```

### Uso Básico

```bash
# Iniciar la interfaz web
python src/web_app.py
```

Esto abrirá automáticamente tu navegador en `http://localhost:7860`

### Opciones Avanzadas

```bash
# Especificar ruta del modelo
python src/web_app.py --modelo models/mi-modelo-custom

# Cambiar puerto
python src/web_app.py --port 8080

# Compartir públicamente (genera URL pública)
python src/web_app.py --share

# Modo debug
python src/web_app.py --debug
```

### Ejemplo Completo

```bash
# Lanzar en puerto 8080 con URL pública
python src/web_app.py --port 8080 --share --modelo models/mt5-video-summarizer-final
```

### Uso en la Interfaz

1. **Subir video**: Arrastra tu video o haz clic para seleccionar
2. **Configurar** (opcional):
   - Modelo Whisper: `tiny` (rápido) a `large` (mejor calidad)
   - Longitud del resumen: 50-300 palabras
   - Calidad de generación: 1-8 beams (más = mejor)
3. **Procesar**: Haz clic en "🚀 Procesar Video"
4. **Ver resultados** en las pestañas:
   - ✨ **Resumen**: El texto resumido
   - 📝 **Transcripción**: Audio completo transcrito
   - 📊 **Estadísticas**: Métricas de compresión
5. **Descargar**: JSON con todos los resultados

---

## 💻 CLI Mejorada (Rich)

### ¿Qué es?
Interfaz de línea de comandos hermosa con colores, tablas, barras de progreso y paneles visuales.

### Características
- ✅ **Colores y emojis** para mejor legibilidad
- ✅ **Barras de progreso** animadas
- ✅ **Tablas de estadísticas** elegantes
- ✅ **Procesamiento por lotes** de múltiples videos
- ✅ **Información del sistema** en tiempo real

### Instalación

```bash
# Instalar Rich y Click
pip install rich click

# O instalar todas las dependencias
pip install -r requirements.txt
```

### Comandos Disponibles

#### 1. Procesar un video individual

```bash
python src/cli.py procesar mi_video.mp4
```

**Con opciones:**

```bash
# Especificar modelo y configuración
python src/cli.py procesar mi_video.mp4 \
  --modelo models/mt5-video-summarizer-final \
  --whisper small \
  --output resultados \
  --formato both
```

**Opciones:**
- `--modelo, -m`: Ruta al modelo mT5 (default: `models/mt5-video-summarizer-final`)
- `--whisper, -w`: Modelo Whisper: `tiny`, `base`, `small`, `medium`, `large` (default: `base`)
- `--output, -o`: Directorio de salida (default: `outputs`)
- `--formato, -f`: Formato de salida: `txt`, `json`, `both` (default: `both`)

#### 2. Procesamiento por lotes (múltiples videos)

```bash
python src/cli.py batch carpeta_videos/
```

**Ejemplo:**

```bash
# Procesar todos los videos de una carpeta
python src/cli.py batch "D:/Videos/Clases" \
  --modelo models/mt5-video-summarizer-final \
  --whisper base \
  --output resultados_clases
```

Esto procesará automáticamente todos los archivos `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm` encontrados en la carpeta.

#### 3. Información del sistema

```bash
python src/cli.py info
```

Muestra:
- ✅ Estado de Whisper, PyTorch, Transformers
- ✅ Versiones instaladas
- ✅ Información de GPU (si está disponible)
- ✅ Comandos disponibles

### Ejemplos Completos

```bash
# 1. Procesar un video con configuración básica
python src/cli.py procesar clase_matematicas.mp4

# 2. Procesar con modelo Whisper más preciso
python src/cli.py procesar conferencia.mp4 --whisper medium

# 3. Procesar y guardar solo en JSON
python src/cli.py procesar video.mp4 --formato json --output json_results

# 4. Procesamiento por lotes de todos los videos
python src/cli.py batch carpeta_videos/ --whisper small

# 5. Ver información del sistema
python src/cli.py info
```

---

## 📦 Instalación

### Opción 1: Instalar todo (recomendado)

```bash
pip install -r requirements.txt
```

### Opción 2: Instalar solo las interfaces

```bash
# Solo interfaz web
pip install gradio

# Solo CLI mejorada
pip install rich click

# Ambas interfaces
pip install gradio rich click
```

### Verificar instalación

```bash
# Verificar que todo está instalado
python src/verificar_instalacion.py

# O usar la CLI
python src/cli.py info
```

---

## 🚀 Ejemplos de Uso

### Ejemplo 1: Uso rápido con interfaz web

```bash
# 1. Iniciar interfaz
python src/web_app.py

# 2. Abrir navegador en http://localhost:7860
# 3. Arrastrar video
# 4. Clic en "Procesar"
# 5. ¡Listo! Ver resultados en pestañas
```

### Ejemplo 2: Procesamiento por lotes con CLI

```bash
# Procesar 10 videos de una carpeta automáticamente
python src/cli.py batch "D:/Videos/Clases_Semestre" \
  --whisper base \
  --output resultados_semestre
```

### Ejemplo 3: Compartir interfaz web públicamente

```bash
# Generar URL pública temporal (estilo Google Colab)
python src/web_app.py --share

# Resultado:
# Running on local URL:  http://127.0.0.1:7860
# Running on public URL: https://xxxxx.gradio.live (válido 72h)
```

### Ejemplo 4: Pipeline completo (sin interfaz)

```bash
# Usar el pipeline directo (sin UI)
python src/pipeline_completo.py \
  --video mi_video.mp4 \
  --modelo models/mt5-video-summarizer-final \
  --whisper base \
  --output outputs
```

---

## 🔍 Comparación de Interfaces

| Característica | Web (Gradio) | CLI (Rich) | Pipeline Directo |
|---------------|--------------|------------|------------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Visual** | ✅ Muy visual | ✅ Colores/Tablas | ❌ Texto plano |
| **Interactivo** | ✅ Sí | ⚠️ Limitado | ❌ No |
| **Procesamiento por lotes** | ❌ No | ✅ Sí | ✅ Sí |
| **Configuración avanzada** | ✅ En UI | ✅ Argumentos | ✅ Argumentos |
| **Descarga resultados** | ✅ JSON | ✅ TXT/JSON | ✅ TXT/JSON |
| **Acceso remoto** | ✅ Con --share | ❌ Solo local | ❌ Solo local |
| **Uso en servidor** | ✅ Ideal | ⚠️ Posible | ✅ Ideal |
| **Scriptable** | ❌ No | ✅ Sí | ✅ Sí |

### ¿Cuál usar?

- **Interfaz Web**: Para demos, usuarios no técnicos, acceso remoto
- **CLI Rich**: Para uso profesional, scripts, procesamiento por lotes
- **Pipeline Directo**: Para integración en otros sistemas, automatización

---

## 🐛 Solución de Problemas

### Problema 1: "No se ha podido resolver la importación 'gradio'"

```bash
# Solución: Instalar Gradio
pip install gradio
```

### Problema 2: "Puerto ya en uso" (Interfaz Web)

```bash
# Solución 1: Cambiar puerto
python src/web_app.py --port 8080

# Solución 2: Encontrar proceso usando el puerto
netstat -ano | findstr :7860

# Solución 3: Cerrar el proceso (PowerShell)
Stop-Process -Id <PID>
```

### Problema 3: La CLI no muestra colores

```bash
# Windows PowerShell: Asegurarse de tener UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# O usar Windows Terminal (recomendado)
# https://aka.ms/terminal
```

### Problema 4: Error al compartir interfaz web (--share)

```bash
# Requiere conexión a internet
# Solución: Verificar conexión o usar solo local
python src/web_app.py  # Sin --share
```

### Problema 5: "ModuleNotFoundError: No module named 'rich'"

```bash
# Solución: Instalar Rich
pip install rich click
```

### Problema 6: Interfaz web muy lenta

```bash
# Usar modelo Whisper más pequeño
# En la UI: Seleccionar "tiny" o "base"

# O en CLI:
python src/cli.py procesar video.mp4 --whisper tiny
```

---

## 📊 Formatos de Salida

### Formato TXT
```
RESUMEN DEL VIDEO: mi_video
Fecha: 2025-10-13 15:30:00
======================================================================

RESUMEN:
----------------------------------------------------------------------
[Texto del resumen aquí...]

======================================================================

TRANSCRIPCIÓN COMPLETA:
----------------------------------------------------------------------
[Texto completo de la transcripción...]
```

### Formato JSON
```json
{
  "video": "mi_video",
  "timestamp": "2025-10-13 15:30:00",
  "transcripcion": "Texto completo...",
  "resumen": "Resumen generado...",
  "estadisticas": {
    "transcripcion": {
      "caracteres": 5430,
      "palabras": 892
    },
    "resumen": {
      "caracteres": 654,
      "palabras": 108
    },
    "compresion": {
      "ratio_caracteres": 0.12,
      "ratio_palabras": 0.12
    }
  }
}
```

---

## 🎯 Mejores Prácticas

### Para Interfaz Web
1. ✅ Usar `--share` solo para demos temporales
2. ✅ Configurar `--port` si usas múltiples servicios
3. ✅ Descargar el JSON para respaldo
4. ✅ Probar con videos cortos primero (<5 min)

### Para CLI
1. ✅ Usar `batch` para múltiples videos
2. ✅ Guardar en carpetas organizadas (`--output`)
3. ✅ Usar formato `json` para análisis posterior
4. ✅ Verificar sistema con `info` antes de empezar

### General
1. ✅ Videos de hasta 30 minutos funcionan bien
2. ✅ Modelos Whisper: `base` es buen balance calidad/velocidad
3. ✅ Primera ejecución descarga modelos (~2-3 min)
4. ✅ GPU acelera 10x vs CPU

---

## 📚 Recursos Adicionales

- **Documentación Gradio**: https://gradio.app/docs
- **Documentación Rich**: https://rich.readthedocs.io
- **Whisper (OpenAI)**: https://github.com/openai/whisper
- **Transformers (Hugging Face)**: https://huggingface.co/docs/transformers

---

## 🤝 Soporte

Si encuentras problemas:

1. Verifica instalación: `python src/verificar_instalacion.py`
2. Consulta esta guía en la sección de [Solución de Problemas](#solución-de-problemas)
3. Revisa los logs/errores en la terminal
4. Prueba con videos más cortos o modelos más pequeños

---

**¡Disfruta resumiendo tus videos educativos!** 🎉
