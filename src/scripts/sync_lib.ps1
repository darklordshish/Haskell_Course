# Синхронизация библиотеки категорного ядра из канонического репозитория.
#
# Источник правды: github.com/darklordshish/SubjectiveModeling (клон: ..\SubjectiveModeling).
# Направление всегда одно: РЕПОЗИТОРИЙ -> src/lib. Править src/lib напрямую нельзя:
# скрипт обнаружит дрейф и остановится, чтобы правки не потерялись.
#
# Запуск из корня Haskell_Course_git:
#   powershell -File src/scripts/sync_lib.ps1          # git pull + копирование
#   powershell -File src/scripts/sync_lib.ps1 -NoPull  # только копирование
#   powershell -File src/scripts/sync_lib.ps1 -Force   # затереть локальный дрейф src/lib

param(
    [switch]$NoPull,
    [switch]$Force
)

$repoRoot = Join-Path $PSScriptRoot "..\..\..\SubjectiveModeling"
$repoSrc  = Join-Path $repoRoot "src"
$dest     = Join-Path $PSScriptRoot "..\lib"

if (-not (Test-Path $repoSrc)) {
    Write-Error "Не найден клон канонического репозитория: $repoRoot`nСклонируй: git clone git@github.com:darklordshish/SubjectiveModeling.git (рядом с Haskell_Course_git)"
    exit 1
}

# 1. Актуализируем клон из GitHub
if (-not $NoPull) {
    Write-Host ">> git pull в $repoRoot"
    git -C $repoRoot pull --ff-only
    if ($LASTEXITCODE -ne 0) { Write-Error "git pull не прошёл (локальные коммиты в клоне? разреши вручную)"; exit 1 }
}

# 2. Проверка дрейфа: src/lib не должен отличаться от ПРОШЛОГО состояния репо
#    иначе кто-то правил копию напрямую — эти правки надо сначала перенести в репозиторий.
if ((Test-Path $dest) -and -not $Force) {
    $drift = @()
    Get-ChildItem $dest -Filter *.hs | ForEach-Object {
        $srcFile = Join-Path $repoSrc $_.Name
        if (-not (Test-Path $srcFile)) { $drift += "$($_.Name) (нет в репозитории)" }
        else {
            $h1 = (Get-FileHash $_.FullName).Hash
            $h2 = (Get-FileHash $srcFile).Hash
            if ($h1 -ne $h2) { $drift += $_.Name }
        }
    }
    if ($drift.Count -gt 0) {
        Write-Host "Найдены отличия src/lib от репозитория:" -ForegroundColor Yellow
        $drift | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
        Write-Host ""
        Write-Host "Если это правки ИЗ репозитория (после pull) — это норма, просто продолжаем."
        Write-Host "Если ты правил src/lib НАПРЯМУЮ — сначала перенеси правки в клон ($repoSrc),"
        Write-Host "закоммить и запушь их там, затем снова запусти синк."
        Write-Host "Затереть локальные отличия без переноса: повторный запуск с -Force."
        # различия после pull — ожидаемы; затираем только их, дрейф против HEAD клона до pull не отличить,
        # поэтому консервативно требуем явного подтверждения
        $answer = Read-Host "Продолжить копирование репозиторий -> src/lib? (y/N)"
        if ($answer -ne 'y') { Write-Host "Отменено."; exit 1 }
    }
}

# 3. Копирование
Copy-Item -Path (Join-Path $repoSrc "*.hs") -Destination $dest -Force
Write-Host ">> Синхронизировано: $repoSrc -> $dest"
Get-ChildItem $dest -Filter *.hs | ForEach-Object { Write-Host ("   {0}  {1}" -f $_.Name, $_.LastWriteTime) }
Write-Host ""
Write-Host "Дальше: перезапусти ядра ноутбуков (Kernel > Restart) или контейнер,"
Write-Host "и прогони Run All — :load подхватит новые версии модулей."
