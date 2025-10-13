"""
Ejemplos de Uso del Sistema de Resumen de Videos
Ejecuta este archivo para ver ejemplos prácticos
"""

def ejemplo_1_transcripcion_basica():
    """Ejemplo 1: Transcribir un video simple"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Transcripción Básica")
    print("="*60)
    
    from transcribe_video import VideoTranscriber
    
    # Crear transcriptor
    transcriber = VideoTranscriber(model_size="base", language="es")
    
    # Transcribir un video (asegúrate de que el archivo exista)
    # video_path = "../videos/ejemplo.mp4"
    # transcript = transcriber.transcribe_video(video_path)
    # print(f"Texto transcrito: {transcript['text']}")
    
    print("Para usar este ejemplo:")
    print("1. Coloca un video en la carpeta 'videos/'")
    print("2. Descomenta las líneas del código")
    print("3. Ejecuta de nuevo")


def ejemplo_2_resumen_simple():
    """Ejemplo 2: Generar resumen de un texto"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Resumen Simple")
    print("="*60)
    
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch
    
    # Cargar modelo
    model_name = "google/mt5-small"
    print(f"Cargando modelo {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # Texto de ejemplo
    texto = """
    El aprendizaje profundo es una rama del machine learning que utiliza redes neuronales
    artificiales con múltiples capas para aprender representaciones jerárquicas de datos.
    Estas redes pueden aprender automáticamente características relevantes sin necesidad
    de ingeniería manual de características. El aprendizaje profundo ha revolucionado
    campos como la visión por computadora, el procesamiento de lenguaje natural y el
    reconocimiento de voz, logrando resultados que superan el desempeño humano en
    muchas tareas específicas.
    """
    
    # Generar resumen
    input_text = "resumir: " + texto
    inputs = tokenizer(input_text, max_length=512, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=128,
            num_beams=4,
            early_stopping=True
        )
    
    resumen = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    print(f"\nTexto original ({len(texto)} caracteres):")
    print(texto.strip())
    print(f"\nResumen generado ({len(resumen)} caracteres):")
    print(resumen)
    print(f"\nCompresión: {len(resumen)/len(texto):.2%}")


def ejemplo_3_preparar_dataset():
    """Ejemplo 3: Preparar dataset para entrenamiento"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Preparar Dataset")
    print("="*60)
    
    from prepare_dataset import DatasetPreparator
    
    # Inicializar preparador
    preparator = DatasetPreparator(model_name="google/mt5-small")
    
    # Cargar dataset público (solo para demostración)
    print("Cargando dataset de ejemplo (1000 muestras)...")
    
    # Descomentar para cargar dataset real
    # dataset = preparator.load_public_dataset(
    #     dataset_name="xsum",
    #     language="en",
    #     num_samples=1000
    # )
    # 
    # print(f"Dataset cargado: {len(dataset['train'])} ejemplos")
    # print(f"Ejemplo: {dataset['train'][0]}")
    
    print("\nPara usar este ejemplo:")
    print("1. Descomenta las líneas del código")
    print("2. El dataset se descargará automáticamente")
    print("3. Puede tomar varios minutos la primera vez")


def ejemplo_4_entrenar_modelo():
    """Ejemplo 4: Entrenar modelo (versión de demostración)"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Entrenamiento de Modelo")
    print("="*60)
    
    print("ADVERTENCIA: El entrenamiento real toma mucho tiempo.")
    print("Este es solo un ejemplo de código.")
    print()
    
    codigo = """
from train_model import SummaryTrainer
from datasets import load_from_disk

# Cargar dataset procesado
dataset = load_from_disk("data/processed/xsum_tokenized")

# Crear entrenador
trainer = SummaryTrainer(
    model_name="google/mt5-small",
    output_dir="models/mt5-video-summarizer"
)

# Entrenar (usar max_steps para prueba rápida)
trainer.train(
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    num_train_epochs=3,
    batch_size=4,
    max_steps=100  # Solo 100 pasos para prueba rápida
)
    """
    
    print("Código de ejemplo:")
    print(codigo)
    
    print("\nPara entrenar realmente:")
    print("1. Prepara tu dataset primero (ejemplo_3)")
    print("2. Ajusta los hiperparámetros según tu hardware")
    print("3. Ten paciencia, puede tomar horas")


