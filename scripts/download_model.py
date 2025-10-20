"""
Script para descargar el modelo mT5 de HuggingFace
"""
import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def download_model():
    """Descarga el modelo google/mt5-small localmente"""

    # Crear directorio para modelos
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models" / "mt5-small"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("📥 Descargando modelo google/mt5-small...")
    print("=" * 70)
    print(f"📂 Destino: {models_dir}")
    print()

    try:
        # Descargar tokenizer
        print("🔄 Descargando tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("google/mt5-small")
        tokenizer.save_pretrained(str(models_dir))
        print("✅ Tokenizer descargado")

        # Descargar modelo
        print("\n🔄 Descargando modelo (esto puede tomar varios minutos)...")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-small")
        model.save_pretrained(str(models_dir))
        print("✅ Modelo descargado")

        print("\n" + "=" * 70)
        print("✅ Modelo descargado exitosamente!")
        print("=" * 70)
        print(f"📂 Ubicación: {models_dir}")
        print(f"📊 Tamaño: {sum(f.stat().st_size for f in models_dir.rglob('*') if f.is_file()) / (1024*1024):.1f} MB")
        print()
        print("💡 Ahora puedes usar el modelo localmente configurando:")
        print(f"   MODEL_PATH={models_dir}")
        print()

        return str(models_dir)

    except Exception as e:
        print(f"\n❌ Error al descargar el modelo: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    download_model()
