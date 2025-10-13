"""
Script de Prueba de Whisper con Audio
Prueba la transcripción de Whisper con un audio de prueba

Autor: Sistema de Resumen de Videos Educativos
Fecha: Octubre 2025
"""

import sys
import os
from pathlib import Path


def crear_audio_prueba():
    """
    Crea un audio de prueba usando TTS (Text-to-Speech) de Windows
    Solo funciona en Windows
    """
    try:
        import pyttsx3
        
        print("🎤 Creando audio de prueba con TTS...")
        
        # Inicializar TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        # Texto de prueba
        texto = """
        Hola, este es un audio de prueba para el sistema de resumen de videos educativos.
        Estamos probando la transcripción con Whisper.
        Si escuchas esto correctamente, el sistema está funcionando bien.
        """
        
        # Guardar audio
        audio_path = "test_audio.mp3"
        engine.save_to_file(texto, audio_path)
        engine.runAndWait()
        
        print(f"✅ Audio creado: {audio_path}")
        return audio_path
        
    except Exception as e:
        print(f"⚠️  No se pudo crear audio de prueba: {str(e)}")
        print("💡 Usa tu propio archivo de audio para probar")
        return None


def probar_whisper_con_audio(audio_path, model_size="base"):
    """
    Prueba Whisper con un archivo de audio
    
    Args:
        audio_path: Ruta al archivo de audio
        model_size: Tamaño del modelo (tiny, base, small, medium, large)
    """
    print("=" * 70)
    print("🎤 PRUEBA DE WHISPER CON AUDIO")
    print("=" * 70)
    
    # Verificar que el audio existe
    if not os.path.exists(audio_path):
        print(f"❌ Audio no encontrado: {audio_path}")
        print("\n💡 Por favor proporciona un archivo de audio válido:")
        print("   python src/test_whisper_audio.py --audio tu_audio.mp3")
        return False
    
    print(f"\n📁 Audio: {Path(audio_path).name}")
    print(f"🧠 Modelo: {model_size}")
    
    try:
        # Importar whisper
        print("\n[1/3] Importando Whisper...")
        import whisper
        print("✅ Whisper importado")
        
        # Cargar modelo
        print(f"\n[2/3] Cargando modelo '{model_size}'...")
        print("   (Esto puede tomar 1-2 minutos la primera vez)")
        model = whisper.load_model(model_size)
        print("✅ Modelo cargado")
        
        # Transcribir
        print(f"\n[3/3] Transcribiendo audio...")
        print("   ⏳ Esto puede tomar algunos segundos...")
        
        result = model.transcribe(
            audio_path,
            language="es",  # Español
            verbose=False
        )
        
        texto = result['text']
        segmentos = result.get('segments', [])
        
        # Mostrar resultados
        print("\n" + "=" * 70)
        print("✅ TRANSCRIPCIÓN COMPLETADA")
        print("=" * 70)
        print(f"\n📝 Texto transcrito:")
        print("-" * 70)
        print(texto)
        print("-" * 70)
        
        print(f"\n📊 Estadísticas:")
        print(f"   - Caracteres: {len(texto):,}")
        print(f"   - Palabras: {len(texto.split()):,}")
        print(f"   - Segmentos: {len(segmentos)}")
        
        if segmentos:
            print(f"\n🎯 Primeros 3 segmentos:")
            for i, seg in enumerate(segmentos[:3], 1):
                inicio = seg.get('start', 0)
                fin = seg.get('end', 0)
                texto_seg = seg.get('text', '').strip()
                print(f"   [{inicio:.1f}s - {fin:.1f}s]: {texto_seg}")
        
        print("\n" + "=" * 70)
        print("🎉 ¡WHISPER FUNCIONA CORRECTAMENTE!")
        print("=" * 70)
        print("\n💡 Próximos pasos:")
        print("   1. Prueba con un video real")
        print("   2. Ejecuta el pipeline completo:")
        print("      python src/pipeline_completo.py --video tu_video.mp4 --modelo models/mt5-video-summarizer-final")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante transcripción: {str(e)}")
        import traceback
        print("\n📋 Traceback:")
        print(traceback.format_exc())
        return False


