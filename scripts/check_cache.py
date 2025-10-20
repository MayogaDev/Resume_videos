"""
Verifica dónde está cacheado el modelo mT5
"""
import sys
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from transformers import AutoTokenizer
import os

print("=" * 70)
print("📦 INFORMACIÓN DE CACHÉ DEL MODELO mT5")
print("=" * 70)

# Obtener ruta de cache
cache_dir = os.environ.get('HF_HOME') or os.path.join(os.path.expanduser('~'), '.cache', 'huggingface')
print(f"\n📂 Directorio de caché de HuggingFace:")
print(f"   {cache_dir}")

# Verificar si existe
if os.path.exists(cache_dir):
    print(f"\n✅ El directorio existe")

    # Buscar modelos mt5
    hub_cache = os.path.join(cache_dir, 'hub')
    if os.path.exists(hub_cache):
        print(f"\n📁 Modelos en caché:")
        for item in os.listdir(hub_cache):
            if 'mt5' in item.lower():
                full_path = os.path.join(hub_cache, item)
                size = sum(f.stat().st_size for f in Path(full_path).rglob('*') if f.is_file())
                print(f"   • {item}")
                print(f"     Tamaño: {size / (1024*1024):.1f} MB")
else:
    print(f"\n⚠️  El directorio no existe")

print("\n" + "=" * 70)
print("💡 INFORMACIÓN DEL MODELO")
print("=" * 70)

print("\n📌 Modelo actual: google/mt5-small")
print("📌 Fuente: HuggingFace Hub (pre-entrenado)")
print("📌 Tipo: Modelo base (NO fine-tuned)")
print("\n⚙️  Proceso:")
print("   1. Primera vez: Descarga desde HuggingFace (~300MB)")
print("   2. Se guarda en caché local automáticamente")
print("   3. Siguientes usos: Carga desde caché (más rápido)")

print("\n" + "=" * 70)
print("💭 OPCIÓN ALTERNATIVA")
print("=" * 70)

print("\n💡 Para usar un modelo fine-tuned personalizado:")
print("   1. Entrenar modelo en dataset específico de resúmenes de videos")
print("   2. Guardar en: models/mt5-video-summarizer/")
print("   3. Cambiar: model_path='models/mt5-video-summarizer'")
print("\n📊 Ventajas de fine-tuning:")
print("   • Resúmenes más relevantes para videos educativos")
print("   • Mejor comprensión del contexto de charlas/conferencias")
print("   • Reducción de 'hallucinations' o texto irrelevante")

print("\n" + "=" * 70)
