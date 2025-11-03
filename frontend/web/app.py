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
    from frontend.web.icons import icon, styled_icon
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("\nAsegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class VideoSummarizerWebApp:
    """
    Aplicación web para resumir videos
    """

    @staticmethod
    def _format_status_message(content, msg_type="info"):
        """
        Formatea un mensaje de estado con iconos y estilos

        Args:
            content: Contenido del mensaje (puede incluir HTML)
            msg_type: Tipo de mensaje (info, success, warning, error, processing)
        """
        styles = {
            "info": {"bg": "#eff6ff", "border": "#3b82f6", "icon": icon('info', 20, '#3b82f6')},
            "success": {"bg": "#d1fae5", "border": "#10b981", "icon": styled_icon('check', 18, '#10b981', 'transparent')},
            "warning": {"bg": "#fef3c7", "border": "#f59e0b", "icon": styled_icon('alert-triangle', 18, '#f59e0b', 'transparent')},
            "error": {"bg": "#fee2e2", "border": "#ef4444", "icon": styled_icon('x', 18, '#ef4444', 'transparent')},
            "processing": {"bg": "#f3e8ff", "border": "#8b5cf6", "icon": icon('loader', 20, '#8b5cf6', 'icon-spin')},
        }

        style = styles.get(msg_type, styles["info"])

        return f"""
        <div style="padding: 16px; background: {style['bg']}; border-left: 4px solid {style['border']};
                    border-radius: 6px; margin: 8px 0; color: #1e293b;">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="flex-shrink: 0; margin-top: 2px;">
                    {style['icon']}
                </div>
                <div style="flex: 1;">
                    {content}
                </div>
            </div>
        </div>
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
            return f"{styled_icon('check', 16, '#10b981', '#d1fae5')} Modelos ya inicializados"

        try:
            print(f"🔄 Inicializando Whisper...")
            self.transcriber = VideoTranscriber(model_size=whisper_model)

            print(f"🔄 Inicializando Resumidor Híbrido...")
            # Intentar cargar modelo abstractivo
            try:
                abstractive = VideoSummarizer(model_path=self.modelo_path)
                print(f"   ✅ Modelo abstractivo cargado")
            except Exception as e:
                print(f"   ⚠️ No se pudo cargar modelo abstractivo: {e}")
                abstractive = None

            # Crear resumidor híbrido (usa extractivo como fallback)
            self.summarizer = HybridSummarizer(abstractive_summarizer=abstractive)

            self.inicializado = True
            return f"{styled_icon('check', 16, '#10b981', '#d1fae5')} Modelos inicializados correctamente"

        except Exception as e:
            return f"{styled_icon('x', 16, '#ef4444', '#fee2e2')} Error al inicializar modelos: {str(e)}"
    
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
            return None, self._format_status_message("<strong>Por favor sube un video</strong>", "warning"), None, None, None

        try:
            import time
            start_time = time.time()

            # Obtener información del video
            video_path = video_file.name if hasattr(video_file, 'name') else video_file
            video_name = Path(video_path).name
            file_size_mb = Path(video_path).stat().st_size / (1024 * 1024)

            # PASO 0: Validación
            progress(0, desc="🔍 Validando archivo...")
            estado_inicial = self._format_status_message(f"""
                <h3 style="margin: 0 0 12px 0; display: flex; align-items: center; gap: 8px;">
                    {icon('search', 22, '#8b5cf6')}
                    <span>Validando archivo...</span>
                </h3>
                <div style="display: grid; gap: 8px; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('folder', 18, '#6366f1')}
                        <span><strong>Archivo:</strong> {video_name}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('bar-chart', 18, '#6366f1')}
                        <span><strong>Tamaño:</strong> {file_size_mb:.2f} MB</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('mic', 18, '#8b5cf6')}
                        <span><strong>Modelo Whisper:</strong> {whisper_model}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('clock', 18, '#3b82f6')}
                        <span><strong>Tiempo estimado:</strong> {self._estimar_tiempo(file_size_mb)}</span>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; padding: 8px; background: rgba(139, 92, 246, 0.1); border-radius: 4px;">
                    {icon('loader', 18, '#8b5cf6', 'icon-spin')}
                    <em>Iniciando procesamiento...</em>
                </div>
            """, "processing")
            yield None, estado_inicial, None, None, None
            time.sleep(0.5)

            # Inicializar modelos
            progress(0.05, desc="🔧 Inicializando modelos...")
            estado_init = self._format_status_message(f"""
                <h3 style="margin: 0 0 12px 0; display: flex; align-items: center; gap: 8px;">
                    {icon('wrench', 22, '#8b5cf6')}
                    <span>Inicializando modelos de IA...</span>
                </h3>
                <div style="display: grid; gap: 8px; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('folder', 18, '#6366f1')}
                        <span>Video: {video_name} ({file_size_mb:.2f} MB)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('mic', 18, '#8b5cf6')}
                        <span>Cargando Whisper {whisper_model}...</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('brain', 18, '#a855f7')}
                        <span>Preparando sistema de resumen híbrido...</span>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; padding: 8px; background: rgba(245, 158, 11, 0.1); border-radius: 4px;">
                    {icon('lightbulb', 18, '#f59e0b')}
                    <em>Cargando modelos de IA...</em>
                </div>
            """, "processing")
            yield None, estado_init, None, None, None

            init_msg = self.inicializar_modelos(whisper_model)
            if 'Error' in init_msg:
                yield None, init_msg, None, None, None
                return

            # PASO 1: Transcripción (5-60%)
            progress(0.10, desc="🎬 Extrayendo audio...")
            estado_audio = f"""
{icon('film', 20, '#8b5cf6')} **[Paso 1/3] Extrayendo audio del video...**

