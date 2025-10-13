"""
Script de Entrenamiento Robusto para RTX 3050
Dataset: MLSUM (Español)
Modelo: mT5-small

Características:
- Optimizado para 4GB VRAM
- Checkpoints automáticos
- Early stopping
- Manejo de errores robusto
- Logging detallado
- Recuperación automática
"""

import os
import sys
import torch
import logging
import traceback
from datetime import datetime
from pathlib import Path

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent))

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback,
)
from datasets import load_dataset, DatasetDict
import evaluate
import numpy as np

from config_rtx3050 import CONFIG, print_config

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
def setup_logging():
    """Configura logging detallado"""
    log_dir = Path(CONFIG["logging_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"training_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


# ============================================================================
# VERIFICACIÓN DE GPU
# ============================================================================
def check_gpu(logger):
    """Verifica disponibilidad de GPU"""
    logger.info("=" * 70)
    logger.info("VERIFICACIÓN DE GPU")
    logger.info("=" * 70)
    
    if not torch.cuda.is_available():
        logger.error("❌ GPU no disponible. Entrenamiento será MUY lento en CPU")
        response = input("¿Continuar de todas formas? (s/n): ")
        if response.lower() != 's':
            sys.exit(1)
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    
    logger.info(f"✅ GPU detectada: {gpu_name}")
    logger.info(f"✅ VRAM disponible: {vram_gb:.2f} GB")
    logger.info(f"✅ CUDA version: {torch.version.cuda}")
    
    if vram_gb < 3.5:
        logger.warning("⚠️  VRAM baja (<4GB). Puede haber problemas de memoria")
    
    logger.info("=" * 70)
    return True


# ============================================================================
# LIMPIEZA DE MEMORIA
# ============================================================================
def clear_memory(logger):
    """Limpia memoria de GPU"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.debug("🧹 Memoria GPU limpiada")


# ============================================================================
# CARGA DE DATASET
# ============================================================================
def load_and_prepare_dataset(tokenizer, logger):
    """Carga y prepara el dataset MLSUM en español"""
    logger.info("=" * 70)
    logger.info("CARGANDO DATASET MLSUM (ESPAÑOL)")
    logger.info("=" * 70)
    
    try:
        # Cargar dataset
        logger.info(f"📥 Descargando dataset {CONFIG['dataset_name']}...")
        dataset = load_dataset(
            CONFIG["dataset_name"],
            CONFIG["dataset_config"],
            cache_dir=CONFIG["cache_dir"],
            trust_remote_code=True
        )
        
        logger.info(f"✅ Dataset cargado exitosamente")
        logger.info(f"  - Train: {len(dataset['train']):,} ejemplos")
        logger.info(f"  - Validation: {len(dataset['validation']):,} ejemplos")
        logger.info(f"  - Test: {len(dataset['test']):,} ejemplos")
        
        # Reducir tamaño si es necesario
        train_size = CONFIG["train_samples"]
        val_size = CONFIG["val_samples"]
        test_size = CONFIG["test_samples"]
        
        if train_size < len(dataset['train']):
            logger.info(f"📊 Reduciendo dataset a {train_size:,} ejemplos de entrenamiento...")
            dataset['train'] = dataset['train'].select(range(train_size))
            dataset['validation'] = dataset['validation'].select(range(val_size))
            dataset['test'] = dataset['test'].select(range(test_size))
            
            logger.info(f"✅ Dataset reducido:")
            logger.info(f"  - Train: {len(dataset['train']):,} ejemplos")
            logger.info(f"  - Validation: {len(dataset['validation']):,} ejemplos")
            logger.info(f"  - Test: {len(dataset['test']):,} ejemplos")
        
        # Mostrar ejemplo
        logger.info("\n📄 Ejemplo del dataset:")
        example = dataset['train'][0]
        logger.info(f"  Texto (primeros 200 chars): {example['text'][:200]}...")
        logger.info(f"  Resumen: {example['summary']}")
        
        # Tokenizar
        logger.info("\n🔤 Tokenizando dataset...")
        
        def preprocess_function(examples):
            """Preprocesa ejemplos para mT5"""
            # mT5 funciona bien con prefijos
            inputs = ["resumir: " + text for text in examples['text']]
            targets = examples['summary']
            
            model_inputs = tokenizer(
                inputs,
                max_length=CONFIG["max_input_length"],
                truncation=True,
                padding=False,  # Padding dinámico en el collator
            )
            
            labels = tokenizer(
                targets,
                max_length=CONFIG["max_target_length"],
                truncation=True,
                padding=False,
            )
            
            model_inputs["labels"] = labels["input_ids"]
            return model_inputs
        
        tokenized_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=dataset['train'].column_names,
            desc="Tokenizando"
        )
        
        logger.info("✅ Dataset tokenizado correctamente")
        logger.info("=" * 70)
        
        return tokenized_dataset
        
    except Exception as e:
        logger.error(f"❌ Error cargando dataset: {e}")
        logger.error(traceback.format_exc())
        raise


# ============================================================================
# MÉTRICAS
# ============================================================================
def setup_metrics(tokenizer, logger):
    """Configura métricas de evaluación"""
    logger.info("📊 Configurando métricas ROUGE...")
    
    rouge = evaluate.load("rouge")
    
    def compute_metrics(eval_pred):
        """Calcula métricas ROUGE"""
        predictions, labels = eval_pred
        
        # Decodificar predicciones
        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        
        # Reemplazar -100 en labels (padding)
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
        
        # Calcular ROUGE
        result = rouge.compute(
            predictions=decoded_preds,
            references=decoded_labels,
            use_stemmer=CONFIG.get("use_stemmer", True)
        )
        
        return {
            "rouge1": result["rouge1"],
            "rouge2": result["rouge2"],
            "rougeL": result["rougeL"],
        }
    
    logger.info("✅ Métricas configuradas")
    return compute_metrics


# ============================================================================
# ENTRENAMIENTO
# ============================================================================
def train_model(logger):
    """Función principal de entrenamiento"""
    
    try:
        # Limpiar memoria inicial
        clear_memory(logger)
        
        # Crear directorios
        output_dir = Path(CONFIG["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar tokenizer
        logger.info(f"🔤 Cargando tokenizer {CONFIG['model_name']}...")
        tokenizer = AutoTokenizer.from_pretrained(CONFIG["model_name"])
        logger.info("✅ Tokenizer cargado")
        
        # Cargar y preparar dataset
        tokenized_dataset = load_and_prepare_dataset(tokenizer, logger)
        
        # Cargar modelo
        logger.info(f"\n🧠 Cargando modelo {CONFIG['model_name']}...")
        model = AutoModelForSeq2SeqLM.from_pretrained(CONFIG["model_name"])
        
        if CONFIG.get("gradient_checkpointing", False):
            model.gradient_checkpointing_enable()
            logger.info("✅ Gradient checkpointing habilitado")
        
        logger.info("✅ Modelo cargado")
        
        # Configurar métricas
        compute_metrics = setup_metrics(tokenizer, logger)
        
        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            padding=True,
        )
        
        # Argumentos de entrenamiento
        logger.info("\n⚙️  Configurando argumentos de entrenamiento...")
        training_args = Seq2SeqTrainingArguments(
            output_dir=CONFIG["output_dir"],
            eval_strategy="steps",
            eval_steps=CONFIG["eval_steps"],
            save_strategy="steps",
            save_steps=CONFIG["save_steps"],
            save_total_limit=CONFIG["save_total_limit"],
            learning_rate=CONFIG["learning_rate"],
            per_device_train_batch_size=CONFIG["per_device_train_batch_size"],
            per_device_eval_batch_size=CONFIG["per_device_eval_batch_size"],
            gradient_accumulation_steps=CONFIG["gradient_accumulation_steps"],
            weight_decay=CONFIG["weight_decay"],
            warmup_steps=CONFIG["warmup_steps"],
            num_train_epochs=CONFIG["num_train_epochs"],
            max_grad_norm=CONFIG["max_grad_norm"],
            fp16=CONFIG["fp16"],
            logging_dir=CONFIG["logging_dir"],
            logging_steps=CONFIG["logging_steps"],
            report_to=CONFIG["report_to"],
            load_best_model_at_end=CONFIG["load_best_model_at_end"],
            metric_for_best_model=CONFIG["metric_for_best_model"],
            greater_is_better=CONFIG["greater_is_better"],
            predict_with_generate=True,
            generation_max_length=CONFIG["max_target_length"],
            dataloader_num_workers=CONFIG["dataloader_num_workers"],
            dataloader_pin_memory=CONFIG["dataloader_pin_memory"],
            remove_unused_columns=True,
            push_to_hub=False,
        )
        
        # Trainer
        logger.info("🏋️  Creando trainer...")
        trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            eval_dataset=tokenized_dataset["validation"],
            tokenizer=tokenizer,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=CONFIG.get("early_stopping_patience", 3)
                )
            ],
        )
        
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO ENTRENAMIENTO")
        logger.info("=" * 70)
        logger.info(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("")
        logger.info("⚠️  IMPORTANTE:")
        logger.info("  - El entrenamiento puede tomar varias horas")
        logger.info("  - Puedes detenerlo con Ctrl+C")
        logger.info("  - Los checkpoints se guardan automáticamente")
        logger.info("  - Monitorea con: tensorboard --logdir ./logs")
        logger.info("=" * 70)
        
        # ENTRENAR
        train_result = trainer.train()
        
        logger.info("=" * 70)
        logger.info("✅ ENTRENAMIENTO COMPLETADO")
        logger.info("=" * 70)
        logger.info(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"⏱️  Tiempo total: {train_result.metrics.get('train_runtime', 0) / 3600:.2f} horas")
        logger.info(f"📊 Loss final: {train_result.metrics.get('train_loss', 0):.4f}")
        
        # Guardar modelo final
        logger.info("\n💾 Guardando modelo final...")
        trainer.save_model(CONFIG["output_dir"])
        tokenizer.save_pretrained(CONFIG["output_dir"])
        logger.info(f"✅ Modelo guardado en: {CONFIG['output_dir']}")
        
        # Evaluación final
        logger.info("\n📊 Evaluación final en test set...")
        test_results = trainer.evaluate(tokenized_dataset["test"])
        
        logger.info("=" * 70)
        logger.info("📊 RESULTADOS FINALES")
        logger.info("=" * 70)
        logger.info(f"  ROUGE-1: {test_results.get('eval_rouge1', 0):.4f}")
        logger.info(f"  ROUGE-2: {test_results.get('eval_rouge2', 0):.4f}")
        logger.info(f"  ROUGE-L: {test_results.get('eval_rougeL', 0):.4f}")
        logger.info("=" * 70)
        
        # Guardar métricas
        metrics_file = output_dir / "final_metrics.txt"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            f.write("MÉTRICAS FINALES\n")
            f.write("=" * 50 + "\n")
            f.write(f"ROUGE-1: {test_results.get('eval_rouge1', 0):.4f}\n")
            f.write(f"ROUGE-2: {test_results.get('eval_rouge2', 0):.4f}\n")
            f.write(f"ROUGE-L: {test_results.get('eval_rougeL', 0):.4f}\n")
            f.write(f"Tiempo: {train_result.metrics.get('train_runtime', 0) / 3600:.2f} horas\n")
        
        logger.info(f"\n✅ Métricas guardadas en: {metrics_file}")
        logger.info("\n🎉 ¡ENTRENAMIENTO EXITOSO!")
        
        return trainer, test_results
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Entrenamiento interrumpido por el usuario")
        logger.info("💾 Los checkpoints se guardaron automáticamente")
        logger.info("📝 Puedes reanudar el entrenamiento más tarde")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"\n❌ ERROR DURANTE ENTRENAMIENTO: {e}")
        logger.error(traceback.format_exc())
        
        if "out of memory" in str(e).lower() or "oom" in str(e).lower():
            logger.error("\n💡 SUGERENCIAS PARA ERROR DE MEMORIA:")
            logger.error("  1. Reduce train_samples en config_rtx3050.py")
            logger.error("  2. Reduce per_device_train_batch_size a 1")
            logger.error("  3. Aumenta gradient_accumulation_steps")
            logger.error("  4. Reduce max_input_length a 256")
        
        raise


# ============================================================================
# MAIN
# ============================================================================
def main():
    """Función principal"""
    print("\n")
    print("=" * 70)
    print("  ENTRENAMIENTO ROBUSTO - RTX 3050")
    print("  Dataset: MLSUM (Español)")
    print("  Modelo: mT5-small")
    print("=" * 70)
    print("\n")
    
    # Setup
    logger = setup_logging()
    
    # Mostrar configuración
    print_config()
    
    # Verificar GPU
    has_gpu = check_gpu(logger)
    
    if not has_gpu:
        logger.warning("⚠️  Continuando sin GPU (muy lento)...")
    
    # Confirmar inicio
    print("\n")
    response = input("¿Iniciar entrenamiento? (s/n): ")
    if response.lower() != 's':
        logger.info("❌ Entrenamiento cancelado por el usuario")
        sys.exit(0)
    
    # Entrenar
    trainer, results = train_model(logger)
    
    print("\n")
    print("=" * 70)
    print("🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print("=" * 70)
    print(f"\n📁 Modelo guardado en: {CONFIG['output_dir']}")
    print(f"📊 Logs en: {CONFIG['logging_dir']}")
    print("\n💡 Próximos pasos:")
    print("  1. Prueba el modelo con: python src/inference.py")
    print("  2. Transcribe videos con: python src/transcribe_video.py")
    print("  3. Pipeline completo: python src/pipeline.py --mode full")
    print("\n")


if __name__ == "__main__":
    main()
