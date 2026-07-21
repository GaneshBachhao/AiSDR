# ============================================
# Pamacore Labs - Application Layer Structure
# ============================================

$root = "app/application"

$folders = @(
    "$root",

    "$root/common",
    "$root/common/commands",
    "$root/common/queries",
    "$root/common/dto",
    "$root/common/exceptions",
    "$root/common/interfaces",
    "$root/common/mappers",
    "$root/common/ports",
    "$root/common/services",
    "$root/common/unit_of_work",
    "$root/common/validation",
    "$root/common/behaviors",

    "$root/lead",
    "$root/lead/commands",
    "$root/lead/queries",
    "$root/lead/handlers",
    "$root/lead/dto",
    "$root/lead/mappers",
    "$root/lead/validators",

    "$root/discovery",
    "$root/discovery/commands",
    "$root/discovery/queries",
    "$root/discovery/handlers",
    "$root/discovery/dto",
    "$root/discovery/mappers",
    "$root/discovery/validators",

    "$root/assessment",
    "$root/assessment/commands",
    "$root/assessment/queries",
    "$root/assessment/handlers",
    "$root/assessment/dto",
    "$root/assessment/mappers",
    "$root/assessment/validators",

    "$root/recommendation",
    "$root/recommendation/commands",
    "$root/recommendation/queries",
    "$root/recommendation/handlers",
    "$root/recommendation/dto",
    "$root/recommendation/mappers",
    "$root/recommendation/validators"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
}

foreach ($folder in $folders) {
    New-Item -ItemType File -Path (Join-Path $folder "__init__.py") -Force | Out-Null
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host " Application Layer Created Successfully" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green