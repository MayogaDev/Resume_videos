// ============================================
// VARIABLES GLOBALES
// ============================================
let selectedFile = null;
let processingData = {
    summary: '',
    transcription: '',
    stats: {}
};

// ============================================
// EVENT LISTENERS
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    animateOnScroll();
});

function initializeEventListeners() {
    // Upload area
    const uploadArea = document.getElementById('uploadArea');
    const videoInput = document.getElementById('videoInput');
    
    if (uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
    }
    
    if (videoInput) {
        videoInput.addEventListener('change', handleFileSelect);
    }
}

// ============================================
// FILE HANDLING
// ============================================
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = '#7c3aed';
    e.currentTarget.style.background = '#faf5ff';
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = '#a78bfa';
    e.currentTarget.style.background = 'white';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const uploadArea = e.currentTarget;
    uploadArea.style.borderColor = '#a78bfa';
    uploadArea.style.background = 'white';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('video/')) {
            handleFile(file);
        } else {
            showNotification('Por favor, selecciona un archivo de video válido', 'error');
        }
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    selectedFile = file;
    
    // Mostrar preview
    const uploadArea = document.getElementById('uploadArea');
    const videoPreview = document.getElementById('videoPreview');
    const videoPlayer = document.getElementById('videoPlayer');
    
    uploadArea.style.display = 'none';
    videoPreview.style.display = 'block';
    
    // Cargar video
    const url = URL.createObjectURL(file);
    videoPlayer.src = url;
    
    // Actualizar información
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    
    // Obtener duración cuando se cargue el video
    videoPlayer.addEventListener('loadedmetadata', function() {
        document.getElementById('videoDuration').textContent = formatDuration(videoPlayer.duration);
    });
    
    showNotification('Video cargado correctamente', 'success');
}

// ============================================
// VIDEO PROCESSING (SIMULADO)
// ============================================
function processVideo() {
    if (!selectedFile) {
        showNotification('Por favor, selecciona un video primero', 'error');
        return;
    }
    
    // Mostrar sección de resultados y progreso
    const resultsSection = document.getElementById('resultsSection');
    const progressSection = document.getElementById('progressSection');
    
    resultsSection.style.display = 'flex';
    progressSection.style.display = 'block';
    
    // Scroll a resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Simulación de procesamiento
    simulateProcessing();
}

function simulateProcessing() {
    const steps = [
        { percent: 10, text: 'Extrayendo audio del video...' },
        { percent: 30, text: 'Transcribiendo con Whisper...' },
        { percent: 60, text: 'Generando resumen con mT5...' },
        { percent: 85, text: 'Calculando métricas...' },
        { percent: 100, text: 'Proceso completado!' }
    ];
    
    let currentStep = 0;
    
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            updateProgress(steps[currentStep].percent, steps[currentStep].text);
            currentStep++;
        } else {
            clearInterval(interval);
            setTimeout(() => {
                showResults();
            }, 500);
        }
    }, 1500);
}

function updateProgress(percent, text) {
    document.getElementById('progressFill').style.width = percent + '%';
    document.getElementById('progressPercent').textContent = percent + '%';
    document.getElementById('progressText').textContent = text;
}

function showResults() {
    // Ocultar progreso
    document.getElementById('progressSection').style.display = 'none';
    
    // Datos de ejemplo
    const exampleTranscription = `En este video exploramos los fundamentos de la inteligencia artificial y el aprendizaje automático. 
    
Comenzamos explicando qué es el machine learning y cómo las computadoras pueden aprender de los datos sin ser programadas explícitamente para cada tarea específica. Vimos diferentes tipos de aprendizaje: supervisado, no supervisado y por refuerzo.

Después, nos adentramos en las redes neuronales artificiales, inspiradas en el funcionamiento del cerebro humano. Explicamos cómo funcionan las neuronas artificiales, las capas ocultas y el proceso de propagación hacia adelante y hacia atrás.

También cubrimos aplicaciones prácticas de la IA en la vida cotidiana: desde asistentes virtuales como Siri y Alexa, hasta sistemas de recomendación en Netflix y Spotify, pasando por vehículos autónomos y diagnóstico médico asistido.

Finalmente, discutimos los desafíos éticos y sociales de la IA, incluyendo temas de privacidad, sesgo algorítmico y el futuro del trabajo en la era de la automatización. Es crucial desarrollar IA de manera responsable y equitativa.`;

    const exampleSummary = `Este video presenta los conceptos fundamentales de inteligencia artificial y machine learning. Se explican los tres tipos principales de aprendizaje automático y el funcionamiento de las redes neuronales. Se muestran aplicaciones prácticas en asistentes virtuales, sistemas de recomendación y vehículos autónomos. También se abordan los desafíos éticos como privacidad, sesgos algorítmicos y el impacto en el empleo.`;
    
    // Actualizar contenido
    document.getElementById('transcriptionText').textContent = exampleTranscription;
    document.getElementById('summaryText').textContent = exampleSummary;
    
    // Actualizar estadísticas
    const transcriptionWords = exampleTranscription.split(/\s+/).length;
    const summaryWords = exampleSummary.split(/\s+/).length;
    const compressionRate = ((1 - summaryWords / transcriptionWords) * 100).toFixed(1);
    
    document.getElementById('processingTime').textContent = '45.3s';
    document.getElementById('wordCount').textContent = transcriptionWords + ' palabras';
    document.getElementById('compressionRate').textContent = compressionRate + '%';
    document.getElementById('detectedLanguage').textContent = 'Español';
    document.getElementById('confidence').textContent = '94.5%';
    document.getElementById('modelUsed').textContent = 'mT5-small';
    
    // Guardar datos
    processingData = {
        transcription: exampleTranscription,
        summary: exampleSummary,
        stats: {
            processingTime: '45.3s',
            wordCount: transcriptionWords,
            compressionRate: compressionRate + '%',
            language: 'Español',
            confidence: '94.5%',
            model: 'mT5-small',
            whisperModel: document.getElementById('whisperModel').value,
            summaryLength: document.getElementById('summaryLength').value,
            numBeams: document.getElementById('numBeams').value
        }
    };
    
    showNotification('¡Procesamiento completado con éxito!', 'success');
}

