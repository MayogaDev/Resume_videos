"""
Lanzador de la Interfaz Web
Script helper para iniciar web_app.py correctamente
"""

import sys
import os

# Agregar src al path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Cambiar al directorio src
os.chdir(src_path)

# Importar y ejecutar web_app
from web_app import main

if __name__ == "__main__":
    main()
