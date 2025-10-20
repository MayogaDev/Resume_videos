"""
Punto de entrada principal del sistema
Permite iniciar diferentes componentes del sistema
"""
import argparse
import sys
import os
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cambiar al directorio raíz del proyecto
project_root = Path(__file__).parent.parent
os.chdir(project_root)
sys.path.insert(0, str(project_root))

def run_api():
    """Inicia el servidor API REST"""
    from backend.api.app import run_server
    print("🚀 Iniciando API REST...")
    run_server(debug=False)

def run_web():
    """Inicia la interfaz web Gradio"""
    print("🌐 Iniciando interfaz web...")
    # Obtener modelo desde variable de entorno o usar default
    model_path = os.getenv('MODEL_PATH', 'google/mt5-small')
    # Importar dinámicamente
    import subprocess
    subprocess.run([sys.executable, "frontend/web/app.py", "--modelo", model_path])

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
