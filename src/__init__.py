"""
Video Summarizer Package
Sistema de resumen automático de videos educativos
"""

__version__ = "1.0.0"
__author__ = "UNSA - Trabajo Interdisciplinar III"

from .transcribe_video import VideoTranscriber
from .prepare_dataset import DatasetPreparator
from .train_model import SummaryTrainer
from .inference import VideoSummarizer

__all__ = [
    'VideoTranscriber',
    'DatasetPreparator',
    'SummaryTrainer',
    'VideoSummarizer'
]
