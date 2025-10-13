# Carpeta de Imágenes para el Informe

Esta carpeta debe contener las capturas de pantalla de cada capa de la arquitectura.

## 📸 Capturas Requeridas

Toma capturas de los siguientes componentes del diagrama PlantUML:

1. **capa_entrada.png** - Capa de Entrada (Usuario + Videos)
2. **capa_transcripcion.png** - Capa de Transcripción (Extractor + Whisper + Transcripciones)
3. **capa_entrenamiento.png** - Capa de Entrenamiento (Dataset + Tokenizer + mT5 + Trainer + Modelo)
4. **capa_inferencia.png** - Capa de Inferencia (Preprocesador + mT5 Fine-tuned + Post-procesador)
5. **capa_presentacion.png** - Capa de Presentación (Interfaz Web + Base de Datos)
6. **capa_infraestructura.png** - Capa de Infraestructura (GPU + Almacenamiento)
7. **capa_monitoreo.png** - Capa de Monitoreo (TensorBoard + Logs)

## 🎯 Cómo Tomar las Capturas

### Desde el Archivo PlantUML:

1. Abre `arquitectura_sistema.puml` o `arquitectura_simplificada.puml`
2. Genera el diagrama (Alt+D en VS Code)
3. Haz zoom en cada capa
4. Toma captura de pantalla (Win+Shift+S)
5. Recorta solo la capa correspondiente
6. Guarda con el nombre especificado

### Formato Recomendado:

- **Formato**: PNG (mejor calidad para LaTeX)
- **Resolución**: Al menos 1920x1080
- **Fondo**: Blanco o transparente
- **Recorte**: Solo la capa específica, sin espacio extra

## 📐 Dimensiones

Las imágenes se mostrarán con `width=0.9\textwidth` en el documento, lo que significa que ocuparán el 90% del ancho de la página.

**Recomendación**: Toma capturas en alta resolución para que se vean bien al imprimir.

## ✅ Checklist

- [ ] capa_entrada.png
- [ ] capa_transcripcion.png
- [ ] capa_entrenamiento.png
- [ ] capa_inferencia.png
- [ ] capa_presentacion.png
- [ ] capa_infraestructura.png
- [ ] capa_monitoreo.png

Una vez que tengas todas las imágenes, actualiza el archivo `informe_tecnico.tex` reemplazando los espacios vacíos con las referencias a las imágenes.