def probar_whisper_con_video(video_path, model_size="base"):
    """
    Prueba Whisper extrayendo audio de un video
    
    Args:
        video_path: Ruta al video
        model_size: Tamaño del modelo Whisper
    """
    print("=" * 70)
    print("🎬 PRUEBA DE WHISPER CON VIDEO")
    print("=" * 70)
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return False
    
    print(f"\n📁 Video: {Path(video_path).name}")
    
    try:
        # Importar módulos necesarios
        print("\n[1/4] Importando módulos...")
        from moviepy.editor import VideoFileClip
        import whisper
        print("✅ Módulos importados")
        
        # Extraer audio
        print("\n[2/4] Extrayendo audio del video...")
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.mp3"
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        print(f"✅ Audio extraído: {audio_path}")
        
        # Cargar modelo Whisper
        print(f"\n[3/4] Cargando modelo Whisper '{model_size}'...")
        model = whisper.load_model(model_size)
        print("✅ Modelo cargado")
        
        # Transcribir
        print(f"\n[4/4] Transcribiendo...")
        result = model.transcribe(audio_path, language="es", verbose=False)
        texto = result['text']
        
        # Limpiar audio temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        # Mostrar resultados
        print("\n" + "=" * 70)
        print("✅ TRANSCRIPCIÓN COMPLETADA")
        print("=" * 70)
        print(f"\n📝 Transcripción (primeros 500 caracteres):")
        print("-" * 70)
        preview = texto[:500] + "..." if len(texto) > 500 else texto
        print(preview)
        print("-" * 70)
        
        print(f"\n📊 Estadísticas:")
        print(f"   - Caracteres totales: {len(texto):,}")
        print(f"   - Palabras totales: {len(texto.split()):,}")
        
        print("\n" + "=" * 70)
        print("🎉 ¡WHISPER CON VIDEO FUNCIONA CORRECTAMENTE!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


def main():
    """Función principal con opciones"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Prueba de Whisper con audio o video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Probar con archivo de audio
  python src/test_whisper_audio.py --audio mi_audio.mp3
  
  # Probar con video (extrae audio automáticamente)
  python src/test_whisper_audio.py --video mi_video.mp4
  
  # Usar modelo Whisper más grande
  python src/test_whisper_audio.py --audio mi_audio.mp3 --modelo small
  
  # Crear audio de prueba automático (solo Windows)
  python src/test_whisper_audio.py --crear-audio
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--audio', '-a',
        help='Ruta al archivo de audio para probar'
    )
    group.add_argument(
        '--video', '-v',
        help='Ruta al video (se extraerá el audio)'
    )
    group.add_argument(
        '--crear-audio',
        action='store_true',
        help='Crear audio de prueba con TTS (solo Windows)'
    )
    
    parser.add_argument(
        '--modelo', '-m',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Tamaño del modelo Whisper (default: base)'
    )
    
    args = parser.parse_args()
    
    # Si no se proporciona nada, mostrar ayuda
    if not (args.audio or args.video or args.crear_audio):
        parser.print_help()
        print("\n💡 Sugerencia: Prueba con --crear-audio para generar un audio de prueba")
        sys.exit(1)
    
    try:
        if args.crear_audio:
            # Crear y probar con audio de prueba
            audio_path = crear_audio_prueba()
            if audio_path:
                success = probar_whisper_con_audio(audio_path, args.modelo)
            else:
                print("❌ No se pudo crear audio de prueba")
                sys.exit(1)
                
        elif args.audio:
            # Probar con audio proporcionado
            success = probar_whisper_con_audio(args.audio, args.modelo)
            
        elif args.video:
            # Probar con video
            success = probar_whisper_con_video(args.video, args.modelo)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
