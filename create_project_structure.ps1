# ============================================================
# Create Recommendation Application Folder Structure
# ============================================================

$root = "app\application\recommendation"

# Root
New-Item -ItemType Directory -Force -Path $root | Out-Null

# Subfolders
$folders = @(
    "commands",
    "dto",
    "handlers",
    "mappers",
    "queries",
    "validators"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $folder) | Out-Null
}

# Root __init__.py
New-Item -ItemType File -Force -Path (Join-Path $root "__init__.py") | Out-Null

# ------------------------------------------------------------
# Commands
# ------------------------------------------------------------
$commandFiles = @(
    "__init__.py",
    "create_recommendation.py",
    "add_solution.py",
    "update_roadmap.py",
    "submit_recommendation.py",
    "approve_recommendation.py"
)

foreach ($file in $commandFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "commands\$file") | Out-Null
}

# ------------------------------------------------------------
# DTO
# ------------------------------------------------------------
$dtoFiles = @(
    "__init__.py",
    "recommendation_dto.py",
    "solution_dto.py",
    "roadmap_phase_dto.py"
)

foreach ($file in $dtoFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "dto\$file") | Out-Null
}

# ------------------------------------------------------------
# Handlers
# ------------------------------------------------------------
$handlerFiles = @(
    "__init__.py",
    "create_recommendation_handler.py",
    "add_solution_handler.py",
    "update_roadmap_handler.py",
    "submit_recommendation_handler.py",
    "approve_recommendation_handler.py"
)

foreach ($file in $handlerFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "handlers\$file") | Out-Null
}

# ------------------------------------------------------------
# Mappers
# ------------------------------------------------------------
$mapperFiles = @(
    "__init__.py",
    "recommendation_mapper.py",
    "solution_mapper.py",
    "roadmap_phase_mapper.py"
)

foreach ($file in $mapperFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "mappers\$file") | Out-Null
}

# ------------------------------------------------------------
# Validators
# ------------------------------------------------------------
$validatorFiles = @(
    "__init__.py",
    "create_recommendation_validator.py",
    "add_solution_validator.py",
    "update_roadmap_validator.py",
    "submit_recommendation_validator.py",
    "approve_recommendation_validator.py"
)

foreach ($file in $validatorFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "validators\$file") | Out-Null
}

# ------------------------------------------------------------
# Queries
# ------------------------------------------------------------
$queryFiles = @(
    "__init__.py"
)

foreach ($file in $queryFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $root "queries\$file") | Out-Null
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host " Recommendation Application Created" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $root" -ForegroundColor Cyan
Write-Host ""