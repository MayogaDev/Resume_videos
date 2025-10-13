"""
CLI Mejorada con Rich para Resumen de Videos
Interfaz de línea de comandos hermosa con colores y barras de progreso

Autor: Sistema de Resumen de Videos Educativos
Fecha: Octubre 2025
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
import time

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Rich para CLI hermosa
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn
)
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box
from rich.layout import Layout
from rich.live import Live

# Click para argumentos
import click

# Nuestros módulos
try:
    from transcribe_video import VideoTranscriber
    from inference import VideoSummarizer
except ImportError:
    print("❌ Error: No se pueden importar transcribe_video o inference")
    sys.exit(1)


console = Console()


def mostrar_banner():
    """Muestra el banner de bienvenida"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎬  SISTEMA DE RESUMEN AUTOMÁTICO DE VIDEOS EDUCATIVOS  🎬  ║
║                                                               ║
║        Whisper (Transcripción) + mT5 (Resumen) = ❤️          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def mostrar_info_sistema():
    """Muestra información del sistema"""
    table = Table(title="ℹ️ Información del Sistema", box=box.ROUNDED)
    
    table.add_column("Componente", style="cyan", no_wrap=True)
    table.add_column("Estado", style="magenta")
    table.add_column("Detalles", style="green")
    
    # Verificar Whisper
    try:
        import whisper
        whisper_status = "✅ Instalado"
        whisper_version = whisper.__version__ if hasattr(whisper, '__version__') else "N/A"
    except ImportError:
        whisper_status = "❌ No instalado"
        whisper_version = "N/A"
    
    # Verificar PyTorch
    try:
        import torch
        torch_status = "✅ Instalado"
        torch_version = torch.__version__
        gpu_info = f"GPU: {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "CPU only"
    except ImportError:
        torch_status = "❌ No instalado"
        torch_version = "N/A"
        gpu_info = "N/A"
    
    # Verificar Transformers
    try:
        import transformers
        transformers_status = "✅ Instalado"
        transformers_version = transformers.__version__
    except ImportError:
        transformers_status = "❌ No instalado"
        transformers_version = "N/A"
    
    table.add_row("Whisper", whisper_status, whisper_version)
    table.add_row("PyTorch", torch_status, f"{torch_version} ({gpu_info})")
    table.add_row("Transformers", transformers_status, transformers_version)
    
    console.print(table)