{icon('folder', 18, '#6366f1')} Video: {video_name}
{icon('volume-2', 18, '#8b5cf6')} Convirtiendo a formato de audio optimizado...

{icon('clock', 18, '#3b82f6')} *Esto puede tardar según el tamaño del video*
            """
            yield None, estado_audio, None, None, None

            progress(0.20, desc="🎤 Transcribiendo con Whisper...")
            estado_transcribe = f"""
{icon('mic', 20, '#8b5cf6')} **[Paso 1/3] Transcribiendo audio con Whisper...**

{icon('brain', 18, '#a855f7')} Modelo: Whisper {whisper_model}
{icon('globe', 18, '#3b82f6')} Idioma: Español
{icon('loader', 18, '#8b5cf6')} Procesando audio...

{icon('lightbulb', 18, '#f59e0b')} *Whisper está convirtiendo el audio en texto*
            """
            yield None, estado_transcribe, None, None, None

            print(f"\n[1/3] Transcribiendo: {video_name}")
            transcript_result = self.transcriber.transcribe_video(video_path, save_transcript=False, cleanup_audio=True)
            transcripcion = transcript_result.get('text', '')

            if not transcripcion or len(transcripcion.strip()) < 50:
                yield None, self._format_status_message(
                    "<strong>Transcripción muy corta o vacía.</strong><br>Verifica que el video tenga audio claro y audible.",
                    "error"
                ), None, None, None
                return

            # Transcripción completada
            progress(0.60, desc="✅ Transcripción completada")
            palabras_transcritas = len(transcripcion.split())
            estado_trans_ok = f"""
{styled_icon('check', 18, '#10b981', '#d1fae5')} **[Paso 1/3] Transcripción completada**

{icon('file-text', 18, '#6366f1')} **Resultado:**
- Palabras: {palabras_transcritas:,}
- Caracteres: {len(transcripcion):,}

{icon('target', 18, '#10b981')} Texto capturado correctamente
            """
            yield None, estado_trans_ok, None, None, None
            time.sleep(0.5)

            # PASO 2: Resumen (60-85%)
            progress(0.65, desc="🧠 Analizando texto...")
            estado_analisis = f"""
{icon('brain', 20, '#a855f7')} **[Paso 2/3] Analizando texto...**

{icon('bar-chart', 18, '#6366f1')} Identificando palabras clave...
{icon('list', 18, '#6366f1')} Extrayendo puntos principales...
{icon('search', 18, '#8b5cf6')} Preparando para resumen...

