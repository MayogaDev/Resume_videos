"""
Script para descargar modelos de IA una sola vez
Los modelos se guardan en la carpeta models/ y se reutilizan
"""
import os
import sys
from pathlib import Path
import whisper
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Directorio de modelos
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Subdirectorios para cada tipo de modelo
WHISPER_CACHE = MODELS_DIR / "whisper"
MT5_CACHE = MODELS_DIR / "mt5"

WHISPER_CACHE.mkdir(exist_ok=True)
MT5_CACHE.mkdir(exist_ok=True)

def download_whisper_model(model_size="base"):
    """Descarga un modelo de Whisper"""
    print(f"\n{'='*70}")
    print(f"DESCARGANDO WHISPER - {model_size.upper()}")
    print(f"{'='*70}")

    # Configurar caché de Whisper
    os.environ["WHISPER_CACHE_DIR"] = str(WHISPER_CACHE)

    try:
        print(f"Ubicacion: {WHISPER_CACHE}")
        print("Descargando... (esto puede tomar varios minutos)")

        model = whisper.load_model(
            model_size,
            download_root=str(WHISPER_CACHE)
        )

        print(f"[OK] Whisper {model_size} descargado exitosamente")

        # Mostrar tamaño
        model_files = list(WHISPER_CACHE.glob("*.pt"))
        if model_files:
            size_mb = sum(f.stat().st_size for f in model_files) / (1024 * 1024)
            print(f"[*] Tamano en disco: {size_mb:.1f} MB")

        return True

    except Exception as e:
        print(f"[X] Error al descargar Whisper {model_size}: {e}")
        return False


def download_mt5_model(model_name="google/mt5-small"):
    """Descarga un modelo mT5"""
    print(f"\n{'='*70}")
    print(f"DESCARGANDO mT5")
    print(f"{'='*70}")

    try:
        print(f"Modelo: {model_name}")
        print(f"Ubicacion: {MT5_CACHE}")
        print("Descargando tokenizer... (puede tomar varios minutos)")

        # Descargar tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=str(MT5_CACHE),
            use_fast=False
        )
        print("[OK] Tokenizer descargado")

        # Descargar modelo
        print("Descargando modelo... (puede tomar 5-10 minutos)")
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            cache_dir=str(MT5_CACHE),
            torch_dtype=torch.float32
        )
        print("[OK] Modelo descargado")

        # Mostrar tamaño
        cache_files = list(MT5_CACHE.rglob("*"))
        size_mb = sum(f.stat().st_size for f in cache_files if f.is_file()) / (1024 * 1024)
        print(f"[*] Tamano en disco: {size_mb:.1f} MB")
        print(f"[OK] mT5 descargado exitosamente")

        return True

    except Exception as e:
        print(f"[X] Error al descargar mT5: {e}")
        return False


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("          DESCARGADOR DE MODELOS DE IA")
    print("       Sistema de Resumen de Videos Educativos")
    print("="*70 + "\n")

    print(f"[*] Directorio de modelos: {MODELS_DIR.absolute()}\n")

    # Verificar espacio en disco
    import shutil
    stat = shutil.disk_usage(MODELS_DIR.parent)
    free_gb = stat.free / (1024**3)
    print(f"[*] Espacio libre en disco: {free_gb:.1f} GB")

    if free_gb < 5:
        print("[!] ADVERTENCIA: Poco espacio en disco (< 5 GB)")
        print("    Se recomienda al menos 5 GB libres\n")

    print("\n" + "="*70)
    print("MODELOS A DESCARGAR:")
    print("="*70)
    print("1. Whisper 'base' (~140 MB) - Transcripción de audio")
    print("2. mT5 'small' (~1.2 GB) - Generación de resúmenes")
    print("="*70)

    response = input("\nDescargar todos los modelos? (s/n): ").lower()

    if response != 's':
        print("[X] Descarga cancelada")
        return

    # Descargar modelos
    results = []

    # Whisper
    results.append(("Whisper base", download_whisper_model("base")))

    # mT5
    results.append(("mT5 small", download_mt5_model("google/mt5-small")))

    # Resumen
    print(f"\n{'='*70}")
    print("RESUMEN DE DESCARGAS")
    print(f"{'='*70}")

    for name, success in results:
        status = "[OK] Exito" if success else "[X] Error"
        print(f"{name:20s} {status}")

    if all(success for _, success in results):
        print(f"\n{'='*70}")
        print("TODOS LOS MODELOS DESCARGADOS EXITOSAMENTE!")
        print(f"{'='*70}")
        print(f"\n[*] Ubicacion: {MODELS_DIR.absolute()}")
        print("\n[*] Los modelos ahora se cargaran desde el disco local")
        print("    No se descargaran de nuevo en las siguientes ejecuciones")

        # Calcular tamaño total
        all_files = list(MODELS_DIR.rglob("*"))
        total_mb = sum(f.stat().st_size for f in all_files if f.is_file()) / (1024 * 1024)
        print(f"\n[*] Espacio total usado: {total_mb:.1f} MB ({total_mb/1024:.2f} GB)")

    else:
        print("\n[!] Algunos modelos no se descargaron correctamente")
        print("    Puedes intentar ejecutar este script de nuevo")

    print("\n" + "="*70)
    print("[OK] Proceso completado")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Descarga interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