def procesar_video_interactivo(
    video_path,
    modelo_path,
    whisper_model="base",
    output_dir="outputs",
    formato="both"
):
    """
    Procesa un video de forma interactiva con Rich
    
    Args:
        video_path: Ruta al video
        modelo_path: Ruta al modelo mT5
        whisper_model: Modelo de Whisper
        output_dir: Directorio de salida
        formato: Formato de salida (txt, json, both)
    """
    video_name = Path(video_path).stem
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Panel de información
    info_panel = Panel(
        f"[cyan]📁 Video:[/cyan] {Path(video_path).name}\n"
        f"[cyan]🧠 Modelo:[/cyan] {Path(modelo_path).name}\n"
        f"[cyan]🎤 Whisper:[/cyan] {whisper_model}\n"
        f"[cyan]📂 Salida:[/cyan] {output_dir}",
        title="[bold yellow]📋 Configuración[/bold yellow]",
        border_style="yellow"
    )
    console.print(info_panel)
    console.print()
    
    # Progress bar con Rich
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        
        # Tarea global
        task_total = progress.add_task(
            "[cyan]Progreso total...",
            total=100
        )
        
        try:
            # PASO 0: Inicialización
            progress.update(task_total, advance=5, description="[yellow]🔧 Inicializando modelos...")
            
            console.print("\n[bold blue]═══ PASO 1/3: TRANSCRIPCIÓN ═══[/bold blue]")
            transcriber = VideoTranscriber(model_size=whisper_model)
            progress.update(task_total, advance=10)
            
            # PASO 1: Transcripción
            progress.update(task_total, description="[yellow]🎤 Transcribiendo audio...")
            console.print("[cyan]🎤 Extrayendo audio y transcribiendo con Whisper...[/cyan]")
            
            transcripcion = transcriber.transcribe(video_path)
            progress.update(task_total, advance=30)
            
            if not transcripcion or len(transcripcion.strip()) < 50:
                console.print("[red]❌ Error: Transcripción muy corta o vacía[/red]")
                return False
            
            console.print(f"[green]✅ Transcripción completada: {len(transcripcion.split())} palabras[/green]")
            
            # PASO 2: Resumen
            console.print("\n[bold blue]═══ PASO 2/3: GENERACIÓN DE RESUMEN ═══[/bold blue]")
            progress.update(task_total, advance=5, description="[yellow]🧠 Cargando modelo mT5...")
            
            summarizer = VideoSummarizer(model_path=modelo_path)
            progress.update(task_total, advance=10)
            
            progress.update(task_total, description="[yellow]📝 Generando resumen...")
            console.print("[cyan]📝 Generando resumen con mT5...[/cyan]")
            
            resumen = summarizer.generate_summary(transcripcion, max_length=150, num_beams=4)
            progress.update(task_total, advance=20)
            
            console.print(f"[green]✅ Resumen generado: {len(resumen.split())} palabras[/green]")
            
            # PASO 3: Guardar resultados
            console.print("\n[bold blue]═══ PASO 3/3: GUARDANDO RESULTADOS ═══[/bold blue]")
            progress.update(task_total, description="[yellow]💾 Guardando archivos...")
            
            # Calcular estadísticas
            stats = {
                "video": video_name,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "transcripcion": {
                    "caracteres": len(transcripcion),
                    "palabras": len(transcripcion.split()),
                },
                "resumen": {
                    "caracteres": len(resumen),
                    "palabras": len(resumen.split()),
                },
                "compresion": {
                    "ratio_caracteres": len(resumen) / len(transcripcion),
                    "ratio_palabras": len(resumen.split()) / len(transcripcion.split())
                }
            }
            
            archivos_generados = []
            
            # Guardar TXT
            if formato in ["txt", "both"]:
                txt_path = os.path.join(output_dir, f"{video_name}_resumen.txt")
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"RESUMEN DEL VIDEO: {video_name}\n")
                    f.write(f"Fecha: {stats['timestamp']}\n")
                    f.write("=" * 70 + "\n\n")
                    f.write("RESUMEN:\n")
                    f.write("-" * 70 + "\n")
                    f.write(resumen + "\n\n")
                    f.write("=" * 70 + "\n\n")
                    f.write("TRANSCRIPCIÓN COMPLETA:\n")
                    f.write("-" * 70 + "\n")
                    f.write(transcripcion + "\n")
                archivos_generados.append(txt_path)
                console.print(f"[green]✅ TXT guardado: {Path(txt_path).name}[/green]")
            
            # Guardar JSON
            if formato in ["json", "both"]:
                json_path = os.path.join(output_dir, f"{video_name}_resumen.json")
                json_output = {
                    "video": video_name,
                    "timestamp": stats['timestamp'],
                    "transcripcion": transcripcion,
                    "resumen": resumen,
                    "estadisticas": stats
                }
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_output, f, indent=2, ensure_ascii=False)
                archivos_generados.append(json_path)
                console.print(f"[green]✅ JSON guardado: {Path(json_path).name}[/green]")
            
            progress.update(task_total, advance=20, description="[green]✅ Completado!")
            
            # Mostrar resultados
            console.print("\n" + "=" * 70)
            mostrar_resultados(resumen, transcripcion, stats, archivos_generados)
            
            return True
            
        except Exception as e:
            console.print(f"\n[red]❌ Error durante el procesamiento: {str(e)}[/red]")
            import traceback
            console.print(traceback.format_exc())
            return False


