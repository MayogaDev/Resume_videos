"""
Interfaz Web con Gradio para Resumen de Videos
Aplicación web moderna y fácil de usar

Autor: Sistema de Resumen de Videos Educativos
Fecha: Octubre 2025
"""

import gradio as gr
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import traceback

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Importar desde la nueva estructura
try:
    from backend.core.transcription import VideoTranscriber
    from backend.core.summarization import VideoSummarizer
    from backend.core.extractive_summarizer import HybridSummarizer
    from backend.core.text_analyzer import TextAnalyzer
    from backend.services.video_processor import VideoProcessorService
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("\nAsegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class VideoSummarizerWebApp:
    """
    Aplicación web para resumir videos
    """
    
    def __init__(self, modelo_path="models/mt5-video-summarizer-final"):
        """
        Inicializa la aplicación

        Args:
            modelo_path: Ruta al modelo mT5 entrenado
        """
        self.modelo_path = modelo_path
        self.transcriber = None
        self.summarizer = None
        self.analyzer = TextAnalyzer()  # Siempre disponible
        self.inicializado = False
        
    def inicializar_modelos(self, whisper_model="base"):
        """
        Inicializa Whisper y mT5 (lazy loading)
        
        Args:
            whisper_model: Modelo de Whisper a usar
        """
        if self.inicializado:
            return "✅ Modelos ya inicializados"
        
        try:
            print("🔄 Inicializando Whisper...")
            self.transcriber = VideoTranscriber(model_size=whisper_model)

            print("🔄 Inicializando Resumidor Híbrido...")
            # Intentar cargar modelo abstractivo
            try:
                abstractive = VideoSummarizer(model_path=self.modelo_path)
                print("   ✅ Modelo abstractivo cargado")
            except Exception as e:
                print(f"   ⚠️ No se pudo cargar modelo abstractivo: {e}")
                abstractive = None

            # Crear resumidor híbrido (usa extractivo como fallback)
            self.summarizer = HybridSummarizer(abstractive_summarizer=abstractive)

            self.inicializado = True
            return "✅ Modelos inicializados correctamente"

        except Exception as e:
            return f"❌ Error al inicializar modelos: {str(e)}"
    
    def procesar_video(
        self,
        video_file,
        whisper_model="base",
        max_length=150,
        num_beams=4,
        progress=gr.Progress()
    ):
        """
        Procesa un video completo: transcripción + resumen

        Args:
            video_file: Archivo de video subido
            whisper_model: Modelo Whisper a usar
            max_length: Longitud máxima del resumen
            num_beams: Número de beams para generación
            progress: Objeto de progreso de Gradio
        """
        if video_file is None:
            return None, "⚠️ Por favor sube un video", None, None, None

        try:
            import time
            start_time = time.time()

            # Obtener información del video
            video_path = video_file.name if hasattr(video_file, 'name') else video_file
            video_name = Path(video_path).name
            file_size_mb = Path(video_path).stat().st_size / (1024 * 1024)

            # PASO 0: Validación
            progress(0, desc="🔍 Validando archivo...")
            estado_inicial = f"""
🔍 **Validando archivo...**

📁 **Archivo:** {video_name}
📊 **Tamaño:** {file_size_mb:.2f} MB
🎤 **Modelo Whisper:** {whisper_model}
⏱️ **Tiempo estimado:** {self._estimar_tiempo(file_size_mb)} minutos

🔄 Iniciando procesamiento...
            """
            yield None, estado_inicial, None, None, None
            time.sleep(0.5)

            # Inicializar modelos
            progress(0.05, desc="🔧 Inicializando modelos...")
            estado_init = f"""
🔧 **Inicializando modelos de IA...**

📁 Video: {video_name} ({file_size_mb:.2f} MB)
🎤 Cargando Whisper {whisper_model}...
🧠 Preparando sistema de resumen híbrido...

💡 *Primera ejecución puede tardar más (descarga de modelos)*
            """
            yield None, estado_init, None, None, None

            init_msg = self.inicializar_modelos(whisper_model)
            if "❌" in init_msg:
                yield None, init_msg, None, None, None
                return

            # PASO 1: Transcripción (5-60%)
            progress(0.10, desc="🎬 Extrayendo audio...")
            estado_audio = f"""
🎬 **[Paso 1/3] Extrayendo audio del video...**

📁 Video: {video_name}
🔊 Convirtiendo a formato de audio optimizado...

⏳ *Esto puede tardar según el tamaño del video*
            """
            yield None, estado_audio, None, None, None

            progress(0.20, desc="🎤 Transcribiendo con Whisper...")
            estado_transcribe = f"""
🎤 **[Paso 1/3] Transcribiendo audio con Whisper...**

🧠 Modelo: Whisper {whisper_model}
🌍 Idioma: Español
🔄 Procesando audio...

💡 *Whisper está convirtiendo el audio en texto*
            """
            yield None, estado_transcribe, None, None, None

            print(f"\n[1/3] Transcribiendo: {video_name}")
            transcript_result = self.transcriber.transcribe_video(video_path, save_transcript=False, cleanup_audio=True)
            transcripcion = transcript_result.get('text', '')

            if not transcripcion or len(transcripcion.strip()) < 50:
                yield None, "❌ Transcripción muy corta o vacía. Verifica que el video tenga audio.", None, None, None
                return

            # Transcripción completada
            progress(0.60, desc="✅ Transcripción completada")
            palabras_transcritas = len(transcripcion.split())
            estado_trans_ok = f"""
✅ **[Paso 1/3] Transcripción completada**

📝 **Resultado:**
- Palabras: {palabras_transcritas:,}
- Caracteres: {len(transcripcion):,}

🎯 Texto capturado correctamente
            """
            yield None, estado_trans_ok, None, None, None
            time.sleep(0.5)

            # PASO 2: Resumen (60-85%)
            progress(0.65, desc="🧠 Analizando texto...")
            estado_analisis = f"""
🧠 **[Paso 2/3] Analizando texto...**

📊 Identificando palabras clave...
📋 Extrayendo puntos principales...
🔍 Preparando para resumen...

💡 *Analizando {palabras_transcritas:,} palabras*
            """
            yield None, estado_analisis, None, None, None

            print(f"[2/4] Analizando texto...")
            analysis = self.analyzer.analyze_text(transcripcion)

            progress(0.72, desc="✨ Generando resumen...")
            estado_resumen = f"""
✨ **[Paso 2/3] Generando resumen inteligente...**

🧠 Sistema híbrido activado:
- Intentando resumen abstractivo (mT5)...
- Fallback extractivo disponible

📊 Procesando {palabras_transcritas:,} palabras
🎯 Objetivo: ~{int(palabras_transcritas * 0.25)} palabras

⏳ *Esto puede tardar 30-60 segundos*
            """
            yield None, estado_resumen, None, None, None

            print(f"[3/4] Generando resumen...")
            # El híbrido usa extractivo si el abstractivo falla
            resumen = self.summarizer.summarize(
                transcripcion,
                use_abstractive=True,  # Intentar abstractivo primero
                compression_ratio=0.25,  # 25% del original para extractivo
                max_length=max_length,   # Para abstractivo
                num_beams=num_beams      # Para abstractivo
            )

            # PASO 3: Finalización (85-100%)
            progress(0.90, desc="📊 Calculando estadísticas...")
            estado_stats = f"""
📊 **[Paso 3/3] Finalizando procesamiento...**

📈 Calculando estadísticas...
📁 Preparando archivos descargables...
✨ Generando informe completo...

⏳ Casi listo...
            """
            yield None, estado_stats, None, None, None

            print(f"[4/4] Generando archivos...")
            stats = self._calcular_estadisticas(transcripcion, resumen, video_name)

            # Formatear resultados para mostrar
            resultado_transcripcion = self._formatear_transcripcion(transcripcion, stats)
            resultado_resumen = self._formatear_resumen_mejorado(resumen, analysis, stats)
            resultado_stats = self._formatear_stats_html(stats, analysis)

            # Crear archivo Markdown descargable
            md_content = self.analyzer.format_markdown(
                video_name, transcripcion, resumen, analysis, stats
            )
            md_path = f"resultados_{video_name}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            # También crear JSON por compatibilidad
            json_output = self._crear_json_output(video_name, transcripcion, resumen, stats, analysis)
            json_path = f"resultados_{video_name}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)

            progress(1.0, desc="🎉 ¡Completado!")

            # Calcular tiempo total
            elapsed_time = time.time() - start_time
            minutos = int(elapsed_time // 60)
            segundos = int(elapsed_time % 60)
            tiempo_str = f"{minutos}:{segundos:02d}" if minutos > 0 else f"{segundos} segundos"

            mensaje_exito = f"""
🎉 **¡Proceso completado exitosamente!**

📁 **Video:** {Path(video_path).name}
📌 **Título:** {analysis['title']}
⏱️ **Tiempo total:** {tiempo_str}

📊 **Resumen de resultados:**
- Transcripción: {stats['transcripcion']['palabras']:,} palabras
- Resumen: {stats['resumen']['palabras']:,} palabras
- Compresión: {(1-stats['compresion']['ratio_palabras'])*100:.1f}% reducción

📥 **Archivos descargables:**
- ✅ Informe Markdown completo
- ✅ Datos JSON estructurados

💡 *Puedes descargar los archivos desde el botón de descarga*
            """

            yield (
                resultado_transcripcion,
                mensaje_exito,
                resultado_resumen,
                resultado_stats,
                md_path
            )

        except Exception as e:
            error_msg = f"""
❌ **Error durante el procesamiento**

**Detalles:** {str(e)}

**Posibles soluciones:**
- Verifica que el video tenga audio
- Prueba con un video más pequeño
- Intenta con un modelo Whisper diferente

**Información técnica:**
```
{traceback.format_exc()}
```
            """
            print(error_msg)
            yield None, error_msg, None, None, None

    def _estimar_tiempo(self, file_size_mb: float) -> str:
        """
        Estima el tiempo de procesamiento basado en el tamaño del video

        Args:
            file_size_mb: Tamaño del archivo en MB

        Returns:
            Tiempo estimado en formato legible
        """
        # Aproximación: 1 minuto por cada 10MB + 1 minuto para resumen
        tiempo_base = (file_size_mb / 10) * 60  # segundos
        tiempo_resumen = 60  # segundos
        tiempo_total = int(tiempo_base + tiempo_resumen)

        if tiempo_total < 60:
            return f"~{tiempo_total} seg"
        else:
            minutos = tiempo_total // 60
            return f"~{minutos}-{minutos+1} min"
    
    def _calcular_estadisticas(self, transcripcion, resumen, video_name):
        """Calcula estadísticas del procesamiento"""
        return {
            "video": video_name,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "transcripcion": {
                "caracteres": len(transcripcion),
                "palabras": len(transcripcion.split()),
                "lineas": len(transcripcion.split('\n'))
            },
            "resumen": {
                "caracteres": len(resumen),
                "palabras": len(resumen.split()),
                "lineas": len(resumen.split('\n'))
            },
            "compresion": {
                "ratio_caracteres": len(resumen) / len(transcripcion) if transcripcion else 0,
                "ratio_palabras": len(resumen.split()) / len(transcripcion.split()) if transcripcion else 0
            }
        }
    
    def _formatear_transcripcion(self, transcripcion, stats):
        """Formatea la transcripción para mostrar"""
        return f"""## 📝 Transcripción Completa

{transcripcion}

---
**Estadísticas:** {stats['transcripcion']['palabras']:,} palabras | {stats['transcripcion']['caracteres']:,} caracteres
"""
    
    def _formatear_resumen_mejorado(self, resumen, analysis, stats):
        """Formatea el resumen con análisis mejorado"""
        # Generar bullet points del resumen
        bullet_text = "\n".join([f"- {point}" for point in analysis['bullet_points'][:5]])

        keywords_text = ", ".join([f"**{word}**" for word, _ in analysis['keywords'][:8]])

        return f"""## ✨ Resumen Generado

{resumen}

### 🔑 Puntos Clave

{bullet_text}

### 🏷️ Palabras Clave

{keywords_text}

---
**Estadísticas:** {stats['resumen']['palabras']:,} palabras | {stats['resumen']['caracteres']:,} caracteres
"""
    
    def _formatear_stats_html(self, stats, analysis):
        """Crea visualización HTML de estadísticas mejoradas"""
        ratio_car = stats['compresion']['ratio_caracteres'] * 100
        ratio_pal = stats['compresion']['ratio_palabras'] * 100

        keywords_html = ", ".join([f"<span style='background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; margin: 2px;'>{word}</span>"
                                   for word, _ in analysis['keywords'][:10]])

        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
            <h2 style="margin-top: 0;">📊 Estadísticas del Procesamiento</h2>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    <h3>🎤 Transcripción</h3>
                    <p><strong>Palabras:</strong> {stats['transcripcion']['palabras']:,}</p>
                    <p><strong>Caracteres:</strong> {stats['transcripcion']['caracteres']:,}</p>
                    <p><strong>Líneas:</strong> {stats['transcripcion']['lineas']:,}</p>
                </div>

                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    <h3>📝 Resumen</h3>
                    <p><strong>Palabras:</strong> {stats['resumen']['palabras']:,}</p>
                    <p><strong>Caracteres:</strong> {stats['resumen']['caracteres']:,}</p>
                    <p><strong>Líneas:</strong> {stats['resumen']['lineas']:,}</p>
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h3>🎯 Compresión</h3>
                <p><strong>Ratio de Caracteres:</strong> {ratio_car:.1f}% (reducción de {100-ratio_car:.1f}%)</p>
                <p><strong>Ratio de Palabras:</strong> {ratio_pal:.1f}% (reducción de {100-ratio_pal:.1f}%)</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h3>🏷️ Palabras Clave Detectadas</h3>
                <div style="margin-top: 10px;">
                    {keywords_html}
                </div>
            </div>

            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                ⏰ Procesado: {stats['timestamp']}
            </p>
        </div>
        """
        return html
    
    def _crear_json_output(self, video_name, transcripcion, resumen, stats, analysis):
        """Crea archivo JSON con todos los resultados"""
        return {
            "video": video_name,
            "titulo": analysis['title'],
            "timestamp": stats['timestamp'],
            "transcripcion": transcripcion,
            "resumen": resumen,
            "puntos_clave": analysis['bullet_points'],
            "palabras_clave": [{"palabra": word, "frecuencia": count} for word, count in analysis['keywords']],
            "estadisticas": stats
        }

    @staticmethod
    def mostrar_preview_video(video_file):
        """
        Muestra información del video subido

        Args:
            video_file: Archivo de video

        Returns:
            String con información formateada en Markdown
        """
        if video_file is None:
            return "📤 **Sube un video para ver su información**"

        try:
            from moviepy import VideoFileClip
            import os

            video_path = video_file.name if hasattr(video_file, 'name') else video_file
            video_name = Path(video_path).name
            file_size_mb = Path(video_path).stat().st_size / (1024 * 1024)

            # Obtener duración y resolución
            try:
                clip = VideoFileClip(video_path)
                duration = clip.duration
                duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"

                # Obtener resolución
                width, height = clip.size
                resolution = f"{width}x{height}"

                # FPS
                fps = clip.fps if hasattr(clip, 'fps') else "N/A"

                clip.close()
            except Exception as e:
                duration_str = "Desconocida"
                resolution = "Desconocida"
                fps = "N/A"

            # Calcular tamaño categoría
            if file_size_mb < 50:
                size_category = "Pequeño"
                processing_speed = "Rápido (~2-3 min)"
            elif file_size_mb < 150:
                size_category = "Mediano"
                processing_speed = "Moderado (~5-7 min)"
            else:
                size_category = "Grande"
                processing_speed = "Lento (~10-15 min)"

            info = f"""
## 📊 Información del Video

### 📁 Archivo
- **Nombre:** {video_name}
- **Tamaño:** {file_size_mb:.2f} MB ({size_category})
- **Ruta:** `{Path(video_path).parent.name}/{video_name}`

### 🎬 Propiedades
- **Duración:** {duration_str}
- **Resolución:** {resolution}
- **FPS:** {fps}

### ⚡ Estimación de Procesamiento
- **Tiempo aproximado:** {processing_speed}
- **Recomendación:** Modelo Whisper {'tiny/base' if file_size_mb < 100 else 'base/small'}

---

✅ **Video validado - Listo para procesar**

💡 **Tip:** Videos más pequeños se procesan más rápido
            """

            return info

        except Exception as e:
            return f"""
## ⚠️ Error al leer información del video

**Detalles:** {str(e)}

El video puede estar dañado o en un formato no compatible.

**Formatos soportados:** MP4, AVI, MOV, MKV, WebM
            """

    @staticmethod
    def obtener_historial_api():
        """
        Obtiene el historial desde la API

        Returns:
            String con historial formateado en Markdown
        """
        import requests

        try:
            # Conectar con la API REST
            api_url = os.getenv('API_URL', 'http://localhost:5000')
            response = requests.get(f'{api_url}/api/history?limit=10', timeout=15)

            if response.status_code == 200:
                data = response.json()

                if not data.get('success'):
                    return f"⚠️ **Error:** {data.get('error', 'Error desconocido')}"

                history = data.get('history', [])
                total = data.get('total', 0)

                if not history:
                    return """
# 📋 Historial de Procesamiento

No hay videos procesados todavía.

💡 **Tip:** Procesa tu primer video en la pestaña "🎬 Procesar Video"
                    """

                # Formatear historial
                md = f"# 📋 Historial de Procesamiento\n\n"
                md += f"**Total de videos procesados:** {total}\n"
                md += f"**Mostrando:** {len(history)} más recientes\n\n"
                md += "---\n\n"

                for i, item in enumerate(history, 1):
                    video = item['video']
                    trans = item.get('transcription')
                    summ = item.get('summary')

                    # Icono basado en estado
                    if summ:
                        status_icon = "✅"
                        status_text = "Completo"
                    elif trans:
                        status_icon = "📝"
                        status_text = "Solo transcripción"
                    else:
                        status_icon = "⚠️"
                        status_text = "Incompleto"

                    md += f"## {status_icon} {i}. {video['filename']}\n\n"

                    # Información del video
                    md += f"**Estado:** {status_text} | "
                    md += f"**Tamaño:** {video['size_mb']:.2f} MB | "
                    md += f"**Fecha:** {video['created_at']}\n\n"

                    # Información de transcripción
                    if trans:
                        md += f"### 📝 Transcripción\n"
                        md += f"- **Palabras:** {trans['word_count']:,}\n"
                        md += f"- **Caracteres:** {trans['char_count']:,}\n"
                        md += f"- **Idioma:** {trans['language']}\n"
                        md += f"- **Modelo:** {trans['model']}\n"
                        md += f"- **Tiempo:** {trans['processing_time']:.1f}s\n\n"

                    # Información de resumen
                    if summ:
                        md += f"### ✨ Resumen\n"
                        md += f"- **Palabras:** {summ['word_count']}\n"
                        md += f"- **Compresión:** {summ['compression_ratio']:.1%}\n"
                        md += f"- **Modelo:** {summ['model']}\n"
                        md += f"- **Tiempo:** {summ['processing_time']:.1f}s\n\n"

                    md += "---\n\n"

                return md

            else:
                return f"""
# ⚠️ Error al conectar con la API

**Código de estado:** {response.status_code}

**Posibles causas:**
- La API no está corriendo
- Puerto incorrecto (verificar puerto 5000)
- Error de red

**Solución:**
Asegúrate de que la API esté corriendo:
```bash
docker-compose up api
```
                """

        except requests.exceptions.ConnectionError:
            return """
# ⚠️ No se puede conectar con la API

La API REST no está disponible.

**Solución:**
1. Verifica que la API esté corriendo:
   ```bash
   docker-compose up api
   ```

2. Verifica que el puerto 5000 esté libre:
   ```bash
   netstat -ano | findstr :5000
   ```

💡 **Nota:** Si estás usando la interfaz sin Docker, la API debe estar corriendo en `http://localhost:5000`
            """

        except Exception as e:
            return f"""
# ❌ Error al obtener historial

**Detalles:** {str(e)}

**Tipo de error:** {type(e).__name__}

💡 Intenta refrescar el historial más tarde
            """


def crear_interfaz(modelo_path="models/mt5-video-summarizer-final"):
    """
    Crea la interfaz de Gradio
    
    Args:
        modelo_path: Ruta al modelo entrenado
    """
    app = VideoSummarizerWebApp(modelo_path)
    
    # Tema personalizado
    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
    )
    
    with gr.Blocks(
        theme=theme,
        title="Resumen de Videos Educativos",
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        """
    ) as demo:
        
        # Header
        gr.Markdown("""
        # 🎬 Sistema de Resumen Automático de Videos Educativos
        
        **Convierte videos largos en resúmenes concisos usando IA**
        
        Procesamiento en 3 pasos:
        1. 🎤 **Whisper** transcribe el audio del video
        2. 🧠 **mT5** genera un resumen inteligente
        3. 📊 Obtiene estadísticas y resultados descargables
        
        ---
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Panel de entrada
                gr.Markdown("## 📤 Subir Video")

                video_input = gr.Video(
                    label="Selecciona tu video",
                    sources=["upload"],
                )

                # Preview del video
                video_preview = gr.Markdown(
                    "📤 **Sube un video para ver su información**",
                    label="Vista Previa"
                )
                
                with gr.Accordion("⚙️ Configuración Avanzada", open=False):
                    whisper_model = gr.Dropdown(
                        choices=["tiny", "base", "small", "medium", "large"],
                        value="base",
                        label="Modelo Whisper",
                        info="Modelos más grandes = mejor calidad pero más lentos"
                    )
                    
                    max_length = gr.Slider(
                        minimum=50,
                        maximum=300,
                        value=150,
                        step=10,
                        label="Longitud máxima del resumen",
                        info="Número máximo de palabras"
                    )
                    
                    num_beams = gr.Slider(
                        minimum=1,
                        maximum=8,
                        value=4,
                        step=1,
                        label="Calidad de generación (beams)",
                        info="Más beams = mejor calidad pero más lento"
                    )
                
                procesar_btn = gr.Button(
                    "🚀 Procesar Video",
                    variant="primary",
                    size="lg"
                )
                
                status_output = gr.Markdown(
                    "ℹ️ Sube un video y haz clic en 'Procesar Video'",
                    label="Estado"
                )
            
            with gr.Column(scale=2):
                # Panel de resultados
                gr.Markdown("## 📋 Resultados")
                
                with gr.Tabs():
                    with gr.Tab("✨ Resumen"):
                        resumen_output = gr.Markdown(
                            "El resumen aparecerá aquí...",
                            label="Resumen Generado"
                        )
                    
                    with gr.Tab("📝 Transcripción"):
                        transcripcion_output = gr.Markdown(
                            "La transcripción completa aparecerá aquí...",
                            label="Transcripción"
                        )
                    
                    with gr.Tab("📊 Estadísticas"):
                        stats_output = gr.HTML(
                            "<p>Las estadísticas aparecerán aquí...</p>",
                            label="Estadísticas"
                        )

                    with gr.Tab("📋 Historial"):
                        gr.Markdown("""
                        ## 📋 Historial de Videos Procesados

                        Aquí puedes ver todos los videos que has procesado con la API REST.

                        **Nota:** Este historial se sincroniza con la base de datos del backend.
                        """)

                        historial_md = gr.Markdown(
                            "Cargando historial...",
                            label="Historial"
                        )

                        btn_refresh_history = gr.Button(
                            "🔄 Actualizar Historial",
                            variant="secondary"
                        )

                markdown_download = gr.File(
                    label="📥 Descargar informe completo (Markdown + JSON)",
                    visible=True
                )
        
        # Footer con información
        gr.Markdown("""
        ---
        ### 💡 Consejos de uso:
        
        - ✅ **Formatos soportados:** MP4, AVI, MOV, MKV, WebM
        - ✅ **Tamaño recomendado:** Videos de hasta 30 minutos
        - ✅ **Idioma:** Optimizado para español
        - ⚠️ **Primera ejecución:** Los modelos se descargan automáticamente (puede tomar 2-3 minutos)
        
        ### ⚙️ Recomendaciones de configuración:
        
        | Tipo de Video | Modelo Whisper | Calidad Generación |
        |--------------|----------------|-------------------|
        | Corto (<5 min) | base | 4 beams |
        | Medio (5-15 min) | base/small | 4 beams |
        | Largo (>15 min) | small/medium | 6 beams |
        
        ---
        **Desarrollado con ❤️ usando Whisper + mT5 + Gradio**
        """)
        
        # Conectar eventos

        # Evento 1: Preview automático al subir video
        video_input.change(
            fn=VideoSummarizerWebApp.mostrar_preview_video,
            inputs=[video_input],
            outputs=[video_preview]
        )

        # Evento 2: Procesamiento del video (con estados progresivos)
        procesar_btn.click(
            fn=app.procesar_video,
            inputs=[video_input, whisper_model, max_length, num_beams],
            outputs=[
                transcripcion_output,
                status_output,
                resumen_output,
                stats_output,
                markdown_download
            ]
        )

        # Evento 3: Cargar historial al abrir la interfaz
        demo.load(
            fn=VideoSummarizerWebApp.obtener_historial_api,
            inputs=[],
            outputs=[historial_md]
        )

        # Evento 4: Actualizar historial al hacer clic en el botón
        btn_refresh_history.click(
            fn=VideoSummarizerWebApp.obtener_historial_api,
            inputs=[],
            outputs=[historial_md]
        )

    return demo


def main():
    """Función principal para lanzar la aplicación"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Interfaz Web para Resumen de Videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Lanzar con configuración por defecto
  python src/web_app.py
  
  # Especificar ruta del modelo
  python src/web_app.py --modelo models/mi-modelo
  
  # Compartir públicamente (genera URL pública)
  python src/web_app.py --share
  
  # Cambiar puerto
  python src/web_app.py --port 7860
        """
    )
    
    parser.add_argument(
        '--modelo', '-m',
        default='models/mt5-video-summarizer-final',
        help='Ruta al modelo mT5 entrenado'
    )
    
    parser.add_argument(
        '--share', '-s',
        action='store_true',
        help='Crear URL pública compartible (requiere internet)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=7860,
        help='Puerto para el servidor web (default: 7860)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Modo debug con información detallada'
    )
    
    args = parser.parse_args()
    
    # Verificar que el modelo existe
    if not os.path.exists(args.modelo):
        print("=" * 70)
        print("⚠️  ADVERTENCIA: Modelo no encontrado")
        print("=" * 70)
        print(f"Ruta especificada: {args.modelo}")
        print("\nEl modelo se intentará cargar cuando proceses el primer video.")
        print("Asegúrate de tener un modelo entrenado en esa ubicación.")
        print("=" * 70)
        print()
    
    # Crear y lanzar interfaz
    print("=" * 70)
    print("🚀 INICIANDO INTERFAZ WEB")
    print("=" * 70)
    print(f"📊 Modelo: {args.modelo}")
    print(f"🌐 Puerto: {args.port}")
    print(f"🔗 Share: {'Sí' if args.share else 'No'}")
    print("=" * 70)
    
    demo = crear_interfaz(modelo_path=args.modelo)
    
    print("\n✅ Interfaz creada exitosamente")
    print(f"\n🌐 Abriendo en: http://localhost:{args.port}")
    
    if args.share:
        print("🔗 Generando URL pública compartible...")
    
    print("\n💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 70)
    print()
    
    # Lanzar
    try:
        demo.launch(
            server_name="0.0.0.0",
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            show_error=True
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor detenido por el usuario")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error al lanzar el servidor: {str(e)}")
        print("\n💡 Asegúrate de que el puerto no esté ocupado:")
        print(f"   netstat -ano | findstr :{args.port}")
        sys.exit(1)


if __name__ == "__main__":
    main()
