"""
Configuración optimizada para RTX 3050 (4GB VRAM)
Entrenamiento robusto con dataset MLSUM en español
"""

# ============================================================================
# CONFIGURACIÓN DE HARDWARE
# ============================================================================
DEVICE_CONFIG = {
    "gpu_name": "RTX 3050",
    "vram_gb": 4,
    "use_gpu": True,
    "fp16": True,  # Precision mixta para ahorrar VRAM
    "gradient_checkpointing": True,  # Ahorra memoria durante backprop
}

# ============================================================================
# CONFIGURACIÓN DE MODELO
# ============================================================================
MODEL_CONFIG = {
    # Modelo pequeño optimizado para español
    "model_name": "google/mt5-small",  # 300M parámetros, multilingüe
    # Alternativa más pequeña: "google/mt5-base" si hay problemas
    
    # Longitudes máximas (reducidas para 4GB VRAM)
    "max_input_length": 512,   # Texto de entrada
    "max_target_length": 128,  # Resumen generado
    
    # Generación
    "num_beams": 4,
    "length_penalty": 2.0,
    "early_stopping": True,
}

# ============================================================================
# CONFIGURACIÓN DE DATASET
# ============================================================================
DATASET_CONFIG = {
    # Dataset en español
    "dataset_name": "mlsum",
    "dataset_config": "es",  # Español
    "cache_dir": "./data/cache",
    
    # Subconjunto para entrenar (ajusta según tiempo disponible)
    #"train_samples": 10000,  # De 266,367 disponibles
    #"val_samples": 1000,     # De 10,358 disponibles
    #"test_samples": 500,     # De 13,920 disponibles

    # Para entrenamiento rápido de prueba:
    "train_samples": 1000,
    "val_samples": 200,
    "test_samples": 100,
}

# ============================================================================
# CONFIGURACIÓN DE ENTRENAMIENTO (OPTIMIZADO PARA 4GB VRAM)
# ============================================================================
TRAINING_CONFIG = {
    # Batch sizes pequeños para 4GB
    "per_device_train_batch_size": 2,  # 2 ejemplos por paso
    "per_device_eval_batch_size": 4,    # Evaluación puede ser más grande
    "gradient_accumulation_steps": 8,   # Simula batch_size=16
    
    # Optimizador
    "learning_rate": 3e-5,
    "weight_decay": 0.01,
    "warmup_steps": 500,
    "max_grad_norm": 1.0,
    
    # Épocas
    "num_train_epochs": 3,
    "max_steps": -1,  # -1 = usar num_train_epochs
    
    # Logging y evaluación
    "logging_steps": 50,
    "eval_steps": 500,
    "save_steps": 500,
    "save_total_limit": 3,  # Solo guardar últimos 3 checkpoints
    
    # Early stopping
    "load_best_model_at_end": True,
    "metric_for_best_model": "rouge1",
    "greater_is_better": True,
    "early_stopping_patience": 3,  # Parar si no mejora en 3 evaluaciones
    
    # Memoria
    "fp16": True,  # Precision mixta
    "gradient_checkpointing": True,
    "dataloader_num_workers": 2,
    "dataloader_pin_memory": True,
    
    # Salida
    "output_dir": "./models/mt5-small-mlsum-es-rtx3050",
    "logging_dir": "./logs",
    "report_to": "tensorboard",  # Monitoreo con TensorBoard
}

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD Y ROBUSTEZ
# ============================================================================
ROBUSTNESS_CONFIG = {
    # Checkpoints automáticos
    "auto_checkpoint": True,
    "checkpoint_on_error": True,
    
    # Reintentos en caso de error
    "max_retries": 3,
    "retry_delay": 10,  # segundos
    
    # Limpieza de memoria
    "clear_cache_every_n_steps": 100,
    
    # Validación
    "validate_before_training": True,
    "validate_after_training": True,
}

# ============================================================================
# CONFIGURACIÓN DE MÉTRICAS
# ============================================================================
METRICS_CONFIG = {
    "metrics": ["rouge1", "rouge2", "rougeL"],
    "use_stemmer": True,
}

# ============================================================================
# TIEMPO ESTIMADO (RTX 3050)
# ============================================================================
ESTIMATED_TIME = {
    "train_samples_1000": "30-45 min",
    "train_samples_5000": "2-3 horas",
    "train_samples_10000": "4-6 horas",
    "train_samples_50000": "20-24 horas",
}

# ============================================================================
# CONFIGURACIÓN COMPLETA
# ============================================================================
CONFIG = {
    **DEVICE_CONFIG,
    **MODEL_CONFIG,
    **DATASET_CONFIG,
    **TRAINING_CONFIG,
    **ROBUSTNESS_CONFIG,
    **METRICS_CONFIG,
}


def get_config():
    """Retorna la configuración completa"""
    return CONFIG


def print_config():
    """Imprime la configuración de forma legible"""
    print("=" * 70)
    print("CONFIGURACIÓN DE ENTRENAMIENTO - RTX 3050")
    print("=" * 70)
    
    print("\n📊 DATASET:")
    print(f"  - Nombre: {DATASET_CONFIG['dataset_name']} ({DATASET_CONFIG['dataset_config']})")
    print(f"  - Train: {DATASET_CONFIG['train_samples']:,} ejemplos")
    print(f"  - Validation: {DATASET_CONFIG['val_samples']:,} ejemplos")
    print(f"  - Test: {DATASET_CONFIG['test_samples']:,} ejemplos")
    
    print("\n🧠 MODELO:")
    print(f"  - Modelo: {MODEL_CONFIG['model_name']}")
    print(f"  - Max input: {MODEL_CONFIG['max_input_length']} tokens")
    print(f"  - Max output: {MODEL_CONFIG['max_target_length']} tokens")
    
    print("\n⚙️ ENTRENAMIENTO:")
    print(f"  - Batch size: {TRAINING_CONFIG['per_device_train_batch_size']}")
    print(f"  - Gradient accumulation: {TRAINING_CONFIG['gradient_accumulation_steps']}")
    print(f"  - Batch efectivo: {TRAINING_CONFIG['per_device_train_batch_size'] * TRAINING_CONFIG['gradient_accumulation_steps']}")
    print(f"  - Learning rate: {TRAINING_CONFIG['learning_rate']}")
    print(f"  - Épocas: {TRAINING_CONFIG['num_train_epochs']}")
    print(f"  - FP16: {TRAINING_CONFIG['fp16']}")
    
    print("\n💾 CHECKPOINTS:")
    print(f"  - Guardar cada: {TRAINING_CONFIG['save_steps']} steps")
    print(f"  - Evaluar cada: {TRAINING_CONFIG['eval_steps']} steps")
    print(f"  - Early stopping: {ROBUSTNESS_CONFIG['auto_checkpoint']}")
    
    print("\n⏱️ TIEMPO ESTIMADO:")
    samples = DATASET_CONFIG['train_samples']
    if samples <= 1000:
        time_est = ESTIMATED_TIME['train_samples_1000']
    elif samples <= 5000:
        time_est = ESTIMATED_TIME['train_samples_5000']
    elif samples <= 10000:
        time_est = ESTIMATED_TIME['train_samples_10000']
    else:
        time_est = ESTIMATED_TIME['train_samples_50000']
    print(f"  - Tiempo estimado: {time_est}")
    
    print("\n💾 SALIDA:")
    print(f"  - Modelo guardado en: {TRAINING_CONFIG['output_dir']}")
    print(f"  - Logs en: {TRAINING_CONFIG['logging_dir']}")
    
    print("=" * 70)


if __name__ == "__main__":
    print_config()
