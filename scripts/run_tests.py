"""
Script para ejecutar tests con diferentes opciones
"""
import sys
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cambiar al directorio raíz
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_tests(test_type="all", verbose=True, coverage=False):
    """
    Ejecuta los tests con pytest

    Args:
        test_type: Tipo de tests ('unit', 'integration', 'all')
        verbose: Modo verbose
        coverage: Calcular cobertura de código
    """
    print("=" * 70)
    print("🧪 EJECUTANDO TESTS")
    print("=" * 70)

    # Construir comando
    cmd = ["pytest"]

    # Agregar opciones
    if verbose:
        cmd.append("-v")

    # Seleccionar tipo de tests
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
        print("\n📦 Ejecutando: Tests Unitarios")
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
        print("\n🔗 Ejecutando: Tests de Integración")
    elif test_type == "api":
        cmd.extend(["-k", "test_api"])
        print("\n🌐 Ejecutando: Tests de API")
    elif test_type == "database":
        cmd.extend(["-k", "test_database"])
        print("\n💾 Ejecutando: Tests de Base de Datos")
    else:
        print("\n🎯 Ejecutando: Todos los Tests")

    # Cobertura
    if coverage:
        cmd.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
        print("📊 Con reporte de cobertura")

    print("=" * 70)
    print()

    # Ejecutar
    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode
    except Exception as e:
        print(f"\n❌ Error al ejecutar tests: {e}")
        return 1


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ejecuta los tests del proyecto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/run_tests.py                    # Todos los tests
  python scripts/run_tests.py --type unit        # Solo tests unitarios
  python scripts/run_tests.py --type integration # Solo tests de integración
  python scripts/run_tests.py --coverage         # Con cobertura de código
  python scripts/run_tests.py --type unit --coverage # Unitarios con cobertura
        """
    )

    parser.add_argument(
        '--type', '-t',
        choices=['all', 'unit', 'integration', 'api', 'database'],
        default='all',
        help='Tipo de tests a ejecutar'
    )

    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Calcular cobertura de código'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Modo silencioso (menos verbose)'
    )

    args = parser.parse_args()

    # Ejecutar tests
    exit_code = run_tests(
        test_type=args.type,
        verbose=not args.quiet,
        coverage=args.coverage
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
