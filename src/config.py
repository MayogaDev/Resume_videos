# Configuración del proyecto
PROJECT_NAME = "video-summarizer"
DATA_DIR = "data"
MODEL_DIR = "models"
VIDEO_DIR = "videos"

# Configuración de Whisper
WHISPER_MODEL_SIZE = "base"  # tiny, base, small, medium, large
DEFAULT_LANGUAGE = "es"

# Configuración del modelo de resumen
DEFAULT_MODEL_NAME = "google/mt5-small"  # Para español
# Alternativas:
# - "google/mt5-base" (más grande, mejor calidad)
# - "t5-small" (solo inglés)
# - "facebook/bart-base" (solo inglés)

# Hiperparámetros de entrenamiento
TRAINING_ARGS = {
    "num_train_epochs": 3,
    "batch_size": 4,
    "learning_rate": 5e-5,
    "warmup_steps": 500,
    "save_steps": 1000,
    "eval_steps": 1000,
    "max_input_length": 512,
    "max_target_length": 128,
}

# Parámetros de generación
GENERATION_ARGS = {
    "max_length": 128,
    "min_length": 30,
    "num_beams": 4,
    "length_penalty": 2.0,
    "early_stopping": True,
}

# Dataset
DATASET_CONFIG = {
    "name": "xsum",  # xsum, cnn_dailymail, mlsum
    "language": "en",  # en, es
    "num_samples": 5000,  # Número de muestras para entrenamiento rápido
}
