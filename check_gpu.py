"""
Script para verificar disponibilidad de GPU y configuración CUDA
"""
import torch

print("=" * 60)
print("VERIFICACIÓN DE GPU Y CUDA")
print("=" * 60)

print(f"\n✓ PyTorch version: {torch.__version__}")
print(f"✓ CUDA disponible: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"✓ GPU detectada: {torch.cuda.get_device_name(0)}")
    print(f"✓ CUDA version: {torch.version.cuda}")
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"✓ VRAM Total: {vram_gb:.2f} GB")
    print(f"✓ VRAM Disponible: {torch.cuda.memory_allocated(0) / (1024**3):.2f} GB usados")
    print(f"\n✅ GPU lista para entrenamiento!")
else:
    print("\n❌ GPU no detectada. El entrenamiento será en CPU (muy lento)")
    print("Verifica que:")
    print("  1. Tienes una GPU NVIDIA")
    print("  2. Drivers NVIDIA instalados")
    print("  3. PyTorch con CUDA: pip install torch --index-url https://download.pytorch.org/whl/cu118")

print("=" * 60)
