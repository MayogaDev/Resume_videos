"""
Script de Verificación de Instalación
Verifica que todas las dependencias estén instaladas correctamente
"""
import sys
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requiere Python 3.8+")
        return False

def check_package(package_name, import_name=None):
    """Verifica si un paquete está instalado"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"✅ {package_name} - Instalado")
        return True
    except ImportError:
        print(f"❌ {package_name} - No instalado")
        return False

def check_ffmpeg():
    """Verifica si FFmpeg está instalado"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg - {version_line}")
            return True
        else:
            print("❌ FFmpeg - No instalado correctamente")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ FFmpeg - No encontrado en PATH")
        return False

def check_gpu():
    """Verifica si GPU está disponible"""
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU - {device_count} dispositivo(s) disponible(s)")
            print(f"   └─ {device_name}")
            return True
        else:
            print("⚠️  GPU - No disponible (usando CPU)")
            return False
    except ImportError:
        print("❌ PyTorch no instalado, no se puede verificar GPU")
        return False

def check_directory_structure():
    """Verifica la estructura de directorios"""
    required_dirs = [
        "backend/api",
        "backend/core",
        "backend/database",
        "backend/services",
        "frontend/web",
        "frontend/cli",
        "database",
        "docs",
        "config"
    ]

    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/ - Existe")
        else:
            print(f"❌ {dir_path}/ - No existe")
            all_exist = False

    return all_exist

def main():
    """Función principal de verificación"""
    print("=" * 70)
    print("VERIFICACIÓN DE INSTALACIÓN - Sistema de Resumen de Videos")
    print("=" * 70)

    results = {}

    # 1. Python
    print("\n[1/6] Verificando Python...")
    results['python'] = check_python_version()

    # 2. Paquetes Core
    print("\n[2/6] Verificando paquetes core...")
    core_packages = [
        ('torch', 'torch'),
        ('transformers', 'transformers'),
        ('whisper', 'whisper'),
        ('moviepy', 'moviepy'),
    ]
    results['core'] = all(check_package(name, imp) for name, imp in core_packages)

    # 3. Backend packages
    print("\n[3/6] Verificando paquetes backend...")
    backend_packages = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'),
    ]
    results['backend'] = all(check_package(name, imp) for name, imp in backend_packages)

    # 4. Frontend packages
    print("\n[4/6] Verificando paquetes frontend...")
    frontend_packages = [
        ('gradio', 'gradio'),
        ('rich', 'rich'),
        ('click', 'click'),
    ]
    results['frontend'] = all(check_package(name, imp) for name, imp in frontend_packages)

    # 5. FFmpeg
    print("\n[5/6] Verificando FFmpeg...")
    results['ffmpeg'] = check_ffmpeg()

    # 6. GPU (opcional)
    print("\n[6/6] Verificando GPU...")
    results['gpu'] = check_gpu()

    # 7. Estructura de directorios
    print("\n[7/7] Verificando estructura de directorios...")
    results['structure'] = check_directory_structure()

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 70)

    essential_checks = ['python', 'core', 'backend', 'frontend', 'ffmpeg', 'structure']
    essential_passed = all(results[check] for check in essential_checks if check in results)

    if essential_passed:
        print("\n✅ Todas las verificaciones esenciales PASARON")
        print("\nPuedes comenzar a usar el sistema:")
        print("  - API REST: python backend/api/app.py")
        print("  - Web UI: python frontend/web/app.py")
        print("  - CLI: python frontend/cli/cli.py --help")

        if not results.get('gpu', False):
            print("\n⚠️  Nota: GPU no disponible. El procesamiento será más lento.")
            print("   Considera instalar PyTorch con CUDA para mejor rendimiento.")

        return 0
    else:
        print("\n❌ Algunas verificaciones FALLARON")
        print("\nPor favor instala las dependencias faltantes:")
        print("  pip install -r requirements.txt")

        if not results.get('ffmpeg', False):
            print("\nFFmpeg no encontrado. Instálalo desde:")
            print("  - Windows: https://ffmpeg.org/download.html")
            print("  - Linux: sudo apt install ffmpeg")
            print("  - Mac: brew install ffmpeg")

        return 1

if __name__ == "__main__":
    sys.exit(main())
