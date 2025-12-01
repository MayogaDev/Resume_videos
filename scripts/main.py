"""
Punto de entrada principal del sistema
Permite iniciar diferentes componentes del sistema
"""
import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cambiar al directorio raíz del proyecto
project_root = Path(__file__).parent.parent
os.chdir(project_root)
sys.path.insert(0, str(project_root))

# Configurar FFmpeg antes de iniciar cualquier componente
print("Configurando FFmpeg...")
from scripts.setup_ffmpeg import setup_ffmpeg_path
if not setup_ffmpeg_path():
    print("\n⚠️  Advertencia: FFmpeg no está disponible.")
    print("El procesamiento de videos podría fallar.")
    input("Presiona Enter para continuar de todas formas...")

def run_api():
    """Inicia el servidor API REST"""
    from backend.api.app import run_server
    print("🚀 Iniciando API REST...")
    run_server(debug=False)

def run_web():
    """Inicia la interfaz web Gradio"""
    print("🌐 Iniciando interfaz web...")
    # Obtener modelo y puerto desde variables de entorno
    model_path = os.getenv('MODEL_PATH', 'google/mt5-small')
    web_port = os.getenv('WEB_PORT', '7860')
    # Importar dinámicamente
    import subprocess
    subprocess.run([sys.executable, "frontend/web/app.py", "--modelo", model_path, "--port", web_port])

def run_cli():
    """Inicia la CLI"""
    print("💻 CLI - Para usar la CLI, ejecuta:")
    print("  python frontend/cli/cli.py --help")

def verify_installation():
    """Verifica la instalación"""
    import subprocess
    subprocess.run([sys.executable, "scripts/verify_installation.py"])

def main():
    parser = argparse.ArgumentParser(
        description="Sistema de Resumen Automático de Videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py api              # Inicia API REST
  python main.py web              # Inicia interfaz web
  python main.py verify           # Verifica instalación

  # Para CLI, usa:
  python frontend/cli/cli.py --help
        """
    )

    parser.add_argument(
        'command',
        choices=['api', 'web', 'cli', 'verify'],
        help='Componente a ejecutar'
    )

    args = parser.parse_args()

    # Banner
    print("=" * 70)
    print(" 🎬 Sistema de Resumen Automático de Videos")
    print(" Whisper + mT5 | Backend API | Frontend Web/CLI")
    print("=" * 70)
    print()

    # Ejecutar comando
    if args.command == 'api':
        run_api()
    elif args.command == 'web':
        run_web()
    elif args.command == 'cli':
        run_cli()
    elif args.command == 'verify':
        verify_installation()

if __name__ == "__main__":
    main()
