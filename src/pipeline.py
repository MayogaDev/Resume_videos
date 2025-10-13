"""
Pipeline Completo
Orquesta todo el proceso: transcripción, entrenamiento e inferencia
"""
import argparse
from pathlib import Path
import sys

# Importar módulos del proyecto
from transcribe_video import VideoTranscriber
from prepare_dataset import DatasetPreparator
from train_model import SummaryTrainer
from inference import VideoSummarizer


def pipeline_full(video_dir: str, 
                 model_name: str = "google/mt5-small",
                 num_epochs: int = 3):
    """
    Pipeline completo: desde videos hasta resúmenes
    
    Args:
        video_dir: Directorio con videos
        model_name: Modelo base a usar
        num_epochs: Número de épocas de entrenamiento
    """
    print("="*60)
    print("PIPELINE COMPLETO DE RESUMEN DE VIDEOS")
    print("="*60)
    
    # Paso 1: Transcribir videos
    print("\n[1/5] Transcribiendo videos...")
    transcriber = VideoTranscriber(model_size="base", language="es")
    transcript_dir = Path(video_dir) / "transcripts"
    transcriber.batch_transcribe(video_dir, str(transcript_dir))
    
    # Paso 2: Preparar dataset (usar dataset público por ahora)
    print("\n[2/5] Preparando dataset de entrenamiento...")
    preparator = DatasetPreparator(model_name=model_name)
    dataset = preparator.load_public_dataset(
        dataset_name="xsum",
        language="en",
        num_samples=5000
    )
    tokenized_dataset = preparator.prepare_dataset(dataset)
    dataset_path = "data/processed/training_dataset"
    preparator.save_dataset(tokenized_dataset, dataset_path)
    
    # Paso 3: Entrenar modelo
    print("\n[3/5] Entrenando modelo...")
    trainer = SummaryTrainer(
        model_name=model_name,
        output_dir="models/video-summarizer"
    )
    trainer.train(
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        num_train_epochs=num_epochs,
        batch_size=4
    )
    
    # Paso 4: Generar resúmenes
    print("\n[4/5] Generando resúmenes...")
    summarizer = VideoSummarizer(model_path="models/video-summarizer")
    results = summarizer.batch_summarize_transcripts(str(transcript_dir))
    
    # Paso 5: Reporte final
    print("\n[5/5] Proceso completado!")
    print(f"  - Videos procesados: {len(results)}")
    print(f"  - Modelo entrenado guardado en: models/video-summarizer")
    print(f"  - Resúmenes guardados en: {transcript_dir}")
    
    return results


def pipeline_inference_only(video_path: str, 
                            model_path: str = "models/video-summarizer"):
    """
    Pipeline solo para inferencia (modelo ya entrenado)
    
    Args:
        video_path: Ruta del video a procesar
        model_path: Ruta del modelo entrenado
    """
    print("="*60)
    print("PIPELINE DE INFERENCIA")
    print("="*60)
    
    # Paso 1: Transcribir
    print("\n[1/2] Transcribiendo video...")
    transcriber = VideoTranscriber(model_size="base", language="es")
    transcript = transcriber.transcribe_video(video_path)
    
    # Paso 2: Resumir
    print("\n[2/2] Generando resumen...")
    summarizer = VideoSummarizer(model_path=model_path)
    summary = summarizer.summarize(transcript['text'])
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("RESULTADOS")
    print("="*60)
    print(f"\nTexto transcrito ({len(transcript['text'])} caracteres):")
    print(transcript['text'][:500] + "...")
    print(f"\nResumen generado ({len(summary)} caracteres):")
    print(summary)
    
    return summary


def main():
    """Función principal con CLI"""
    parser = argparse.ArgumentParser(description="Pipeline de resumen de videos")
    
    parser.add_argument(
        "--mode",
        type=str,
        choices=["full", "inference", "train", "transcribe"],
        default="inference",
        help="Modo de ejecución"
    )
    
    parser.add_argument(
        "--video",
        type=str,
        help="Ruta del video a procesar (para modo inference)"
    )
    
    parser.add_argument(
        "--video-dir",
        type=str,
        default="videos",
        help="Directorio con videos (para modo full o transcribe)"
    )
    
    parser.add_argument(
        "--model-name",
        type=str,
        default="google/mt5-small",
        help="Modelo base a usar (mt5-small, t5-small, etc.)"
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="models/video-summarizer",
        help="Ruta del modelo entrenado (para inference)"
    )
    
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Número de épocas de entrenamiento"
    )
    
    args = parser.parse_args()
    
    # Ejecutar según el modo
    if args.mode == "full":
        pipeline_full(
            video_dir=args.video_dir,
            model_name=args.model_name,
            num_epochs=args.epochs
        )
    
    elif args.mode == "inference":
        if not args.video:
            print("Error: Debes especificar --video para el modo inference")
            sys.exit(1)
        
        pipeline_inference_only(
            video_path=args.video,
            model_path=args.model_path
        )
    
    elif args.mode == "transcribe":
        print("Transcribiendo videos...")
        transcriber = VideoTranscriber(model_size="base", language="es")
        transcriber.batch_transcribe(args.video_dir)
        print("Transcripción completada!")
    
    elif args.mode == "train":
        print("Entrenando modelo...")
        from datasets import load_from_disk
        dataset = load_from_disk("data/processed/training_dataset")
        
        trainer = SummaryTrainer(
            model_name=args.model_name,
            output_dir=args.model_path
        )
        trainer.train(
            train_dataset=dataset["train"],
            eval_dataset=dataset["validation"],
            num_train_epochs=args.epochs,
            batch_size=4
        )
        print("Entrenamiento completado!")


if __name__ == "__main__":
    # Si no hay argumentos, mostrar ejemplo de uso
    if len(sys.argv) == 1:
        print("\n" + "="*60)
        print("SISTEMA DE RESUMEN DE VIDEOS EDUCATIVOS")
        print("="*60)
        print("\nEjemplos de uso:")
        print("\n1. Resumir un video (con modelo ya entrenado):")
        print("   python pipeline.py --mode inference --video videos/mi_video.mp4")
        print("\n2. Pipeline completo (transcribir + entrenar + resumir):")
        print("   python pipeline.py --mode full --video-dir videos")
        print("\n3. Solo transcribir videos:")
        print("   python pipeline.py --mode transcribe --video-dir videos")
        print("\n4. Solo entrenar modelo:")
        print("   python pipeline.py --mode train --epochs 5")
        print("\n" + "="*60)
        print("\nPara más opciones, usa: python pipeline.py --help")
        print()
    else:
        main()
