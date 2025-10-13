"""
Script completo para entrenar el modelo con un dataset
Ejecuta este script para todo el proceso de entrenamiento
"""
from prepare_dataset import DatasetPreparator
from train_model import SummaryTrainer
from datasets import load_from_disk
import sys
import os


def entrenar_con_dataset_publico():
    """Opción 1: Entrenar con dataset público (XSum o MLSUM)"""
    print("="*60)
    print("ENTRENAMIENTO CON DATASET PÚBLICO")
    print("="*60)
    
    # Configuración
    MODEL_NAME = "google/mt5-small"  # Cambiar a "t5-small" para inglés
    DATASET_NAME = "xsum"            # Cambiar a "mlsum" para español
    LANGUAGE = "en"                  # Cambiar a "es" para español
    NUM_SAMPLES = 5000               # Número de ejemplos (más = mejor pero más lento)
    OUTPUT_DIR = "../models/mt5-video-summarizer"
    
    # Paso 1: Cargar y preparar dataset
    print("\n[1/3] Cargando dataset...")
    print(f"   Dataset: {DATASET_NAME}")
    print(f"   Idioma: {LANGUAGE}")
    print(f"   Muestras: {NUM_SAMPLES}")
    
    preparator = DatasetPreparator(model_name=MODEL_NAME)
    
    try:
        dataset = preparator.load_public_dataset(
            dataset_name=DATASET_NAME,
            language=LANGUAGE,
            num_samples=NUM_SAMPLES
        )
        print(f"   ✅ Dataset cargado: {len(dataset['train'])} ejemplos de entrenamiento")
    except Exception as e:
        print(f"   ❌ Error al cargar dataset: {e}")
        print("\n   Intenta con:")
        print("   - dataset_name='xsum' y language='en'")
        print("   - O instala el dataset manualmente")
        return
    
    # Paso 2: Tokenizar
    print("\n[2/3] Tokenizando dataset...")
    tokenized_dataset = preparator.prepare_dataset(
        dataset,
        text_column="document",
        summary_column="summary",
        max_input_length=512,
        max_target_length=128
    )
    
    # Guardar dataset procesado
    dataset_path = f"../data/processed/{DATASET_NAME}_tokenized"
    preparator.save_dataset(tokenized_dataset, dataset_path)
    print(f"   ✅ Dataset tokenizado y guardado en {dataset_path}")
    
    # Paso 3: Entrenar
    print("\n[3/3] Entrenando modelo...")
    print(f"   Modelo base: {MODEL_NAME}")
    print(f"   Salida: {OUTPUT_DIR}")
    
    trainer = SummaryTrainer(
        model_name=MODEL_NAME,
        output_dir=OUTPUT_DIR
    )
    
    # Configuración de entrenamiento
    print("\n   Configuración:")
    print("   - Modo: PRUEBA RÁPIDA (max_steps=500)")
    print("   - Épocas: 1")
    print("   - Batch size: 4")
    print("   - Learning rate: 5e-5")
    print("\n   ⏰ Tiempo estimado: 10-20 minutos en CPU, 5-10 min en GPU")
    print("\n   Iniciando entrenamiento...")
    
    trainer.train(
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        num_train_epochs=1,
        batch_size=4,
        learning_rate=5e-5,
        warmup_steps=100,
        max_steps=500,  # CAMBIAR A -1 para entrenamiento completo
        save_steps=100,
        eval_steps=100
    )
    
    # Resultado
    print("\n" + "="*60)
    print("✅ ¡ENTRENAMIENTO COMPLETADO!")
    print("="*60)
    print(f"\n📁 Modelo guardado en: {OUTPUT_DIR}")
    print(f"📊 Métricas guardadas en: {OUTPUT_DIR}/logs")
    
    print("\n📋 Próximos pasos:")
    print("   1. Evaluar el modelo en el test set")
    print("   2. Probar con inference.py para generar resúmenes")
    print("   3. Comparar con el modelo base sin fine-tuning")
    
    print("\n💡 Para entrenamiento completo:")
    print("   - Edita max_steps=-1 en este script")
    print("   - Aumenta num_train_epochs=3")
    print("   - Tiempo estimado: 2-4 horas")


