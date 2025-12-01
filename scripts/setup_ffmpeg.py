"""
Script para configurar FFmpeg en el PATH antes de ejecutar el proyecto
Soluciona el problema de FFmpeg no disponible en la sesión actual
"""
import os
import sys
import subprocess
from pathlib import Path

def find_ffmpeg():
    """Busca FFmpeg en ubicaciones comunes de Windows"""
    possible_paths = [
        # Winget locations
        Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
        Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-*" / "bin",
        # Common installation paths
        Path("C:/ffmpeg/bin"),
        Path("C:/Program Files/ffmpeg/bin"),
        Path("C:/Program Files (x86)/ffmpeg/bin"),
        # Webots (found earlier)
        Path("C:/Program Files/Webots/msys64/mingw64/bin"),
    ]

    # Check direct exe paths
    for path in possible_paths:
        if path.suffix == '.exe' and path.exists():
            print(f"[OK] FFmpeg encontrado: {path}")
            return str(path.parent)
        elif path.exists() and path.is_dir():
            ffmpeg_exe = path / "ffmpeg.exe"
            if ffmpeg_exe.exists():
                print(f"[OK] FFmpeg encontrado: {ffmpeg_exe}")
                return str(path)

    # Try using 'where' command
    try:
        result = subprocess.run(
            ["where", "ffmpeg"],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            ffmpeg_path = Path(result.stdout.strip().split('\n')[0])
            print(f"[OK] FFmpeg encontrado en PATH: {ffmpeg_path}")
            return str(ffmpeg_path.parent)
    except:
        pass

    return None

def setup_ffmpeg_path():
    """Agrega FFmpeg al PATH del proceso actual"""
    ffmpeg_dir = find_ffmpeg()

    if ffmpeg_dir:
        # Agregar al PATH del proceso actual
        current_path = os.environ.get('PATH', '')
        if ffmpeg_dir not in current_path:
            os.environ['PATH'] = f"{ffmpeg_dir}{os.pathsep}{current_path}"
            print(f"[OK] FFmpeg agregado al PATH: {ffmpeg_dir}")

            # Configurar variables de entorno para ImageIO/MoviePy
            os.environ['IMAGEIO_FFMPEG_EXE'] = str(Path(ffmpeg_dir) / "ffmpeg.exe")
            print(f"[OK] IMAGEIO_FFMPEG_EXE configurado")

            return True
        else:
            print("[OK] FFmpeg ya esta en el PATH")
            return True
    else:
        print("[ERROR] FFmpeg no encontrado. Por favor instalalo o reinicia el terminal.")
        print("\nPara instalar FFmpeg:")
        print("  winget install --id Gyan.FFmpeg")
        print("\nO descarga desde: https://ffmpeg.org/download.html")
        return False

if __name__ == "__main__":
    success = setup_ffmpeg_path()
    sys.exit(0 if success else 1)
