"""
Model Training Module
Entrena modelos de resumen con fine-tuning usando Transformers
"""
import os
from pathlib import Path
from typing import Optional
import torch
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import load_from_disk
import evaluate
import numpy as np


class SummaryTrainer:
    """Clase para entrenar modelos de resumen"""
    
    def __init__(self, 
                 model_name: str = "google/mt5-small",
                 output_dir: str = "models/mt5-summarizer"):
        """
        Inicializa el entrenador
        
        Args:
            model_name: Nombre del modelo base (mt5-small, t5-small, bart, etc.)
            output_dir: Directorio donde guardar el modelo entrenado
        """
        self.model_name = model_name
        self.output_dir = output_dir
        
        print(f"Cargando modelo {model_name}...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Métricas para evaluación
        self.rouge = evaluate.load("rouge")
        
        # Device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando device: {self.device}")
        
    def compute_metrics(self, eval_pred):
        """
        Calcula métricas ROUGE para evaluación
        
        Args:
            eval_pred: Predicciones del modelo
            
        Returns:
            Diccionario con métricas
        """
        predictions, labels = eval_pred
        
        # Decodificar predicciones
        decoded_preds = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)
        
        # Reemplazar -100 en labels (usado para padding)
        labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
        decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)
        
        # Calcular ROUGE
        result = self.rouge.compute(
            predictions=decoded_preds,
            references=decoded_labels,
            use_stemmer=True
        )
        
        return {
            "rouge1": result["rouge1"],
            "rouge2": result["rouge2"],
            "rougeL": result["rougeL"],
        }
    
    def train(self,
              train_dataset,
              eval_dataset,
              num_train_epochs: int = 3,
              batch_size: int = 4,
              learning_rate: float = 5e-5,
              warmup_steps: int = 500,
              save_steps: int = 500,
              eval_steps: int = 500,
              max_steps: int = -1):
        """
        Entrena el modelo
        
        Args:
            train_dataset: Dataset de entrenamiento tokenizado
            eval_dataset: Dataset de validación tokenizado
            num_train_epochs: Número de épocas
            batch_size: Tamaño del batch
            learning_rate: Tasa de aprendizaje
            warmup_steps: Pasos de warmup
            save_steps: Cada cuántos pasos guardar checkpoint
            eval_steps: Cada cuántos pasos evaluar
            max_steps: Máximo de pasos (-1 para usar épocas)
        """
        # Crear data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model
        )
        
        # Configurar argumentos de entrenamiento
        training_args = Seq2SeqTrainingArguments(
            output_dir=self.output_dir,
            evaluation_strategy="steps",
            eval_steps=eval_steps,
            save_strategy="steps",
            save_steps=save_steps,
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_train_epochs,
            max_steps=max_steps,
            warmup_steps=warmup_steps,
            weight_decay=0.01,
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=100,
            predict_with_generate=True,
            fp16=torch.cuda.is_available(),  # Usar mixed precision si hay GPU
            push_to_hub=False,
            load_best_model_at_end=True,
            metric_for_best_model="rouge1",
            greater_is_better=True,
            save_total_limit=3,  # Solo guardar los 3 mejores checkpoints
        )
        
        # Crear trainer
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics
        )
        
        # Entrenar
        print("Iniciando entrenamiento...")
        train_result = trainer.train()
        
        # Guardar modelo final
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        # Guardar métricas
        metrics = train_result.metrics
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        
        print(f"Entrenamiento completado. Modelo guardado en {self.output_dir}")
        
        return trainer
    
    def evaluate(self, eval_dataset, trained_model_path: Optional[str] = None):
        """
        Evalúa el modelo en el dataset de evaluación
        
        Args:
            eval_dataset: Dataset de evaluación
            trained_model_path: Ruta del modelo entrenado (None para usar self.model)
        """
        if trained_model_path:
            print(f"Cargando modelo desde {trained_model_path}...")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(trained_model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(trained_model_path)
        
        # Configurar trainer solo para evaluación
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model
        )
        
        eval_args = Seq2SeqTrainingArguments(
            output_dir=self.output_dir,
            per_device_eval_batch_size=4,
            predict_with_generate=True,
            fp16=torch.cuda.is_available(),
        )
        
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=eval_args,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics
        )
        
        # Evaluar
        print("Evaluando modelo...")
        metrics = trainer.evaluate()
        
        print("\nMétricas de evaluación:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.4f}")
        
        return metrics


def main():
    """Ejemplo de uso"""
    # Cargar dataset procesado
    print("Cargando dataset procesado...")
    dataset = load_from_disk("data/processed/xsum_tokenized")
    
    # Crear entrenador
    trainer = SummaryTrainer(
        model_name="google/mt5-small",  # O "t5-small" para inglés
        output_dir="models/mt5-video-summarizer"
    )
    
    # Entrenar
    # NOTA: Ajusta estos parámetros según tu hardware
    trainer.train(
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        num_train_epochs=3,
        batch_size=4,  # Reducir si tienes problemas de memoria
        learning_rate=5e-5,
        warmup_steps=500,
        save_steps=1000,
        eval_steps=1000,
        # max_steps=3000  # Descomentar para entrenamiento rápido de prueba
    )
    
    # Evaluar
    if "test" in dataset:
        metrics = trainer.evaluate(dataset["test"])


if __name__ == "__main__":
    main()