{icon('lightbulb', 18, '#f59e0b')} *Analizando {palabras_transcritas:,} palabras*
            """
            yield None, estado_analisis, None, None, None

            print(f"[2/4] Analizando texto...")
            analysis = self.analyzer.analyze_text(transcripcion)

            progress(0.72, desc="✨ Generando resumen...")
            estado_resumen = f"""
{icon('sparkles', 20, '#a855f7')} **[Paso 2/3] Generando resumen inteligente...**

{icon('brain', 18, '#a855f7')} Sistema híbrido activado:
- Intentando resumen abstractivo (mT5)...
- Fallback extractivo disponible

{icon('bar-chart', 18, '#6366f1')} Procesando {palabras_transcritas:,} palabras
{icon('target', 18, '#10b981')} Objetivo: ~{int(palabras_transcritas * 0.25)} palabras

{icon('clock', 18, '#3b82f6')} *Esto puede tardar 30-60 segundos*
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
{icon('bar-chart', 20, '#6366f1')} **[Paso 3/3] Finalizando procesamiento...**

{icon('trending-up', 18, '#6366f1')} Calculando estadísticas...
{icon('folder', 18, '#6366f1')} Preparando archivos descargables...
{icon('sparkles', 18, '#a855f7')} Generando informe completo...

{icon('clock', 18, '#3b82f6')} Casi listo...
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

            mensaje_exito = self._format_status_message(f"""
                <h3 style="margin: 0 0 16px 0; display: flex; align-items: center; gap: 10px; color: #065f46;">
                    {styled_icon('party-popper', 22, '#10b981', 'transparent')}
                    <span style="color: #065f46;">¡Proceso completado exitosamente!</span>
                </h3>

                <div style="display: grid; gap: 10px; margin-bottom: 16px; padding: 12px; background: rgba(255,255,255,0.7); border-radius: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('folder', 18, '#6366f1')}
                        <span style="color: #1e293b;"><strong>Video:</strong> {Path(video_path).name}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('bookmark', 18, '#8b5cf6')}
                        <span style="color: #1e293b;"><strong>Título:</strong> {analysis['title']}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        {icon('clock', 18, '#3b82f6')}
                        <span style="color: #1e293b;"><strong>Tiempo total:</strong> {tiempo_str}</span>
                    </div>
                </div>

                <div style="margin-bottom: 16px; color: #1e293b;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        {icon('bar-chart', 20, '#6366f1')}
                        <strong style="color: #1e293b;">Resumen de resultados:</strong>
                    </div>
                    <ul style="margin: 0; padding-left: 28px; color: #1e293b;">
                        <li>Transcripción: <strong>{stats['transcripcion']['palabras']:,}</strong> palabras</li>
                        <li>Resumen: <strong>{stats['resumen']['palabras']:,}</strong> palabras</li>
                        <li>Compresión: <strong>{(1-stats['compresion']['ratio_palabras'])*100:.1f}%</strong> reducción</li>
                    </ul>
                </div>

                <div style="margin-bottom: 12px; color: #1e293b;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        {icon('download', 20, '#10b981')}
                        <strong style="color: #1e293b;">Archivos descargables:</strong>
                    </div>
                    <div style="display: grid; gap: 6px; padding-left: 28px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {styled_icon('check', 14, '#10b981', 'transparent')}
                            <span style="color: #1e293b;">Informe Markdown completo</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {styled_icon('check', 14, '#10b981', 'transparent')}
                            <span style="color: #1e293b;">Datos JSON estructurados</span>
                        </div>
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 8px; padding: 10px; background: rgba(245, 158, 11, 0.15); border-radius: 4px;">
                    {icon('lightbulb', 18, '#f59e0b')}
                    <em style="color: #78350f;">Puedes descargar los archivos desde el botón de descarga más abajo</em>
                </div>
            """, "success")

            yield (
                resultado_transcripcion,
                mensaje_exito,
                resultado_resumen,
                resultado_stats,
                md_path
            )

        except Exception as e:
            error_msg = self._format_status_message(f"""
                <h3 style="margin: 0 0 12px 0; display: flex; align-items: center; gap: 8px;">
                    <span>Error durante el procesamiento</span>
                </h3>

                <div style="margin-bottom: 12px; padding: 10px; background: rgba(255,255,255,0.5); border-radius: 4px;">
                    <strong>Detalles:</strong>
                    <p style="margin: 8px 0 0 0;">{str(e)}</p>
                </div>

                <div style="margin-bottom: 12px;">
                    <strong>Posibles soluciones:</strong>
                    <ul style="margin: 8px 0 0 0;">
                        <li>Verifica que el video tenga audio</li>
                        <li>Prueba con un video más pequeño</li>
                        <li>Intenta con un modelo Whisper diferente</li>
                    </ul>
                </div>

                <details style="margin-top: 12px;">
                    <summary style="cursor: pointer; padding: 8px; background: rgba(255,255,255,0.3); border-radius: 4px;">
                        <strong>Información técnica</strong>
                    </summary>
                    <pre style="margin: 8px 0 0 0; padding: 12px; background: rgba(0,0,0,0.05); border-radius: 4px; overflow-x: auto; font-size: 0.85em;">{traceback.format_exc()}</pre>
                </details>
            """, "error")
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
        return f"""## {icon('file-text', 22, '#6366f1')} Transcripción Completa

{transcripcion}

---
**Estadísticas:** {stats['transcripcion']['palabras']:,} palabras | {stats['transcripcion']['caracteres']:,} caracteres
"""
    
    def _formatear_resumen_mejorado(self, resumen, analysis, stats):
        """Formatea el resumen con análisis mejorado"""
        # Generar bullet points del resumen
        bullet_text = "\n".join([f"- {point}" for point in analysis['bullet_points'][:5]])

        keywords_text = ", ".join([f"**{word}**" for word, _ in analysis['keywords'][:8]])

        return f"""## {icon('sparkles', 22, '#a855f7')} Resumen Generado

{resumen}

### {icon('key', 20, '#6366f1')} Puntos Clave

{bullet_text}

### {icon('tag', 20, '#8b5cf6')} Palabras Clave

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
            <h2 style="margin-top: 0;">{icon('bar-chart', 24, '#ffffff')} Estadísticas del Procesamiento</h2>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    <h3>{icon('mic', 22, '#ffffff')} Transcripción</h3>
                    <p><strong>Palabras:</strong> {stats['transcripcion']['palabras']:,}</p>
                    <p><strong>Caracteres:</strong> {stats['transcripcion']['caracteres']:,}</p>
                    <p><strong>Líneas:</strong> {stats['transcripcion']['lineas']:,}</p>
                </div>

                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                    <h3>{icon('file-text', 22, '#ffffff')} Resumen</h3>
                    <p><strong>Palabras:</strong> {stats['resumen']['palabras']:,}</p>
                    <p><strong>Caracteres:</strong> {stats['resumen']['caracteres']:,}</p>
                    <p><strong>Líneas:</strong> {stats['resumen']['lineas']:,}</p>
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h3>{icon('target', 22, '#ffffff')} Compresión</h3>
                <p><strong>Ratio de Caracteres:</strong> {ratio_car:.1f}% (reducción de {100-ratio_car:.1f}%)</p>
                <p><strong>Ratio de Palabras:</strong> {ratio_pal:.1f}% (reducción de {100-ratio_pal:.1f}%)</p>
            </div>

            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h3>{icon('tag', 22, '#ffffff')} Palabras Clave Detectadas</h3>
                <div style="margin-top: 10px;">
                    {keywords_html}
                </div>
            </div>

            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                {icon('clock', 18, '#ffffff')} Procesado: {stats['timestamp']}
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
            return f"{styled_icon('upload', 20, '#8b5cf6', '#f3e8ff')} **Sube un video para ver su información**"

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
## {icon('bar-chart', 22, '#6366f1')} Información del Video

### {icon('folder', 20, '#8b5cf6')} Archivo
- **Nombre:** {video_name}
- **Tamaño:** {file_size_mb:.2f} MB ({size_category})
- **Ruta:** `{Path(video_path).parent.name}/{video_name}`

### {icon('film', 20, '#a855f7')} Propiedades
- **Duración:** {duration_str}
- **Resolución:** {resolution}
- **FPS:** {fps}

### {icon('activity', 20, '#3b82f6')} Estimación de Procesamiento
- **Tiempo aproximado:** {processing_speed}
- **Recomendación:** Modelo Whisper {'tiny/base' if file_size_mb < 100 else 'base/small'}

---

{styled_icon('check', 20, '#10b981', '#d1fae5')} **Video validado - Listo para procesar**

{icon('lightbulb', 18, '#f59e0b')} **Tip:** Videos más pequeños se procesan más rápido
            """

            return info

        except Exception as e:
            return f"""
## {styled_icon('alert-triangle', 22, '#f59e0b', '#fef3c7')} Error al leer información del video

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
                    return f"{styled_icon('alert-triangle', 20, '#f59e0b', '#fef3c7')} **Error:** {data.get('error', 'Error desconocido')}"

                history = data.get('history', [])
                total = data.get('total', 0)

                if not history:
                    return f"""
