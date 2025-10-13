# Script PowerShell para instalar dependencias de FASE 2
# Interfaz Web (Gradio) + CLI Mejorada (Rich)

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 INSTALACIÓN DE INTERFACES DE USUARIO (FASE 2)" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Verificar si pip está disponible
try {
    $pipVersion = pip --version
    Write-Host "✅ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip no encontrado. Por favor instala Python primero." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Instalando dependencias de FASE 2..." -ForegroundColor Yellow
Write-Host ""

# Lista de paquetes a instalar
$paquetes = @(
    "gradio>=4.0.0",
    "rich>=13.7.0",
    "click>=8.1.0"
)

$exito = 0
$fallos = 0

foreach ($paquete in $paquetes) {
    Write-Host "📥 Instalando: $paquete" -ForegroundColor Cyan
    
    try {
        pip install "$paquete" --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ $paquete instalado" -ForegroundColor Green
            $exito++
        } else {
            Write-Host "   ❌ Error al instalar $paquete" -ForegroundColor Red
            $fallos++
        }
    } catch {
        Write-Host "   ❌ Error: $_" -ForegroundColor Red
        $fallos++
    }
    
    Write-Host ""
}

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE INSTALACIÓN" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✅ Exitosos: $exito" -ForegroundColor Green
Write-Host "❌ Fallidos: $fallos" -ForegroundColor Red
Write-Host ""

if ($fallos -eq 0) {
    Write-Host "🎉 ¡Todas las dependencias instaladas correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "   1. Interfaz Web:" -ForegroundColor Yellow
    Write-Host "      python src/web_app.py" -ForegroundColor White
    Write-Host ""
    Write-Host "   2. CLI Mejorada:" -ForegroundColor Yellow
    Write-Host "      python src/cli.py info" -ForegroundColor White
    Write-Host "      python src/cli.py procesar tu_video.mp4" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "⚠️  Algunas instalaciones fallaron." -ForegroundColor Yellow
    Write-Host "💡 Intenta instalar manualmente:" -ForegroundColor Cyan
    Write-Host "   pip install gradio rich click" -ForegroundColor White
}

Write-Host "=" * 70 -ForegroundColor Cyan
