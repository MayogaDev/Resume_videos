# Documentación del Proyecto

Esta carpeta contiene el informe técnico del Sistema de Resumen Automático de Videos Educativos.

## 📄 Archivos

- **informe_tecnico.tex**: Documento principal en LaTeX
- **Arquitectura_general.svg**: Diagrama de arquitectura del sistema (debe estar en el directorio raíz)

## 🔧 Compilación del Documento

### Opción 1: Overleaf (Recomendado)

1. Ve a [Overleaf](https://www.overleaf.com/)
2. Crea un nuevo proyecto (New Project → Upload Project)
3. Sube `informe_tecnico.tex` y `Arquitectura_general.svg`
4. Compila automáticamente (Ctrl+S)
5. Descarga el PDF generado

### Opción 2: LaTeX Local

#### Instalación (Windows):

1. **Instala MiKTeX**:
   - Descarga: https://miktex.org/download
   - Instala con todas las opciones por defecto

2. **Instala TeXstudio** (Editor recomendado):
   - Descarga: https://www.texstudio.org/
   - Instala con todas las opciones por defecto

#### Compilación:

1. Abre `informe_tecnico.tex` en TeXstudio
2. Presiona F5 o clic en el botón verde "Build & View"
3. El PDF se generará automáticamente

#### Comandos de Terminal:

```powershell
# En la carpeta documentation/
pdflatex informe_tecnico.tex
pdflatex informe_tecnico.tex  # Segunda vez para índice y referencias
```

### Opción 3: VS Code + LaTeX Workshop

1. **Instala la extensión**:
   - Busca "LaTeX Workshop" en VS Code
   - Instala de James Yu

2. **Compila**:
   - Abre `informe_tecnico.tex`
   - Guarda el archivo (Ctrl+S)
   - Se compila automáticamente
   - Vista previa: Ctrl+Alt+V

## 📊 Inserción de Capturas de Pantalla

El documento tiene espacios marcados para insertar capturas de cada capa:

```latex
% Busca estos comentarios en el documento:
% ESPACIO PARA CAPTURA DE PANTALLA DE CAPA DE ENTRADA
% ESPACIO PARA CAPTURA DE PANTALLA DE CAPA DE TRANSCRIPCIÓN
% etc...
```

### Cómo Insertar Imágenes:

1. **Guarda tus capturas** en la carpeta `documentation/images/` con nombres descriptivos:
   - `capa_entrada.png`
   - `capa_transcripcion.png`
   - `capa_entrenamiento.png`
   - `capa_inferencia.png`
   - `capa_presentacion.png`
   - `capa_infraestructura.png`
   - `capa_monitoreo.png`

2. **Reemplaza los bloques de texto** por código LaTeX:

```latex
% Antes (espacio vacío):
\fbox{\parbox{0.9\textwidth}{\centering\vspace{3cm}
    \textit{[Insertar aquí captura de la Capa de Entrada]}\\
    \vspace{0.3cm}
    Componentes: Usuario, Videos Educativos
    \vspace{3cm}}}

% Después (con imagen):
\includegraphics[width=0.9\textwidth]{images/capa_entrada.png}
```

### Ejemplo Completo:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{images/capa_entrada.png}
    \caption{Capa de Entrada - Interacción con el Usuario}
    \label{fig:capa_entrada}
\end{figure}
```

## 📝 Estructura del Documento

### Sección 1: Pipeline Final
- 1.1 Introducción
- 1.2 Arquitectura General del Sistema (con diagrama SVG)
- 1.3 Descripción Detallada de las Capas:
  - Capa de Entrada
  - Capa de Transcripción
  - Capa de Entrenamiento
  - Capa de Inferencia
  - Capa de Presentación
  - Capa de Infraestructura
  - Capa de Monitoreo
- 1.4 Flujo de Procesamiento
- 1.5 Ventajas de la Arquitectura

### Sección 2: Avance de Implementación
- 2.1 Estado Actual del Proyecto
- 2.2 Componentes Implementados:
  - Infraestructura
  - Configuración del Entorno
  - Preparación del Dataset
  - Entrenamiento del Modelo
  - Resultados y Métricas
  - Logs y Monitoreo
- 2.3 Módulos Pendientes
- 2.4 Cronograma
- 2.5 Desafíos Superados
- 2.6 Conclusiones

## 🎨 Personalización

### Datos del Estudiante:

Busca y reemplaza en la portada (líneas ~90-95):

```latex
\begin{tabular}{ll}
    \textbf{Estudiante:} & [Nombre del Estudiante] \\  % <-- EDITAR AQUÍ
    \textbf{Código:} & [Código] \\                     % <-- EDITAR AQUÍ
    \textbf{Docente:} & [Nombre del Docente] \\        % <-- EDITAR AQUÍ
\end{tabular}
```

### Colores:

Cambia los colores en las líneas 30-32:

```latex
\definecolor{primarycolor}{RGB}{25, 118, 210}     % Azul principal
\definecolor{secondarycolor}{RGB}{76, 175, 80}    % Verde secundario
\definecolor{accentcolor}{RGB}{244, 67, 54}       % Rojo acento
```

## 📋 Checklist de Entrega

- [ ] Compilar el documento y generar PDF
- [ ] Insertar imagen `Arquitectura_general.svg` (ya incluida)
- [ ] Tomar capturas de cada capa del diagrama PlantUML
- [ ] Insertar las 7 capturas en sus respectivas secciones
- [ ] Completar datos personales en la portada
- [ ] Revisar ortografía y formato
- [ ] Verificar que todas las figuras tengan caption
- [ ] Comprobar que el índice esté correcto
- [ ] Exportar a PDF final

## 📦 Archivos Necesarios

```
documentation/
├── informe_tecnico.tex          # Documento principal
├── README.md                    # Este archivo
├── images/                      # Crear esta carpeta
│   ├── capa_entrada.png
│   ├── capa_transcripcion.png
│   ├── capa_entrenamiento.png
│   ├── capa_inferencia.png
│   ├── capa_presentacion.png
│   ├── capa_infraestructura.png
│   └── capa_monitoreo.png
└── ../Arquitectura_general.svg  # En directorio raíz
```

## 🐛 Solución de Problemas

### Error: "File not found: Arquitectura_general.svg"
**Solución**: Verifica que el archivo SVG esté en el directorio raíz del proyecto (un nivel arriba de `documentation/`)

### Error: "Package not found"
**Solución**: En MiKTeX, acepta la instalación automática de paquetes cuando te lo pida

### Las imágenes no se ven
**Solución**: Asegúrate de que la carpeta `images/` existe y contiene las capturas con los nombres correctos

### El documento no compila
**Solución**: 
1. Compila 2 veces (para actualizar índice y referencias)
2. Borra archivos auxiliares (.aux, .log, .toc) e intenta de nuevo

## 📧 Contacto

Para dudas sobre la compilación del documento, consulta:
- Documentación LaTeX: https://www.latex-project.org/help/documentation/
- Overleaf Guides: https://www.overleaf.com/learn

---

**Última actualización**: Octubre 2025