# {icon('history', 24, '#6366f1')} Historial de Procesamiento

No hay videos procesados todavía.

{icon('lightbulb', 18, '#f59e0b')} **Tip:** Procesa tu primer video en la pestaña "{icon('film', 18, '#8b5cf6')} Procesar Video"
                    """

                # Formatear historial
                md = f"# {icon('history', 24, '#6366f1')} Historial de Procesamiento\n\n"
                md += f"**Total de videos procesados:** {total}\n"
                md += f"**Mostrando:** {len(history)} más recientes\n\n"
                md += "---\n\n"

                for i, item in enumerate(history, 1):
                    video = item['video']
                    trans = item.get('transcription')
                    summ = item.get('summary')

                    # Icono basado en estado
                    if summ:
                        status_icon = icon('check', 18, '#10b981')
                        status_text = "Completo"
                    elif trans:
                        status_icon = icon('file-text', 18, '#6366f1')
                        status_text = "Solo transcripción"
                    else:
                        status_icon = icon('alert-triangle', 18, '#f59e0b')
                        status_text = "Incompleto"

                    md += f"## {status_icon} {i}. {video['filename']}\n\n"

                    # Información del video
                    md += f"**Estado:** {status_text} | "
                    md += f"**Tamaño:** {video['size_mb']:.2f} MB | "
                    md += f"**Fecha:** {video['created_at']}\n\n"

                    # Información de transcripción
                    if trans:
                        md += f"### {icon('file-text', 20, '#6366f1')} Transcripción\n"
                        md += f"- **Palabras:** {trans['word_count']:,}\n"
                        md += f"- **Caracteres:** {trans['char_count']:,}\n"
                        md += f"- **Idioma:** {trans['language']}\n"
                        md += f"- **Modelo:** {trans['model']}\n"
                        md += f"- **Tiempo:** {trans['processing_time']:.1f}s\n\n"

                    # Información de resumen
                    if summ:
                        md += f"### {icon('sparkles', 20, '#a855f7')} Resumen\n"
                        md += f"- **Palabras:** {summ['word_count']}\n"
                        md += f"- **Compresión:** {summ['compression_ratio']:.1%}\n"
                        md += f"- **Modelo:** {summ['model']}\n"
                        md += f"- **Tiempo:** {summ['processing_time']:.1f}s\n\n"

                    md += "---\n\n"

                return md

            else:
                return f"""
