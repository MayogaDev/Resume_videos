"""
Script de prueba para verificar la instalación
Ejecuta este script para verificar que todas las dependencias están instaladas correctamente
"""
import sys


def check_package(package_name, import_name=None):
    """Verifica si un paquete está instalado"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} instalado correctamente")
        return True
    except ImportError:
        print(f"❌ {package_name} NO está instalado")
        return False


def main():
    """Verifica todas las dependencias"""
    print("="*60)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("="*60)
    print()
    
    packages = [
        ("PyTorch", "torch"),
        ("Transformers", "transformers"),
        ("Datasets", "datasets"),
        ("Whisper", "whisper"),
        ("MoviePy", "moviepy"),
        ("Evaluate", "evaluate"),
        ("ROUGE Score", "rouge_score"),
        ("NLTK", "nltk"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("tqdm", "tqdm"),
    ]
    
    results = []
    for package_name, import_name in packages:
        result = check_package(package_name, import_name)
        results.append(result)
    
    print()
    print("="*60)
    
    if all(results):
        print("✅ TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS")
        print()
        
        # Información adicional
        import torch
        import transformers
        import whisper as whisper_pkg
        
        print("Información del sistema:")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  PyTorch: {torch.__version__}")
        print(f"  Transformers: {transformers.__version__}")
        print(f"  CUDA disponible: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA version: {torch.version.cuda}")
        
        print()
        print("🎉 ¡Tu entorno está listo para usar!")
        print()
        print("Próximos pasos:")
        print("  1. Coloca tus videos en la carpeta 'videos/'")
        print("  2. Ejecuta: cd src && python pipeline.py")
        print("  3. O abre el notebook: jupyter notebook notebooks/tutorial_resumen_videos.ipynb")
        
    else:
        print("❌ FALTAN ALGUNAS DEPENDENCIAS")
        print()
        print("Para instalar todas las dependencias, ejecuta:")
        print("  pip install -r requirements.txt")
    
    print("="*60)


if __name__ == "__main__":
    main()