// ============================================
// TAB NAVIGATION
// ============================================
function showTab(tabName) {
    // Ocultar todos los tabs
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Desactivar botones
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // Mostrar tab seleccionado
    document.getElementById(tabName + 'Tab').classList.add('active');
    
    // Activar botón
    event.target.classList.add('active');
}

// ============================================
// COPY & DOWNLOAD FUNCTIONS
// ============================================
function copyText(elementId) {
    const text = document.getElementById(elementId).textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Texto copiado al portapapeles', 'success');
    }).catch(() => {
        showNotification('Error al copiar texto', 'error');
    });
}

function downloadJSON() {
    const data = {
        video: {
            name: selectedFile ? selectedFile.name : 'example_video.mp4',
            size: selectedFile ? formatFileSize(selectedFile.size) : 'N/A',
        },
        configuration: processingData.stats,
        transcription: processingData.transcription,
        summary: processingData.summary,
        timestamp: new Date().toISOString()
    };
    
    downloadFile(JSON.stringify(data, null, 2), 'resultado.json', 'application/json');
    showNotification('Descargando JSON...', 'success');
}

function downloadTXT() {
    const content = `
VIDEO SUMMARIZER AI - RESULTADOS
================================

VIDEO: ${selectedFile ? selectedFile.name : 'example_video.mp4'}
FECHA: ${new Date().toLocaleString('es-ES')}
MODELO: ${processingData.stats.model}

RESUMEN:
--------
${processingData.summary}

TRANSCRIPCIÓN COMPLETA:
-----------------------
${processingData.transcription}

ESTADÍSTICAS:
-------------
- Tiempo de procesamiento: ${processingData.stats.processingTime}
- Palabras en transcripción: ${processingData.stats.wordCount}
- Tasa de compresión: ${processingData.stats.compressionRate}
- Idioma detectado: ${processingData.stats.language}
- Confianza: ${processingData.stats.confidence}
`;
    
    downloadFile(content, 'resultado.txt', 'text/plain');
    showNotification('Descargando TXT...', 'success');
}

function downloadTranscription() {
    downloadFile(processingData.transcription, 'transcripcion.txt', 'text/plain');
    showNotification('Descargando transcripción...', 'success');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type: type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

function getIconSVG(type) {
    const icons = {
        success: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
        error: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`,
        info: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`
    };
    return icons[type] || icons.info;
}

function showNotification(message, type = 'info') {
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 400px;
    `;

    const iconSVG = getIconSVG(type);
    notification.innerHTML = `<div style="display: flex; align-items: center; flex-shrink: 0;">${iconSVG}</div> <span>${message}</span>`;

    document.body.appendChild(notification);

    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// ============================================
// NAVIGATION FUNCTIONS
// ============================================
function scrollToDemo() {
    document.getElementById('demo').scrollIntoView({ behavior: 'smooth' });
}

function showInfo() {
    document.getElementById('about').scrollIntoView({ behavior: 'smooth' });
}

function showDocumentation() {
    showNotification('Documentación disponible en el repositorio de GitHub', 'info');
    window.open('https://github.com/MayogaDev/Resume_videos', '_blank');
}

// ============================================
// SCROLL ANIMATIONS
// ============================================
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });
    
    // Observar elementos
    document.querySelectorAll('.feature-card, .stat-card, .tech-card, .info-card').forEach(el => {
        observer.observe(el);
    });
}

// ============================================
// SMOOTH SCROLL FOR ALL LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ============================================
// CSS ANIMATIONS (agregar al head si no existe)
// ============================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
