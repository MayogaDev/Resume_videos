"""
Utilidades generales para el proyecto
"""
import os
import json
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd


def create_directories(base_dir: str = "."):
    """Crea la estructura de directorios del proyecto"""
    directories = [
        "data/raw",
        "data/processed",
        "models",
        "videos",
        "notebooks",
        "logs"
    ]
    
    for directory in directories:
        path = Path(base_dir) / directory
        path.mkdir(parents=True, exist_ok=True)
    
    print(f"Estructura de directorios creada en {base_dir}")


def load_json(file_path: str) -> Dict:
    """Carga un archivo JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, file_path: str):
    """Guarda datos en un archivo JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def count_tokens(text: str, tokenizer) -> int:
    """Cuenta el número de tokens en un texto"""
    tokens = tokenizer.encode(text)
    return len(tokens)


def split_text_by_sentences(text: str, max_sentences: int = 5) -> List[str]:
    """Divide un texto en chunks por oraciones"""
    sentences = text.split('. ')
    chunks = []
    
    for i in range(0, len(sentences), max_sentences):
        chunk = '. '.join(sentences[i:i+max_sentences])
        chunks.append(chunk)
    
    return chunks


def calculate_compression_ratio(original: str, summary: str) -> float:
    """Calcula el ratio de compresión"""
    if len(original) == 0:
        return 0.0
    return len(summary) / len(original)


def plot_training_metrics(metrics_file: str, output_path: str = None):
    """
    Visualiza las métricas de entrenamiento
    
    Args:
        metrics_file: Ruta al archivo de métricas (JSON)
        output_path: Ruta donde guardar la gráfica (opcional)
    """
    metrics = load_json(metrics_file)
    
    # Crear gráfica
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Loss
    axes[0, 0].plot(metrics.get('train_loss', []))
    axes[0, 0].set_title('Training Loss')
    axes[0, 0].set_xlabel('Steps')
    axes[0, 0].set_ylabel('Loss')
    
    # ROUGE-1
    axes[0, 1].plot(metrics.get('eval_rouge1', []))
    axes[0, 1].set_title('ROUGE-1')
    axes[0, 1].set_xlabel('Steps')
    axes[0, 1].set_ylabel('Score')
    
    # ROUGE-2
    axes[1, 0].plot(metrics.get('eval_rouge2', []))
    axes[1, 0].set_title('ROUGE-2')
    axes[1, 0].set_xlabel('Steps')
    axes[1, 0].set_ylabel('Score')
    
    # ROUGE-L
    axes[1, 1].plot(metrics.get('eval_rougeL', []))
    axes[1, 1].set_title('ROUGE-L')
    axes[1, 1].set_xlabel('Steps')
    axes[1, 1].set_ylabel('Score')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"Gráfica guardada en {output_path}")
    else:
        plt.show()


def compare_summaries(original: str, summaries: Dict[str, str]):
    """
    Compara múltiples resúmenes del mismo texto
    
    Args:
        original: Texto original
        summaries: Diccionario con nombre_modelo: resumen
    """
    print("="*60)
    print("COMPARACIÓN DE RESÚMENES")
    print("="*60)
    print(f"\nTexto original ({len(original)} caracteres):")
    print(original[:200] + "...\n")
    
    for model_name, summary in summaries.items():
        compression = calculate_compression_ratio(original, summary)
        print(f"\n{model_name}:")
        print(f"  Longitud: {len(summary)} caracteres")
        print(f"  Compresión: {compression:.2%}")
        print(f"  Resumen: {summary}\n")
        print("-"*60)


def analyze_dataset(dataset_dir: str):
    """
    Analiza estadísticas del dataset
    
    Args:
        dataset_dir: Directorio con archivos JSON de transcripciones
    """
    files = list(Path(dataset_dir).glob('*_transcript.json'))
    
    if not files:
        print(f"No se encontraron archivos en {dataset_dir}")
        return
    
    stats = {
        'num_files': len(files),
        'total_chars': 0,
        'avg_chars': 0,
        'min_chars': float('inf'),
        'max_chars': 0,
        'lengths': []
    }
    
    for file_path in files:
        data = load_json(str(file_path))
        text = data.get('text', '')
        length = len(text)
        
        stats['total_chars'] += length
        stats['lengths'].append(length)
        stats['min_chars'] = min(stats['min_chars'], length)
        stats['max_chars'] = max(stats['max_chars'], length)
    
    stats['avg_chars'] = stats['total_chars'] / stats['num_files']
    
    print("="*60)
    print("ESTADÍSTICAS DEL DATASET")
    print("="*60)
    print(f"Número de archivos: {stats['num_files']}")
    print(f"Total de caracteres: {stats['total_chars']:,}")
    print(f"Promedio de caracteres: {stats['avg_chars']:.0f}")
    print(f"Mínimo: {stats['min_chars']:,} caracteres")
    print(f"Máximo: {stats['max_chars']:,} caracteres")
    
    # Histograma
    plt.figure(figsize=(10, 6))
    plt.hist(stats['lengths'], bins=20, edgecolor='black')
    plt.xlabel('Longitud (caracteres)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Longitudes de Transcripciones')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return stats


def export_summaries_to_csv(summaries_dir: str, output_file: str = "summaries.csv"):
    """
    Exporta todos los resúmenes a un archivo CSV
    
    Args:
        summaries_dir: Directorio con archivos de resumen
        output_file: Nombre del archivo CSV de salida
    """
    files = list(Path(summaries_dir).glob('*_summary.json'))
    
    data = []
    for file_path in files:
        summary_data = load_json(str(file_path))
        data.append({
            'filename': summary_data['filename'],
            'original_length': summary_data['original_length'],
            'summary_length': summary_data['summary_length'],
            'compression_ratio': summary_data['compression_ratio'],
            'summary': summary_data['summary']
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Resúmenes exportados a {output_file}")
    
    return df


if __name__ == "__main__":
    # Ejemplo de uso
    print("Utilidades del proyecto de resumen de videos")
    print("Importa este módulo en tus scripts para usar las funciones")
