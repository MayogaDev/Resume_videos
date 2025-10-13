"""
Pipeline Completo End-to-End
Video → Transcripción (Whisper) → Resumen (mT5)

Autor: Sistema de Resumen de Videos Educativos
Fecha: Octubre 2025
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import json

# Importar módulos del proyecto
from transcribe_video import VideoTranscriber
from inference import VideoSummarizer


def procesar_video_completo(
    video_path: str,
    modelo_mt5_path: str,
    output_dir: str = None,
    whisper_model: str = "base",
    guardar_json: bool = True,
    verbose: bool = True
):
    """
    Procesa un video de principio a fin: transcripción + resumen
    
    Args:
        video_path: Ruta al video (mp4, avi, mkv, etc.)
        modelo_mt5_path: Ruta al modelo mT5 entrenado
        output_dir: Directorio de salida (opcional, por defecto junto al video)
        whisper_model: Tamaño del modelo Whisper (tiny, base, small, medium, large)
        guardar_json: Si guardar resultado en JSON
        verbose: Si mostrar mensajes detallados
    
    Returns:
        dict con transcripción, resumen y estadísticas
    """
    
    # Verificar que el video existe
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ Video no encontrado: {video_path}")
    
    # Verificar que el modelo existe
    if not os.path.exists(modelo_mt5_path):
        raise FileNotFoundError(f"❌ Modelo mT5 no encontrado: {modelo_mt5_path}")
    
    if verbose:
        print("=" * 70)
        print("🎬 PIPELINE COMPLETO DE RESUMEN DE VIDEOS")
        print("=" * 70)
        print(f"📹 Video: {Path(video_path).name}")
        print(f"🧠 Modelo mT5: {Path(modelo_mt5_path).name}")
        print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    inicio = datetime.now()
    
    # ========================================================================
    # PASO 1: TRANSCRIPCIÓN CON WHISPER
    # ========================================================================
    if verbose:
        print("\n[1/2] 🎤 TRANSCRIBIENDO VIDEO CON WHISPER")
        print("-" * 70)
        print(f"   Modelo: {whisper_model}")
        print(f"   Idioma: español")
    
    try:
        transcriber = VideoTranscriber(model_size=whisper_model, language="es")
        transcript_result = transcriber.transcribe_video(
            video_path, 
            save_transcript=True
        )
        
        texto_completo = transcript_result['text']
        segmentos = transcript_result.get('segments', [])
        
        if verbose:
            print(f"\n✅ Transcripción completada:")
            print(f"   - Caracteres: {len(texto_completo):,}")
            print(f"   - Palabras: {len(texto_completo.split()):,}")
            print(f"   - Segmentos: {len(segmentos)}")
            
            # Mostrar preview
            preview = texto_completo[:200] + "..." if len(texto_completo) > 200 else texto_completo
            print(f"\n   Preview: {preview}")
        
    except Exception as e:
        print(f"\n❌ Error en transcripción: {str(e)}")
        raise
    
    # ========================================================================
    # PASO 2: RESUMEN CON mT5
    # ========================================================================
    if verbose:
        print("\n[2/2] 📝 GENERANDO RESUMEN CON mT5")
        print("-" * 70)
        print(f"   Modelo: {Path(modelo_mt5_path).name}")
    
    try:
        summarizer = VideoSummarizer(model_path=modelo_mt5_path)
        resumen = summarizer.summarize(
            texto_completo,
            max_length=128,
            num_beams=4
        )
        
        if verbose:
            print(f"\n✅ Resumen generado:")
            print(f"   - Caracteres: {len(resumen):,}")
            print(f"   - Palabras: {len(resumen.split()):,}")
            print(f"\n   Resumen: {resumen}")
        
    except Exception as e:
        print(f"\n❌ Error en resumen: {str(e)}")
        raise
    
    # ========================================================================
    # PASO 3: CALCULAR ESTADÍSTICAS
    # ========================================================================
    fin = datetime.now()
    tiempo_total = (fin - inicio).total_seconds()
    
    resultado = {
        'video': {
            'ruta': str(video_path),
            'nombre': Path(video_path).name,
            'existe': os.path.exists(video_path)
        },
        'transcripcion': {
            'texto': texto_completo,
            'num_caracteres': len(texto_completo),
            'num_palabras': len(texto_completo.split()),
            'num_segmentos': len(segmentos),
            'idioma': 'es',
            'modelo_whisper': whisper_model
        },
        'resumen': {
            'texto': resumen,
            'num_caracteres': len(resumen),
            'num_palabras': len(resumen.split()),
            'modelo': Path(modelo_mt5_path).name
        },
        'estadisticas': {
            'ratio_compresion': len(resumen) / len(texto_completo) if len(texto_completo) > 0 else 0,
            'palabras_originales': len(texto_completo.split()),
            'palabras_resumen': len(resumen.split()),
            'reduccion_palabras': 1 - (len(resumen.split()) / len(texto_completo.split())) if len(texto_completo.split()) > 0 else 0
        },
        'metadata': {
            'fecha_proceso': datetime.now().isoformat(),
            'tiempo_total_segundos': tiempo_total,
            'tiempo_total_minutos': tiempo_total / 60
        }
    }
    
    # ========================================================================
    # PASO 4: GUARDAR RESULTADOS
    # ========================================================================
    if output_dir is None:
        output_dir = Path(video_path).parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    nombre_base = Path(video_path).stem
    
    # Guardar archivo de texto
    output_txt = output_dir / f"{nombre_base}_resultado.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("SISTEMA DE RESUMEN AUTOMÁTICO DE VIDEOS EDUCATIVOS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Video: {resultado['video']['nombre']}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tiempo de procesamiento: {resultado['metadata']['tiempo_total_minutos']:.2f} minutos\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write("TRANSCRIPCIÓN COMPLETA\n")
        f.write("=" * 70 + "\n\n")
        f.write(resultado['transcripcion']['texto'])
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("RESUMEN GENERADO\n")
        f.write("=" * 70 + "\n\n")
        f.write(resultado['resumen']['texto'])
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("ESTADÍSTICAS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Palabras originales: {resultado['estadisticas']['palabras_originales']:,}\n")
        f.write(f"Palabras resumen: {resultado['estadisticas']['palabras_resumen']:,}\n")
        f.write(f"Compresión: {resultado['estadisticas']['ratio_compresion']:.1%}\n")
        f.write(f"Reducción: {resultado['estadisticas']['reduccion_palabras']:.1%}\n")
    
    # Guardar JSON
    if guardar_json:
        output_json = output_dir / f"{nombre_base}_resultado.json"
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        if verbose:
            print(f"\n💾 Guardado en JSON: {output_json}")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    if verbose:
        print("\n" + "=" * 70)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        print(f"⏱️  Tiempo total: {resultado['metadata']['tiempo_total_minutos']:.2f} minutos")
        print(f"📄 Palabras originales: {resultado['estadisticas']['palabras_originales']:,}")
        print(f"📝 Palabras resumen: {resultado['estadisticas']['palabras_resumen']:,}")
        print(f"📊 Compresión: {resultado['estadisticas']['ratio_compresion']:.1%}")
        print(f"💾 Archivo TXT: {output_txt}")
        if guardar_json:
            print(f"💾 Archivo JSON: {output_json}")
        print("=" * 70)
    
    return resultado


def procesar_batch(
    directorio: str,
    modelo_mt5_path: str,
    output_dir: str = None,
    whisper_model: str = "base",
    extensiones: list = None
):
    """
    Procesa múltiples videos en un directorio
    
    Args:
        directorio: Directorio con videos
        modelo_mt5_path: Ruta al modelo mT5
        output_dir: Directorio de salida
        whisper_model: Modelo de Whisper
        extensiones: Lista de extensiones de video a procesar
    
    Returns:
        list de resultados
    """
    if extensiones is None:
        extensiones = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
    
    directorio = Path(directorio)
    videos = []
    
    for ext in extensiones:
        videos.extend(directorio.glob(f'*{ext}'))
    
    if not videos:
        print(f"❌ No se encontraron videos en: {directorio}")
        return []
    
    print(f"\n📹 Encontrados {len(videos)} videos para procesar\n")
    
    resultados = []
    exitosos = 0
    fallidos = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*70}")
        print(f"Procesando {i}/{len(videos)}: {video.name}")
        print(f"{'='*70}\n")
        
        try:
            resultado = procesar_video_completo(
                video_path=str(video),
                modelo_mt5_path=modelo_mt5_path,
                output_dir=output_dir,
                whisper_model=whisper_model,
                verbose=True
            )
            resultados.append(resultado)
            exitosos += 1
            
        except Exception as e:
            print(f"\n❌ Error procesando {video.name}: {str(e)}")
            fallidos += 1
            continue
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PROCESAMIENTO BATCH")
    print("=" * 70)
    print(f"Total de videos: {len(videos)}")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Fallidos: {fallidos}")
    print("=" * 70)
    
    return resultados


def main():
    """Función principal con CLI"""
    parser = argparse.ArgumentParser(
        description="Pipeline completo de resumen de videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Procesar un solo video
  python pipeline_completo.py --video "clase.mp4" --modelo "models/mt5-video-summarizer-final"
  
  # Procesar con modelo Whisper más grande
  python pipeline_completo.py --video "clase.mp4" --modelo "models/mt5-video-summarizer-final" --whisper small
  
  # Procesar múltiples videos en batch
  python pipeline_completo.py --batch "videos/" --modelo "models/mt5-video-summarizer-final"
  
  # Especificar directorio de salida
  python pipeline_completo.py --video "clase.mp4" --modelo "models/mt5-video-summarizer-final" --output "resultados/"
        """
    )
    
    # Argumentos principales
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--video', '-v',
        help='Ruta al video a procesar'
    )
    group.add_argument(
        '--batch', '-b',
        help='Directorio con múltiples videos para procesar en batch'
    )
    
    parser.add_argument(
        '--modelo', '-m',
        required=True,
        help='Ruta al modelo mT5 entrenado'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Directorio de salida para resultados (opcional)'
    )
    
    parser.add_argument(
        '--whisper',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Tamaño del modelo Whisper (default: base)'
    )
    
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='No guardar resultado en formato JSON'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Modo silencioso, mínima salida'
    )
    
    args = parser.parse_args()
    
    try:
        if args.video:
            # Procesar un solo video
            resultado = procesar_video_completo(
                video_path=args.video,
                modelo_mt5_path=args.modelo,
                output_dir=args.output,
                whisper_model=args.whisper,
                guardar_json=not args.no_json,
                verbose=not args.quiet
            )
            
        elif args.batch:
            # Procesar múltiples videos
            resultados = procesar_batch(
                directorio=args.batch,
                modelo_mt5_path=args.modelo,
                output_dir=args.output,
                whisper_model=args.whisper
            )
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        if not args.quiet:
            print("\n📋 Traceback:")
            print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
