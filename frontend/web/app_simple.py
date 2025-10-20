"""
Interfaz Web Simplificada con Gradio
Solo transcripción (sin resumen por ahora)
"""
import gradio as gr
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.core.transcription import VideoTranscriber
from backend.core.summarization import VideoSummarizer

# Inicializar transcriptor y resumidor globales
transcriber = None
summarizer = None

def inicializar_whisper(model_size="base"):
    """Inicializa Whisper (lazy loading)"""
    global transcriber
    if transcriber is None:
        print(f"🔄 Cargando Whisper ({model_size})...")
        transcriber = VideoTranscriber(model_size=model_size, language="es", verbose=False)
        print("✅ Whisper cargado")
    return transcriber

def inicializar_summarizer():
    """Inicializa mT5 (lazy loading)"""
    global summarizer
    if summarizer is None:
        print("🔄 Cargando mT5 (google/mt5-small)...")
        summarizer = VideoSummarizer(model_path="google/mt5-small")
        print("✅ mT5 cargado")
    return summarizer

def procesar_video(video_file, whisper_model, generar_resumen, progress=gr.Progress()):
    """Procesa un video y genera transcripción (y opcionalmente resumen)"""
    if video_file is None:
        return "⚠️ Por favor sube un video", "", "", ""

    try:
        # Inicializar Whisper
        progress(0.1, desc="🔄 Inicializando Whisper...")
        inicializar_whisper(whisper_model)

        # Transcribir
        progress(0.3, desc="🎤 Transcribiendo audio...")
        video_path = video_file.name if hasattr(video_file, 'name') else video_file

        result = transcriber.transcribe_video(
            video_path=video_path,
            save_transcript=False,
            cleanup_audio=True
        )

        text = result.get('text', '')
        stats = result.get('stats', {})

        # Generar resumen si se solicitó
        summary = ""
        summary_md = ""

        if generar_resumen and text:
            progress(0.7, desc="✨ Generando resumen...")
            inicializar_summarizer()

            summary = summarizer.generate_summary(
                text,
                max_length=150,
                min_length=30
            )

            compression_ratio = len(summary.split()) / stats.get('total_words', 1)

            summary_md = f"""## ✨ Resumen Generado

{summary}

---
**Estadísticas:** {len(summary.split())} palabras | Ratio: {compression_ratio:.1%} del texto original
"""

        # Formatear resultados
        progress(1.0, desc="✅ Completado!")

        status = f"""
✅ **Procesamiento completado**

📁 Video: {Path(video_path).name}
📊 Palabras: {stats.get('total_words', 0):,}
📊 Caracteres: {stats.get('total_characters', 0):,}
{"✨ Resumen: Generado" if generar_resumen else ""}
        """

        transcription_md = f"""## 📝 Transcripción Completa

{text}

---
**Estadísticas:** {stats.get('total_words', 0):,} palabras | {stats.get('total_characters', 0):,} caracteres
"""

        # Primeros 500 caracteres
        preview = text[:500] + "..." if len(text) > 500 else text

        return status, transcription_md, summary_md, preview

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg, "", "", ""

# Crear interfaz
with gr.Blocks(
    title="Transcripción de Videos",
    theme=gr.themes.Soft(primary_hue="purple")
) as demo:

    gr.Markdown("""
    # 🎬 Sistema de Transcripción y Resumen de Videos

    **Convierte el audio de tus videos en texto y genera resúmenes automáticos**

    *Whisper (OpenAI) + mT5 (Google)*

    ---
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📤 Subir Video")

            video_input = gr.Video(
                label="Selecciona tu video",
                sources=["upload"],
            )

            whisper_model = gr.Dropdown(
                choices=["tiny", "base", "small", "medium"],
                value="tiny",
                label="Modelo Whisper",
                info="tiny = más rápido, medium = mejor calidad"
            )

            generar_resumen = gr.Checkbox(
                label="✨ Generar resumen automático (mT5)",
                value=True,
                info="Genera un resumen del contenido transcrito"
            )

            procesar_btn = gr.Button(
                "🚀 Procesar Video",
                variant="primary",
                size="lg"
            )

            status_output = gr.Markdown(
                "ℹ️ Sube un video y haz clic en 'Transcribir Video'",
                label="Estado"
            )

        with gr.Column(scale=2):
            gr.Markdown("## 📋 Resultados")

            with gr.Tabs():
                with gr.Tab("👁️ Vista Previa"):
                    preview_output = gr.Textbox(
                        label="Primeros 500 caracteres",
                        lines=10,
                        max_lines=15
                    )

                with gr.Tab("📝 Transcripción Completa"):
                    transcription_output = gr.Markdown(
                        "La transcripción completa aparecerá aquí...",
                        label="Transcripción"
                    )

                with gr.Tab("✨ Resumen"):
                    summary_output = gr.Markdown(
                        "El resumen aparecerá aquí si activas la opción...",
                        label="Resumen"
                    )

    gr.Markdown("""
    ---
    ### 💡 Consejos:

    - ✅ **Formatos:** MP4, AVI, MOV, MKV, WebM
    - ✅ **Modelo tiny:** Rápido, buena calidad
    - ✅ **Modelo base:** Equilibrio velocidad/calidad
    - ✅ **Modelo medium:** Mejor calidad, más lento
    - ✨ **Resumen:** Genera resumen automático con mT5
    - ⏱️ **Tiempo:** ~1-3 minutos por video de 10 min (en CPU)
    - ⏱️ **Tiempo resumen:** +30-60 segundos adicionales

    ---
    **Desarrollado con ❤️ usando Whisper + mT5 + Gradio**
    """)

    # Conectar eventos
    procesar_btn.click(
        fn=procesar_video,
        inputs=[video_input, whisper_model, generar_resumen],
        outputs=[status_output, transcription_output, summary_output, preview_output]
    )

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 INICIANDO INTERFAZ WEB - Transcripción y Resumen de Videos")
    print("=" * 70)
    print("\n✅ Interfaz creada exitosamente")
    print("\n📦 Funcionalidades:")
    print("   - Transcripción con Whisper")
    print("   - Resumen automático con mT5")
    print(f"\n🌐 Abriendo en: http://localhost:7860")
    print("\n💡 Presiona Ctrl+C para detener")
    print("=" * 70)
    print()

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
