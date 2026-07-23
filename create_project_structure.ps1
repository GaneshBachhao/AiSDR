# ==========================================================
# Create Presentation Layer Structure
# ==========================================================

$root = "app\presentation"

# Root
New-Item -ItemType Directory -Force -Path $root | Out-Null

# API
New-Item -ItemType Directory -Force -Path "$root\api" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\api\dependencies" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\api\middleware" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\api\exception_handlers" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\api\routers" | Out-Null

# Schemas
New-Item -ItemType Directory -Force -Path "$root\schemas" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\schemas\requests" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\schemas\responses" | Out-Null

# ==========================================================
# Python Files
# ==========================================================

$files = @(

    # Root
    "$root\__init__.py",
    "$root\main.py",
    "$root\startup.py",

    # API
    "$root\api\__init__.py",

    # Dependencies
    "$root\api\dependencies\__init__.py",
    "$root\api\dependencies\ai.py",
    "$root\api\dependencies\persistence.py",

    # Middleware
    "$root\api\middleware\__init__.py",
    "$root\api\middleware\correlation_id.py",
    "$root\api\middleware\exception.py",
    "$root\api\middleware\logging.py",

    # Exception Handlers
    "$root\api\exception_handlers\__init__.py",
    "$root\api\exception_handlers\domain_handler.py",
    "$root\api\exception_handlers\validation_handler.py",
    "$root\api\exception_handlers\infrastructure_handler.py",

    # Routers
    "$root\api\routers\__init__.py",
    "$root\api\routers\ai_router.py",
    "$root\api\routers\assessment_router.py",
    "$root\api\routers\discovery_router.py",
    "$root\api\routers\lead_router.py",
    "$root\api\routers\recommendation_router.py",
    "$root\api\routers\health_router.py",

    # Schemas
    "$root\schemas\__init__.py",

    # Request Schemas
    "$root\schemas\requests\__init__.py",

    # Response Schemas
    "$root\schemas\responses\__init__.py"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " Presentation Layer Created Successfully " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green