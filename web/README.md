# 🌐 Video Summarizer AI - Interfaz Web Estática

## 📋 Descripción

Esta es una **versión estática de demostración** de la interfaz web del Video Summarizer AI. Está construida con HTML, CSS y JavaScript vanilla (sin frameworks), y simula el funcionamiento completo de la aplicación para mostrar cómo se vería en producción.

## ✨ Características

### 🎨 Diseño Moderno
- Interfaz responsive que se adapta a cualquier dispositivo
- Paleta de colores profesional (púrpura/azul)
- Animaciones suaves y transiciones elegantes
- Iconos de Font Awesome
- Gradientes y efectos visuales modernos

### 🚀 Funcionalidades Implementadas

1. **Upload de Videos**
   - Drag & drop para arrastrar videos
   - Click para seleccionar archivos
   - Preview del video cargado
   - Información del archivo (nombre, tamaño, duración)

2. **Configuración Avanzada**
   - Selector de modelo Whisper (tiny, base, small, medium, large)
   - Longitud del resumen (64, 128, 256, 512 tokens)
   - Número de beams para calidad
   - Detección automática de idioma

3. **Resultados en Pestañas**
   - **Resumen:** Muestra el resumen generado
   - **Transcripción:** Muestra la transcripción completa
   - **Estadísticas:** Métricas de procesamiento

4. **Descargas**
   - Descargar JSON con todos los datos
   - Descargar TXT con resumen y transcripción
   - Descargar solo transcripción

5. **Barra de Progreso**
   - Simulación realista del procesamiento
   - Muestra cada paso del pipeline

6. **Características Extra**
   - Copiar al portapapeles
   - Notificaciones toast
   - Scroll suave entre secciones
   - Animaciones al hacer scroll

## 📁 Estructura de Archivos

```
web/
├── index.html      # Página principal (HTML completo)
├── styles.css      # Estilos CSS modernos (~1000 líneas)
├── script.js       # JavaScript funcional (~500 líneas)
└── README.md       # Este archivo
```

## 🚀 Cómo Usar

### Opción 1: Abrir Directamente
Simplemente abre `index.html` en tu navegador favorito:
- Doble clic en el archivo
- O click derecho → Abrir con → Chrome/Firefox/Edge

### Opción 2: Servidor Local (Recomendado)
Para mejor funcionalidad, usa un servidor local:

**Python:**
```bash
cd web
python -m http.server 8000
# Abre: http://localhost:8000
```

**Node.js:**
```bash
cd web
npx serve
# Abre: http://localhost:5000
```

**VS Code:**
Usa la extensión "Live Server" y click derecho → "Open with Live Server"

## 🎯 Secciones de la Página

### 1️⃣ Hero Section
- Título llamativo
- Descripción del proyecto
- Botones de acción
- Estadísticas destacadas (95% ahorro, 40+ idiomas, GPU)

### 2️⃣ Features Section
- 6 tarjetas de características principales
- Iconos ilustrativos
- Descripción de cada funcionalidad
- Hover effects

### 3️⃣ Demo Section (⭐ Principal)
- **Lado izquierdo:** Upload y configuración
  - Área de drag & drop
  - Preview de video
  - Configuración avanzada
  - Botón "Procesar Video"

- **Lado derecho:** Resultados
  - Pestañas: Resumen, Transcripción, Estadísticas
  - Botones de descarga
  - Barra de progreso

### 4️⃣ About Section
- Stack tecnológico
- Logos de tecnologías usadas
- Información del proyecto
- Tarjetas informativas

### 5️⃣ Footer
- Enlaces a GitHub
- Información del proyecto
- Copyright

## 🎨 Paleta de Colores

```css
Primario:   #7c3aed (Púrpura)
Secundario: #3b82f6 (Azul)
Acento:     #f59e0b (Ámbar)
Fondo:      #f8fafc (Gris claro)
Oscuro:     #0f172a (Azul oscuro)
```

## 📱 Responsive Design

La interfaz se adapta perfectamente a:
- 📱 Móviles (320px+)
- 📱 Tablets (768px+)
- 💻 Laptops (1024px+)
- 🖥️ Desktops (1440px+)

Breakpoints principales:
- 768px: Cambio a layout móvil
- 1024px: Ajuste de grid de demo

## 🔧 Personalización

### Cambiar Colores
Edita las variables CSS en `styles.css`:
```css
:root {
    --primary-color: #7c3aed;  /* Tu color */
    --secondary-color: #3b82f6;
    /* ... más variables ... */
}
```

### Modificar Contenido
Edita directamente `index.html`:
- Títulos y descripciones
- Textos de las secciones
- Enlaces del footer

### Agregar Funcionalidades
Edita `script.js`:
- Función `processVideo()` para lógica real
- Integración con backend/API
- Validaciones adicionales

## 🌐 Integración con Backend

Para conectar con el backend Python/Gradio real:

1. **Modificar `processVideo()` en script.js:**
```javascript
async function processVideo() {
    const formData = new FormData();
    formData.append('video', selectedFile);
    
    const response = await fetch('http://localhost:7860/api/process', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    showResults(result);
}
```

2. **Agregar CORS en el servidor Python:**
```python
# Permitir peticiones desde la web estática
```

## 📊 Datos de Demostración

La versión actual usa datos simulados para mostrar cómo funcionaría:
- Transcripción de ejemplo sobre IA
- Resumen generado de ejemplo
- Estadísticas simuladas
- Progreso animado

## 🎯 Diferencias con Gradio

| Característica | Gradio | Web Estática |
|---------------|--------|--------------|
| Framework | Python/Gradio | HTML/CSS/JS |
| Backend | Integrado | Separado (API) |
| Deployment | Python server | Cualquier hosting |
| Personalización | Limitada | Total |
| Performance | Buena | Excelente |
| SEO | Limitado | Completo |

## 🚀 Deployment

### GitHub Pages
```bash
git add web/
git commit -m "Add static web interface"
git push origin main
# Activar GitHub Pages en Settings
```

### Netlify
```bash
# Arrastra la carpeta 'web' a Netlify
# O conecta el repo de GitHub
```

### Vercel
```bash
vercel web/
```

## 🔒 Seguridad

⚠️ **Nota:** Esta es una interfaz de demostración. Para producción:
- Validar todos los inputs en el backend
- Implementar rate limiting
- Sanitizar uploads de archivos
- Agregar autenticación si es necesario
- Usar HTTPS

## 📈 Mejoras Futuras

- [ ] Integración real con el backend Python
- [ ] Sistema de autenticación
- [ ] Historial de videos procesados
- [ ] Modo oscuro/claro
- [ ] Más idiomas en la interfaz
- [ ] Compartir resultados por URL
- [ ] Comparación de diferentes modelos

## 🤝 Contribuir

Si quieres mejorar la interfaz:
1. Fork el repositorio
2. Crea una branch: `git checkout -b feature/mejora`
3. Commit: `git commit -m "Descripción"`
4. Push: `git push origin feature/mejora`
5. Abre un Pull Request

## 📝 Licencia

MIT License - Proyecto académico UNSA

## 👨‍💻 Autor

Desarrollado como parte del Trabajo Interdisciplinar III  
Universidad Nacional de San Agustín de Arequipa

---

**¡Disfruta de la interfaz!** 🎉
