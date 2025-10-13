"""
Script de Verificación de Instalación de Whisper
Verifica que OpenAI Whisper esté instalado y funcionando correctamente

Autor: Sistema de Resumen de Videos Educativos
Fecha: Octubre 2025
"""

import sys
import os


def verificar_whisper():
    """Verifica instalación de Whisper"""
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE WHISPER")
    print("=" * 70)
    
    # 1. Verificar importación
    print("\n[1/5] Verificando importación de whisper...")
    try:
        import whisper
        print("✅ Módulo whisper importado correctamente")
        print(f"   Versión: {whisper.__version__ if hasattr(whisper, '__version__') else 'N/A'}")
    except ImportError as e:
        print("❌ Error: whisper no está instalado")
        print(f"\n💡 Solución:")
        print("   pip install openai-whisper")
        return False
    
    # 2. Verificar torch
    print("\n[2/5] Verificando PyTorch...")
    try:
        import torch
        print("✅ PyTorch instalado")
        print(f"   Versión: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
        else:
            print("   ⚠️  GPU no disponible, Whisper usará CPU (más lento)")
    except ImportError:
        print("❌ PyTorch no está instalado")
        return False
    
    # 3. Verificar ffmpeg
    print("\n[3/5] Verificando ffmpeg...")
    try:
        import subprocess
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ ffmpeg instalado: {version_line}")
        else:
            raise Exception("ffmpeg no encontrado")
    except (FileNotFoundError, Exception) as e:
        print("❌ ffmpeg no está instalado o no está en el PATH")
        print(f"\n💡 Solución Windows:")
        print("   1. Descargar: https://ffmpeg.org/download.html")
        print("   2. Extraer y agregar al PATH del sistema")
        print("   O usando chocolatey: choco install ffmpeg")
        print(f"\n💡 Solución Linux:")
        print("   sudo apt install ffmpeg")
        return False
    
    # 4. Listar modelos disponibles
    print("\n[4/5] Modelos de Whisper disponibles:")
    modelos = ['tiny', 'base', 'small', 'medium', 'large']
    for modelo in modelos:
        print(f"   - {modelo}")
    
    # 5. Probar carga de modelo
    print("\n[5/5] Probando carga de modelo 'tiny' (más rápido)...")
    try:
        print("   ⏳ Descargando/cargando modelo tiny...")
        model = whisper.load_model("tiny")
        print("   ✅ Modelo cargado correctamente")
        print(f"   📊 Tamaño del modelo: ~39 MB")
        
        # Limpiar memoria
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
    except Exception as e:
        print(f"   ❌ Error al cargar modelo: {str(e)}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ WHISPER ESTÁ INSTALADO Y FUNCIONANDO CORRECTAMENTE")
    print("=" * 70)
    print("\n💡 Próximos pasos:")
    print("   1. Ejecuta: python src/test_whisper_audio.py")
    print("   2. Prueba con tu primer video")
    print("=" * 70)
    
    return True


def verificar_moviepy():
    """Verifica instalación de moviepy"""
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DE MOVIEPY (para extraer audio)")
    print("=" * 70)
    
    try:
        import moviepy
        from moviepy.editor import VideoFileClip
        print("✅ moviepy instalado correctamente")
        print(f"   Versión: {moviepy.__version__}")
        return True
    except ImportError:
        print("❌ moviepy no está instalado")
        print(f"\n💡 Solución:")
        print("   pip install moviepy")
        return False


def verificar_dependencias_completas():
    """Verifica todas las dependencias del proyecto"""
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DE DEPENDENCIAS COMPLETAS")
    print("=" * 70)
    
    dependencias = {
        'transformers': '✅ Para modelo mT5',
        'datasets': '✅ Para cargar datasets',
        'torch': '✅ PyTorch (deep learning)',
        'whisper': '✅ OpenAI Whisper (transcripción)',
        'moviepy': '✅ Para extraer audio de videos',
        'sentencepiece': '✅ Tokenizador de mT5',
        'evaluate': '✅ Métricas ROUGE',
        'tqdm': '✅ Barras de progreso'
    }
    
    instaladas = []
    faltantes = []
    
    for paquete, descripcion in dependencias.items():
        try:
            __import__(paquete)
            print(f"{descripcion}")
            instaladas.append(paquete)
        except ImportError:
            print(f"❌ {paquete} no instalado - {descripcion}")
            faltantes.append(paquete)
    
    print("\n" + "=" * 70)
    print(f"✅ Instaladas: {len(instaladas)}/{len(dependencias)}")
    
    if faltantes:
        print(f"❌ Faltantes: {len(faltantes)}")
        print(f"\n💡 Para instalar todas:")
        print(f"   pip install {' '.join(faltantes)}")
    else:
        print("🎉 ¡Todas las dependencias están instaladas!")
    
    print("=" * 70)
    
    return len(faltantes) == 0


def main():
    """Función principal"""
    print("\n")
    print("🎓 Sistema de Resumen Automático de Videos Educativos")
    print("   Verificación de Instalación\n")
    
    # Verificar Whisper
    whisper_ok = verificar_whisper()
    
    # Verificar moviepy
    moviepy_ok = verificar_moviepy()
    
    # Verificar todas las dependencias
    deps_ok = verificar_dependencias_completas()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70)
    
    if whisper_ok and moviepy_ok and deps_ok:
        print("✅ Sistema listo para usar")
        print("\n🚀 Puedes comenzar a procesar videos:")
        print("   python src/pipeline_completo.py --video tu_video.mp4 --modelo models/mt5-video-summarizer-final")
        sys.exit(0)
    else:
        print("❌ Faltan componentes por instalar")
        print("\n💡 Sigue las instrucciones arriba para completar la instalación")
        sys.exit(1)


if __name__ == "__main__":
    main()