def ejemplo_5_usar_modelo_entrenado():
    """Ejemplo 5: Usar modelo ya entrenado"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Inferencia con Modelo Entrenado")
    print("="*60)
    
    print("Este ejemplo requiere que tengas un modelo entrenado.")
    print()
    
    codigo = """
from inference import VideoSummarizer

# Cargar modelo entrenado
summarizer = VideoSummarizer(model_path="models/mt5-video-summarizer")

# Resumir un texto
texto = "Tu texto largo aquí..."
resumen = summarizer.summarize(texto)

print(f"Resumen: {resumen}")

# O resumir una transcripción completa
result = summarizer.summarize_transcript("videos/mi_video_transcript.json")
print(f"Resumen: {result['summary']}")
    """
    
    print("Código de ejemplo:")
    print(codigo)
    
    print("\nPara usar este ejemplo:")
    print("1. Primero entrena un modelo (ejemplo_4)")
    print("2. O descarga un modelo pre-entrenado")
    print("3. Ajusta la ruta del modelo según corresponda")


def ejemplo_6_pipeline_completo():
    """Ejemplo 6: Pipeline completo automatizado"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Pipeline Completo")
    print("="*60)
    
    print("El pipeline completo ejecuta todos los pasos automáticamente:")
    print()
    print("1. Transcripción de videos")
    print("2. Preparación de dataset")
    print("3. Entrenamiento del modelo")
    print("4. Generación de resúmenes")
    print()
    
    print("Comando para ejecutar:")
    print("  cd src")
    print("  python pipeline.py --mode full --video-dir ../videos --epochs 3")
    print()
    
    print("Otros modos disponibles:")
    print("  --mode inference : Solo resumir (con modelo pre-entrenado)")
    print("  --mode transcribe: Solo transcribir videos")
    print("  --mode train     : Solo entrenar modelo")


def menu_ejemplos():
    """Menú interactivo de ejemplos"""
    ejemplos = {
        '1': ('Transcripción Básica', ejemplo_1_transcripcion_basica),
        '2': ('Resumen Simple', ejemplo_2_resumen_simple),
        '3': ('Preparar Dataset', ejemplo_3_preparar_dataset),
        '4': ('Entrenar Modelo', ejemplo_4_entrenar_modelo),
        '5': ('Usar Modelo Entrenado', ejemplo_5_usar_modelo_entrenado),
        '6': ('Pipeline Completo', ejemplo_6_pipeline_completo),
    }
    
    print("\n" + "="*60)
    print("EJEMPLOS DE USO - SISTEMA DE RESUMEN DE VIDEOS")
    print("="*60)
    print("\nSelecciona un ejemplo para ver:")
    
    for key, (nombre, _) in ejemplos.items():
        print(f"  {key}. {nombre}")
    
    print("  0. Ejecutar todos los ejemplos")
    print("  q. Salir")
    print()
    
    while True:
        opcion = input("Selecciona una opción: ").strip().lower()
        
        if opcion == 'q':
            print("¡Hasta luego!")
            break
        elif opcion == '0':
            for _, (_, func) in ejemplos.items():
                func()
            break
        elif opcion in ejemplos:
            _, func = ejemplos[opcion]
            func()
            
            continuar = input("\n¿Ver otro ejemplo? (s/n): ").strip().lower()
            if continuar != 's':
                break
        else:
            print("Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    import sys
    
    # Si se pasa un argumento, ejecutar ese ejemplo
    if len(sys.argv) > 1:
        ejemplo_num = sys.argv[1]
        
        ejemplos = {
            '1': ejemplo_1_transcripcion_basica,
            '2': ejemplo_2_resumen_simple,
            '3': ejemplo_3_preparar_dataset,
            '4': ejemplo_4_entrenar_modelo,
            '5': ejemplo_5_usar_modelo_entrenado,
            '6': ejemplo_6_pipeline_completo,
        }
        
        if ejemplo_num in ejemplos:
            ejemplos[ejemplo_num]()
        else:
            print(f"Ejemplo {ejemplo_num} no encontrado")
            print("Ejemplos disponibles: 1, 2, 3, 4, 5, 6")
    else:
        # Menú interactivo
        menu_ejemplos()