def mostrar_resultados(resumen, transcripcion, stats, archivos):
    """Muestra los resultados de forma visual"""
    
    # Panel del resumen
    resumen_panel = Panel(
        resumen,
        title="[bold green]✨ RESUMEN GENERADO[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(resumen_panel)
    console.print()
    
    # Tabla de estadísticas
    stats_table = Table(title="📊 Estadísticas", box=box.DOUBLE_EDGE)
    stats_table.add_column("Métrica", style="cyan", no_wrap=True)
    stats_table.add_column("Transcripción", justify="right", style="yellow")
    stats_table.add_column("Resumen", justify="right", style="green")
    stats_table.add_column("Compresión", justify="right", style="magenta")
    
    stats_table.add_row(
        "Palabras",
        f"{stats['transcripcion']['palabras']:,}",
        f"{stats['resumen']['palabras']:,}",
        f"{stats['compresion']['ratio_palabras']:.1%}"
    )
    
    stats_table.add_row(
        "Caracteres",
        f"{stats['transcripcion']['caracteres']:,}",
        f"{stats['resumen']['caracteres']:,}",
        f"{stats['compresion']['ratio_caracteres']:.1%}"
    )
    
    reduccion = (1 - stats['compresion']['ratio_palabras']) * 100
    stats_table.add_row(
        "Reducción",
        "",
        "",
        f"[bold]{reduccion:.1f}%[/bold]"
    )
    
    console.print(stats_table)
    console.print()
    
    # Archivos generados
    files_tree = Tree("📁 [bold cyan]Archivos Generados[/bold cyan]")
    for archivo in archivos:
        size_mb = os.path.getsize(archivo) / (1024 * 1024)
        files_tree.add(f"[green]{Path(archivo).name}[/green] ({size_mb:.2f} MB)")
    
    console.print(files_tree)
    console.print()


@click.group()
def cli():
    """
    Sistema de Resumen Automático de Videos Educativos
    
    Herramienta de línea de comandos con interfaz hermosa
    """
    pass


@cli.command()
@click.argument('video', type=click.Path(exists=True))
@click.option('--modelo', '-m', default='models/mt5-video-summarizer-final',
              help='Ruta al modelo mT5')
@click.option('--whisper', '-w', default='base',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']),
              help='Modelo de Whisper')
@click.option('--output', '-o', default='outputs',
              help='Directorio de salida')
@click.option('--formato', '-f', default='both',
              type=click.Choice(['txt', 'json', 'both']),
              help='Formato de salida')
def procesar(video, modelo, whisper, output, formato):
    """
    Procesa un video y genera su resumen
    
    Ejemplo:
        python src/cli.py procesar mi_video.mp4
    """
    mostrar_banner()
    
    # Verificar que el video existe
    if not os.path.exists(video):
        console.print(f"[red]❌ Video no encontrado: {video}[/red]")
        sys.exit(1)
    
    # Procesar
    success = procesar_video_interactivo(
        video_path=video,
        modelo_path=modelo,
        whisper_model=whisper,
        output_dir=output,
        formato=formato
    )
    
    if success:
        console.print("\n[bold green]🎉 ¡Procesamiento completado exitosamente![/bold green]")
    else:
        console.print("\n[bold red]❌ El procesamiento falló[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('carpeta', type=click.Path(exists=True))
@click.option('--modelo', '-m', default='models/mt5-video-summarizer-final')
@click.option('--whisper', '-w', default='base',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']))
@click.option('--output', '-o', default='outputs')
def batch(carpeta, modelo, whisper, output):
    """
    Procesa múltiples videos en una carpeta
    
    Ejemplo:
        python src/cli.py batch mis_videos/
    """
    mostrar_banner()
    
    # Buscar videos
    extensiones = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    videos = []
    for ext in extensiones:
        videos.extend(Path(carpeta).glob(f"*{ext}"))
    
    if not videos:
        console.print(f"[red]❌ No se encontraron videos en: {carpeta}[/red]")
        sys.exit(1)
    
    console.print(f"[cyan]📁 Encontrados {len(videos)} videos para procesar[/cyan]\n")
    
    # Confirmar
    if not Confirm.ask("¿Deseas continuar?"):
        console.print("[yellow]⚠️  Operación cancelada[/yellow]")
        sys.exit(0)
    
    # Procesar cada video
    exitosos = 0
    fallidos = 0
    
    for i, video in enumerate(videos, 1):
        console.print(f"\n[bold cyan]{'=' * 70}[/bold cyan]")
        console.print(f"[bold cyan]VIDEO {i}/{len(videos)}: {video.name}[/bold cyan]")
        console.print(f"[bold cyan]{'=' * 70}[/bold cyan]\n")
        
        success = procesar_video_interactivo(
            video_path=str(video),
            modelo_path=modelo,
            whisper_model=whisper,
            output_dir=output,
            formato="both"
        )
        
        if success:
            exitosos += 1
        else:
            fallidos += 1
        
        time.sleep(1)  # Pausa entre videos
    
    # Resumen final
    console.print("\n" + "=" * 70)
    console.print("[bold]📊 RESUMEN DEL PROCESAMIENTO POR LOTES[/bold]")
    console.print("=" * 70)
    console.print(f"[green]✅ Exitosos: {exitosos}[/green]")
    console.print(f"[red]❌ Fallidos: {fallidos}[/red]")
    console.print(f"[cyan]📁 Total procesados: {exitosos + fallidos}[/cyan]")
    console.print("=" * 70)


@cli.command()
def info():
    """
    Muestra información del sistema y dependencias
    """
    mostrar_banner()
    mostrar_info_sistema()
    
    console.print("\n[bold cyan]💡 Comandos disponibles:[/bold cyan]")
    console.print("  • [green]procesar[/green] - Procesa un video individual")
    console.print("  • [green]batch[/green]    - Procesa múltiples videos")
    console.print("  • [green]info[/green]     - Muestra esta información")
    console.print("\n[dim]Usa --help en cualquier comando para más detalles[/dim]")


if __name__ == '__main__':
    cli()
