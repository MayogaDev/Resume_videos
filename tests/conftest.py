"""
Configuración de pytest y fixtures compartidas
"""
import sys
from pathlib import Path
import pytest
import tempfile
import shutil

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Ruta raíz del proyecto"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_video_path(project_root_path):
    """Ruta al video de prueba"""
    video_path = project_root_path / "tests" / "test_data" / "videotest_resumen.mp4"
    if video_path.exists():
        return video_path
    else:
        pytest.skip("Video de prueba no disponible")


@pytest.fixture
def temp_db():
    """Base de datos temporal para tests"""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"

    yield str(db_path)

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_output_dir():
    """Directorio temporal para outputs"""
    temp_dir = tempfile.mkdtemp()

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def sample_text():
    """Texto de ejemplo para tests de resumen"""
    return """
    La inteligencia artificial está transformando la educación moderna.
    Los sistemas de IA pueden personalizar el aprendizaje para cada estudiante,
    adaptándose a su ritmo y estilo individual. Las herramientas de IA ayudan
    a los profesores a automatizar tareas administrativas y crear contenidos
    educativos más efectivos. Sin embargo, es importante mantener el balance
    entre tecnología y el factor humano en la educación.
    """


@pytest.fixture(scope="session")
def sample_transcription():
    """Transcripción de ejemplo para tests"""
    return {
        "text": "Este es un texto de transcripción de prueba con suficiente contenido para ser resumido.",
        "language": "es",
        "stats": {
            "total_words": 15,
            "total_characters": 95,
            "total_segments": 1
        }
    }
