"""
Dataset Preparation Module
Prepara y procesa datasets para fine-tuning de modelos de resumen
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from datasets import Dataset, DatasetDict, load_dataset
from transformers import AutoTokenizer
import random


class DatasetPreparator:
    """Clase para preparar datasets de resumen"""
    
    def __init__(self, model_name: str = "google/mt5-small"):
        """
        Inicializa el preparador de dataset
        
        Args:
            model_name: Nombre del modelo para el tokenizador
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def load_transcripts(self, transcript_dir: str) -> List[Dict]:
        """
        Carga transcripciones de un directorio
        
        Args:
            transcript_dir: Directorio con archivos JSON de transcripciones
            
        Returns:
            Lista de diccionarios con las transcripciones
        """
        transcripts = []
        transcript_files = Path(transcript_dir).glob('*_transcript.json')
        
        for file_path in transcript_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                transcripts.append({
                    'filename': file_path.stem,
                    'text': data['text'],
                    'segments': data.get('segments', [])
                })
        
        return transcripts
    
    def create_synthetic_summaries(self, transcripts: List[Dict], 
                                   summary_ratio: float = 0.3) -> List[Dict]:
        """
        Crea resúmenes sintéticos simples para demostración
        NOTA: En producción, deberías tener resúmenes reales o generarlos con GPT
        
        Args:
            transcripts: Lista de transcripciones
            summary_ratio: Proporción del texto a usar como resumen
            
        Returns:
            Lista con pares texto-resumen
        """
        dataset = []
        
        for transcript in transcripts:
            text = transcript['text']
            
            # Resumen simple: primeras oraciones (esto es solo para demo)
            sentences = text.split('. ')
            n_summary_sentences = max(1, int(len(sentences) * summary_ratio))
            summary = '. '.join(sentences[:n_summary_sentences]) + '.'
            
            dataset.append({
                'document': text,
                'summary': summary
            })
        
        return dataset
    
    def load_public_dataset(self, dataset_name: str = "xsum", 
                          language: str = "en",
                          num_samples: Optional[int] = None) -> DatasetDict:
        """
        Carga un dataset público para entrenamiento
        
        Args:
            dataset_name: Nombre del dataset (xsum, cnn_dailymail, etc.)
            language: Idioma del dataset
            num_samples: Número de muestras a cargar (None para todas)
            
        Returns:
            DatasetDict con splits train/validation/test
        """
        print(f"Cargando dataset {dataset_name}...")
        
        # Datasets populares en español
        if language == "es":
            # MLSUM es un dataset de resumen en español
            try:
                dataset = load_dataset("mlsum", "es")
            except:
                print("MLSUM no disponible, usando XSum en inglés")
                dataset = load_dataset("xsum")
        else:
            if dataset_name == "xsum":
                dataset = load_dataset("xsum")
            elif dataset_name == "cnn_dailymail":
                dataset = load_dataset("cnn_dailymail", "3.0.0")
            else:
                dataset = load_dataset(dataset_name)
        
        # Limitar número de muestras si es necesario
        if num_samples:
            dataset['train'] = dataset['train'].select(range(min(num_samples, len(dataset['train']))))
            if 'validation' in dataset:
                val_samples = min(num_samples // 10, len(dataset['validation']))
                dataset['validation'] = dataset['validation'].select(range(val_samples))
        
        return dataset
    
    def preprocess_function(self, examples, 
                          text_column: str = "document",
                          summary_column: str = "summary",
                          max_input_length: int = 512,
                          max_target_length: int = 128):
        """
        Preprocesa ejemplos para el modelo
        
        Args:
            examples: Batch de ejemplos
            text_column: Nombre de la columna con el texto
            summary_column: Nombre de la columna con el resumen
            max_input_length: Longitud máxima del input
            max_target_length: Longitud máxima del target
            
        Returns:
            Ejemplos tokenizados
        """
        # Agregar prefix para T5
        inputs = ["resumir: " + doc for doc in examples[text_column]]
        
        model_inputs = self.tokenizer(
            inputs,
            max_length=max_input_length,
            truncation=True,
            padding="max_length"
        )
        
        # Tokenizar targets
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(
                examples[summary_column],
                max_length=max_target_length,
                truncation=True,
                padding="max_length"
            )
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    def prepare_dataset(self, 
                       dataset: DatasetDict,
                       text_column: str = "document",
                       summary_column: str = "summary",
                       max_input_length: int = 512,
                       max_target_length: int = 128) -> DatasetDict:
        """
        Prepara el dataset completo para entrenamiento
        
        Args:
            dataset: Dataset a preparar
            text_column: Nombre de la columna con el texto
            summary_column: Nombre de la columna con el resumen
            max_input_length: Longitud máxima del input
            max_target_length: Longitud máxima del target
            
        Returns:
            Dataset tokenizado y preparado
        """
        print("Preprocesando dataset...")
        
        tokenized_dataset = dataset.map(
            lambda x: self.preprocess_function(
                x, text_column, summary_column, 
                max_input_length, max_target_length
            ),
            batched=True,
            remove_columns=dataset["train"].column_names
        )
        
        return tokenized_dataset
    
    def save_dataset(self, dataset: DatasetDict, output_dir: str):
        """Guarda el dataset procesado"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        dataset.save_to_disk(output_dir)
        print(f"Dataset guardado en {output_dir}")


def main():
    """Ejemplo de uso"""
    # Inicializar preparador
    preparator = DatasetPreparator(model_name="google/mt5-small")
    
    # Opción 1: Usar dataset público
    print("Opción 1: Cargando dataset público...")
    dataset = preparator.load_public_dataset(
        dataset_name="xsum",
        language="en",
        num_samples=1000  # Usar solo 1000 muestras para prueba
    )
    
    # Preparar dataset
    tokenized_dataset = preparator.prepare_dataset(
        dataset,
        text_column="document",
        summary_column="summary"
    )
    
    # Guardar
    preparator.save_dataset(tokenized_dataset, "data/processed/xsum_tokenized")
    
    print(f"Dataset preparado con {len(tokenized_dataset['train'])} ejemplos de entrenamiento")
    
    # Opción 2: Usar tus propias transcripciones (comentado para ejemplo)
    # transcripts = preparator.load_transcripts("videos/transcripts")
    # custom_dataset = preparator.create_synthetic_summaries(transcripts)
    # ... procesar y guardar


if __name__ == "__main__":
    main()