def entrenar_con_dataset_guardado():
    """Opción 2: Entrenar con dataset ya procesado"""
    print("="*60)
    print("ENTRENAMIENTO CON DATASET GUARDADO")
    print("="*60)
    
    dataset_path = "../data/processed/xsum_tokenized"
    
    if not os.path.exists(dataset_path):
        print(f"\n❌ Dataset no encontrado en {dataset_path}")
        print("\nPrimero ejecuta la opción 1 para preparar el dataset")
        return
    
    print(f"\n📂 Cargando dataset desde: {dataset_path}")
    dataset = load_from_disk(dataset_path)
    print(f"   ✅ Dataset cargado: {len(dataset['train'])} ejemplos")
    
    # Entrenar
    print("\n🏋️ Entrenando modelo...")
    trainer = SummaryTrainer(
        model_name="google/mt5-small",
        output_dir="../models/mt5-video-summarizer"
    )
    
    trainer.train(
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        num_train_epochs=3,
        batch_size=4,
        learning_rate=5e-5,
        max_steps=500,
        save_steps=100,
        eval_steps=100
    )
    
    print("\n✅ ¡Entrenamiento completado!")


def menu():
    """Menú interactivo"""
    print("\n" + "="*60)
    print("ENTRENAMIENTO DEL MODELO DE RESUMEN")
    print("="*60)
    
    print("\nOpciones:")
    print("  1. Entrenar con dataset público (XSum/MLSUM)")
    print("  2. Entrenar con dataset ya procesado")
    print("  3. Ver información de datasets disponibles")
    print("  0. Salir")
    
    opcion = input("\nSelecciona una opción: ").strip()
    
    if opcion == "1":
        entrenar_con_dataset_publico()
    elif opcion == "2":
        entrenar_con_dataset_guardado()
    elif opcion == "3":
        mostrar_info_datasets()
    elif opcion == "0":
        print("¡Hasta luego!")
    else:
        print("Opción inválida")


def mostrar_info_datasets():
    """Muestra información sobre datasets disponibles"""
    print("\n" + "="*60)
    print("DATASETS DISPONIBLES")
    print("="*60)
    
    print("\n📚 DATASETS EN INGLÉS:")
    print("\n1. XSum (Extreme Summarization)")
    print("   - Fuente: Noticias BBC")
    print("   - Ejemplos: ~200,000")
    print("   - Estilo: Resúmenes muy cortos (1 oración)")
    print("   - Uso: dataset_name='xsum', language='en'")
    
    print("\n2. CNN/DailyMail")
    print("   - Fuente: Noticias CNN y Daily Mail")
    print("   - Ejemplos: ~300,000")
    print("   - Estilo: Resúmenes de párrafo")
    print("   - Uso: dataset_name='cnn_dailymail', language='en'")
    
    print("\n📚 DATASETS EN ESPAÑOL:")
    print("\n1. MLSUM")
    print("   - Fuente: Noticias en español")
    print("   - Ejemplos: ~266,000")
    print("   - Estilo: Resúmenes de párrafo")
    print("   - Uso: dataset_name='mlsum', language='es'")
    
    print("\n2. WikiLingua (Español)")
    print("   - Fuente: Wikipedia")
    print("   - Ejemplos: Variable")
    print("   - Estilo: Resúmenes técnicos")
    print("   - Uso: Requiere código personalizado")
    
    print("\n💡 RECOMENDACIONES:")
    print("   - Para empezar: XSum (en inglés) o MLSUM (en español)")
    print("   - Para proyecto: Crea tu propio dataset con videos académicos")
    print("   - Para mejor calidad: Combina dataset público + personalizado")
    
    print("\n📊 TAMAÑO RECOMENDADO:")
    print("   - Prueba rápida: 1,000 - 5,000 ejemplos")
    print("   - Entrenamiento normal: 10,000 - 50,000 ejemplos")
    print("   - Entrenamiento completo: 50,000+ ejemplos")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--rapido":
            entrenar_con_dataset_publico()
        elif sys.argv[1] == "--info":
            mostrar_info_datasets()
        else:
            print("Uso:")
            print("  python entrenar_completo.py           # Menú interactivo")
            print("  python entrenar_completo.py --rapido  # Entrenamiento directo")
            print("  python entrenar_completo.py --info    # Info de datasets")
    else:
        menu()
