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

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar nuestros módulos
try:
    from transcribe_video import VideoTranscriber
    from inference import VideoSummarizer
except ImportError:
    print("⚠️ Asegúrate de que transcribe_video.py e inference.py estén en el mismo directorio")
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
            
            print("🔄 Inicializando mT5...")
            self.summarizer = VideoSummarizer(model_path=self.modelo_path)
            
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
            return None, "⚠️ Por favor sube un video", None, None
        
        try:
            # Inicializar modelos si es necesario
            progress(0.1, desc="🔄 Inicializando modelos...")
            init_msg = self.inicializar_modelos(whisper_model)
            if "❌" in init_msg:
                return None, init_msg, None, None
            
            # Obtener ruta del video
            video_path = video_file.name if hasattr(video_file, 'name') else video_file
            video_name = Path(video_path).stem
            
            # PASO 1: Transcripción
            progress(0.3, desc="🎤 Transcribiendo audio...")
            print(f"\n[1/3] Transcribiendo: {Path(video_path).name}")
            transcripcion = self.transcriber.transcribe(video_path)
            
            if not transcripcion or len(transcripcion.strip()) < 50:
                return None, "❌ Transcripción muy corta o vacía. Verifica que el video tenga audio.", None, None
            
            # PASO 2: Resumen
            progress(0.6, desc="📝 Generando resumen...")
            print(f"[2/3] Generando resumen...")
            resumen = self.summarizer.generate_summary(
                transcripcion,
                max_length=max_length,
                num_beams=num_beams
            )
            
            # PASO 3: Estadísticas
            progress(0.9, desc="📊 Calculando estadísticas...")
            print(f"[3/3] Calculando estadísticas...")
            
            stats = self._calcular_estadisticas(transcripcion, resumen, video_name)
            
            # Formatear resultados para mostrar
            resultado_transcripcion = self._formatear_transcripcion(transcripcion, stats)
            resultado_resumen = self._formatear_resumen(resumen, stats)
            resultado_stats = self._formatear_stats_html(stats)
            
            # Crear archivo JSON descargable
            json_output = self._crear_json_output(video_name, transcripcion, resumen, stats)
            json_path = f"resultados_{video_name}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)
            
            progress(1.0, desc="✅ Completado!")
            
            mensaje_exito = f"""
✅ **Proceso completado exitosamente**

📁 Video: {Path(video_path).name}
⏱️ Procesado en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            return (
                resultado_transcripcion,
                mensaje_exito,
                resultado_resumen,
                resultado_stats,
                json_path
            )
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return None, error_msg, None, None, None
    
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
    
    def _formatear_resumen(self, resumen, stats):
        """Formatea el resumen para mostrar"""
        return f"""## ✨ Resumen Generado

{resumen}

---
**Estadísticas:** {stats['resumen']['palabras']:,} palabras | {stats['resumen']['caracteres']:,} caracteres
"""
    
    def _formatear_stats_html(self, stats):
        """Crea visualización HTML de estadísticas"""
        ratio_car = stats['compresion']['ratio_caracteres'] * 100
        ratio_pal = stats['compresion']['ratio_palabras'] * 100
        
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
            
            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                ⏰ Procesado: {stats['timestamp']}
            </p>
        </div>
        """
        return html
    
    def _crear_json_output(self, video_name, transcripcion, resumen, stats):
        """Crea archivo JSON con todos los resultados"""
        return {
            "video": video_name,
            "timestamp": stats['timestamp'],
            "transcripcion": transcripcion,
            "resumen": resumen,
            "estadisticas": stats
        }


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
                
                json_download = gr.File(
                    label="📥 Descargar resultados (JSON)",
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
        procesar_btn.click(
            fn=app.procesar_video,
            inputs=[video_input, whisper_model, max_length, num_beams],
            outputs=[
                transcripcion_output,
                status_output,
                resumen_output,
                stats_output,
                json_download
            ]
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
