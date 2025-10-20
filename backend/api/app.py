"""
REST API - Flask Application
API REST para el sistema de resumen de videos
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import logging
import os

from backend.services.video_processor import VideoProcessorService
from backend.database.connection import DatabaseManager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para frontend

# Inicializar servicio (lazy loading de modelos)
processor = None

def get_processor():
    """Obtiene la instancia del procesador (lazy loading)"""
    global processor
    if processor is None:
        whisper_model = os.getenv('WHISPER_MODEL', 'base')
        summarizer_model = os.getenv('SUMMARIZER_MODEL', None)

        processor = VideoProcessorService(
            whisper_model=whisper_model,
            summarizer_model=summarizer_model
        )
        logger.info("Servicio de procesamiento inicializado")

    return processor


# ===== ENDPOINTS =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado del servidor"""
    return jsonify({
        'status': 'healthy',
        'message': 'API REST funcionando correctamente'
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas de la base de datos"""
    try:
        proc = get_processor()
        stats = proc.get_database_stats()
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/process', methods=['POST'])
def process_video():
    """
    Procesa un video: transcripción + resumen

    Body (JSON):
        {
            "video_path": "/path/to/video.mp4",
            "create_summary": true,
            "save_outputs": true
        }
    """
    try:
        data = request.get_json()

        if not data or 'video_path' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "video_path" requerido'
            }), 400

        video_path = data['video_path']
        create_summary = data.get('create_summary', True)
        save_outputs = data.get('save_outputs', True)

        # Verificar que el video existe
        if not Path(video_path).exists():
            return jsonify({
                'success': False,
                'error': f'Video no encontrado: {video_path}'
            }), 404

        # Procesar video
        proc = get_processor()
        result = proc.process_video(
            video_path=video_path,
            create_summary=create_summary,
            save_outputs=save_outputs
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"Error en proceso de video: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/video/history', methods=['GET'])
def get_video_history():
    """
    Obtiene el historial de un video

    Query params:
        video_path: Ruta al video
    """
    try:
        video_path = request.args.get('video_path')

        if not video_path:
            return jsonify({
                'success': False,
                'error': 'Parámetro "video_path" requerido'
            }), 400

        proc = get_processor()
        history = proc.get_video_history(video_path)

        if history:
            return jsonify({
                'success': True,
                'history': {
                    'video': history['video'].__dict__ if history['video'] else None,
                    'transcription': history['transcription'].__dict__ if history['transcription'] else None,
                    'summary': history['summary'].__dict__ if history['summary'] else None
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Video no encontrado en el historial'
            }), 404

    except Exception as e:
        logger.error(f"Error al obtener historial: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/videos', methods=['GET'])
def get_all_videos():
    """Obtiene todos los videos procesados"""
    try:
        from backend.database.models import Video

        proc = get_processor()
        limit = request.args.get('limit', 100, type=int)

        videos = Video.get_all(proc.db, limit=limit)

        return jsonify({
            'success': True,
            'count': len(videos),
            'videos': [v.__dict__ for v in videos]
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener videos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_processing_history():
    """
    Obtiene el historial completo de procesamiento con transcripciones y resúmenes

    Query params:
        limit: Número máximo de videos a retornar (default: 20)
        offset: Offset para paginación (default: 0)
    """
    try:
        from backend.database.models import Video, Transcription, Summary

        proc = get_processor()
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Obtener videos
        all_videos = Video.get_all(proc.db, limit=limit + offset)
        videos = all_videos[offset:offset + limit] if len(all_videos) > offset else []

        history = []
        for video in videos:
            # Obtener transcripción asociada
            transcription = Transcription.get_by_video_id(proc.db, video.id)

            # Obtener resumen si existe transcripción
            summary = None
            if transcription:
                summary = Summary.get_by_transcription_id(proc.db, transcription.id)

            # Construir entrada del historial
            history_entry = {
                'video': {
                    'id': video.id,
                    'filename': video.filename,
                    'filepath': video.filepath,
                    'size_mb': round(video.file_size / (1024 * 1024), 2) if video.file_size else 0,
                    'duration': video.duration,
                    'created_at': video.created_at
                },
                'transcription': {
                    'id': transcription.id,
                    'word_count': transcription.word_count,
                    'char_count': transcription.char_count,
                    'language': transcription.language,
                    'model': transcription.model_used,
                    'processing_time': transcription.processing_time,
                    'created_at': transcription.created_at
                } if transcription else None,
                'summary': {
                    'id': summary.id,
                    'word_count': len(summary.summary_text.split()) if summary.summary_text else 0,
                    'compression_ratio': summary.compression_ratio,
                    'model': summary.model_used,
                    'processing_time': summary.processing_time,
                    'created_at': summary.created_at
                } if summary else None,
                'has_transcription': transcription is not None,
                'has_summary': summary is not None
            }

            history.append(history_entry)

        return jsonify({
            'success': True,
            'count': len(history),
            'total': proc.get_database_stats().get('total_videos', 0),
            'offset': offset,
            'limit': limit,
            'history': history
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener historial: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/video/<int:video_id>', methods=['GET'])
def get_video_details(video_id):
    """
    Obtiene los detalles completos de un video incluyendo transcripción y resumen

    Path params:
        video_id: ID del video
    """
    try:
        from backend.database.models import Video, Transcription, Summary

        proc = get_processor()

        # Obtener video
        video = Video.get_by_id(proc.db, video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': f'Video con ID {video_id} no encontrado'
            }), 404

        # Obtener transcripción
        transcription = Transcription.get_by_video_id(proc.db, video_id)

        # Obtener resumen
        summary = None
        if transcription:
            summary = Summary.get_by_transcription_id(proc.db, transcription.id)

        result = {
            'success': True,
            'video': video.__dict__,
            'transcription': {
                **transcription.__dict__,
                'text_preview': transcription.text[:500] + '...' if len(transcription.text) > 500 else transcription.text
            } if transcription else None,
            'summary': {
                **summary.__dict__,
                'text': summary.summary_text
            } if summary else None
        }

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error al obtener detalles del video {video_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Manejo de error 404"""
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejo de error 500"""
    logger.error(f"Error interno del servidor: {error}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500


def run_server(host='0.0.0.0', port=5000, debug=False):
    """
    Ejecuta el servidor Flask

    Args:
        host: Host para el servidor
        port: Puerto para el servidor
        debug: Modo debug
    """
    logger.info(f"Iniciando servidor en http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