# {styled_icon('alert-triangle', 24, '#f59e0b', '#fef3c7')} Error al conectar con la API

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
            return f"""
# {styled_icon('alert-triangle', 24, '#f59e0b', '#fef3c7')} No se puede conectar con la API

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

{icon('lightbulb', 18, '#f59e0b')} **Nota:** Si estás usando la interfaz sin Docker, la API debe estar corriendo en `http://localhost:5000`
            """

        except Exception as e:
            return f"""
# {styled_icon('x', 24, '#ef4444', '#fee2e2')} Error al obtener historial

**Detalles:** {str(e)}

**Tipo de error:** {type(e).__name__}

{icon('lightbulb', 18, '#f59e0b')} Intenta refrescar el historial más tarde
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
        .icon {
            display: inline-block;
            vertical-align: middle;
            flex-shrink: 0;
        }
        .icon-spin {
            animation: icon-spin 1s linear infinite;
        }
        @keyframes icon-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        """
    ) as demo:
        
        # Header
        gr.HTML(f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0;">
                {icon('film', 32, '#8b5cf6')}
                <span>Sistema de Resumen Automático de Videos Educativos</span>
            </h1>
            <p style="font-size: 1.1em; margin: 16px 0; color: #64748b;">
                <strong>Convierte videos largos en resúmenes concisos usando IA</strong>
            </p>

            <div style="display: flex; justify-content: center; gap: 40px; margin: 24px 0; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: #f3e8ff; padding: 8px; border-radius: 8px; display: flex;">
                        {icon('mic', 20, '#8b5cf6')}
                    </span>
                    <span><strong>Whisper</strong> transcribe el audio</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: #f3e8ff; padding: 8px; border-radius: 8px; display: flex;">
                        {icon('sparkles', 20, '#a855f7')}
                    </span>
                    <span><strong>mT5</strong> genera resumen inteligente</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: #d1fae5; padding: 8px; border-radius: 8px; display: flex;">
                        {icon('download', 20, '#10b981')}
                    </span>
                    <span>Resultados descargables</span>
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Panel de entrada
                gr.HTML(f"""
                <div style="margin-bottom: 16px;">
                    <h2 style="display: flex; align-items: center; gap: 10px; margin: 0; font-size: 1.5em;">
                        {icon('upload', 24, '#8b5cf6')}
                        <span>Subir Video</span>
                    </h2>
                </div>
                """)

                video_input = gr.Video(
                    label="Selecciona tu video",
                    sources=["upload"],
                )

                # Preview del video
                video_preview = gr.Markdown(
                    "**Sube un video para ver su información**",
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

                status_output = gr.HTML(
                    f"""<div style="padding: 12px; background: #eff6ff; border-left: 4px solid #3b82f6; border-radius: 6px; display: flex; align-items: center; gap: 10px;">
                        {icon('info', 20, '#3b82f6')}
                        <span style="color: #1e293b; font-weight: 500;">Sube un video y haz clic en 'Procesar Video'</span>
                    </div>""",
                    label="Estado"
                )
            
            with gr.Column(scale=2):
                # Panel de resultados
                gr.HTML(f"""
                <div style="margin-bottom: 16px;">
                    <h2 style="display: flex; align-items: center; gap: 10px; margin: 0; font-size: 1.5em;">
                        {icon('bar-chart', 24, '#6366f1')}
                        <span>Resultados</span>
                    </h2>
                </div>
                """)

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
                        gr.HTML(f"""
                        <div style="padding: 16px;">
                            <h2 style="display: flex; align-items: center; gap: 10px; margin: 0 0 16px 0;">
                                {icon('history', 24, '#6366f1')}
                                <span>Historial de Videos Procesados</span>
                            </h2>
                            <p>Aquí puedes ver todos los videos que has procesado con la API REST.</p>
                            <p><strong>Nota:</strong> Este historial se sincroniza con la base de datos del backend.</p>
                        </div>
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
        ### Consejos de uso:

        - **Formatos soportados:** MP4, AVI, MOV, MKV, WebM
        - **Tamaño recomendado:** Videos de hasta 30 minutos
        - **Idioma:** Optimizado para español

        ### Recomendaciones de configuración:

        | Tipo de Video | Modelo Whisper | Calidad Generación |
        |--------------|----------------|-------------------|
        | Corto (<5 min) | base | 4 beams |
        | Medio (5-15 min) | base/small | 4 beams |
        | Largo (>15 min) | small/medium | 6 beams |

        ---
        **Desarrollado usando Whisper + mT5 + Gradio**
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
