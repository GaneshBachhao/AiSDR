# ==========================================================
# Create Infrastructure Folder Structure
# ==========================================================

$Root = "app\infrastructure"

# ----------------------------------------------------------
# Folders
# ----------------------------------------------------------

$Folders = @(

    "$Root"

    "$Root\ai"
    "$Root\ai\clients"
    "$Root\ai\providers"
    "$Root\ai\mappers"

    "$Root\persistence"
    "$Root\persistence\repositories"
    "$Root\persistence\repositories\lead"
    "$Root\persistence\repositories\discovery"
    "$Root\persistence\repositories\assessment"
    "$Root\persistence\repositories\recommendation"
    "$Root\persistence\repositories\ai"

    "$Root\persistence\sqlalchemy"
    "$Root\persistence\unit_of_work"

    "$Root\configuration"

    "$Root\dependency_injection"

    "$Root\telemetry"

    "$Root\cache"

    "$Root\messaging"
)

foreach ($Folder in $Folders) {
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $Folder | Out-Null
}

# ----------------------------------------------------------
# Python Files
# ----------------------------------------------------------

$Files = @(

    "$Root\__init__.py"

    "$Root\ai\__init__.py"

    "$Root\ai\clients\__init__.py"
    "$Root\ai\clients\base_ai_client.py"
    "$Root\ai\clients\openai_client.py"
    "$Root\ai\clients\gemini_client.py"
    "$Root\ai\clients\ollama_client.py"

    "$Root\ai\providers\__init__.py"
    "$Root\ai\providers\base_provider.py"
    "$Root\ai\providers\openai_provider.py"
    "$Root\ai\providers\gemini_provider.py"
    "$Root\ai\providers\ollama_provider.py"
    "$Root\ai\providers\mock_provider.py"
    "$Root\ai\providers\provider_factory.py"

    "$Root\ai\mappers\__init__.py"
    "$Root\ai\mappers\ai_request_mapper.py"
    "$Root\ai\mappers\ai_response_mapper.py"

    "$Root\persistence\__init__.py"

    "$Root\persistence\repositories\__init__.py"

    "$Root\persistence\repositories\lead\__init__.py"

    "$Root\persistence\repositories\discovery\__init__.py"

    "$Root\persistence\repositories\assessment\__init__.py"

    "$Root\persistence\repositories\recommendation\__init__.py"

    "$Root\persistence\repositories\ai\__init__.py"

    "$Root\persistence\sqlalchemy\__init__.py"

    "$Root\persistence\unit_of_work\__init__.py"

    "$Root\configuration\__init__.py"
    "$Root\configuration\settings.py"
    "$Root\configuration\provider_settings.py"

    "$Root\dependency_injection\__init__.py"
    "$Root\dependency_injection\container.py"
    "$Root\dependency_injection\providers.py"

    "$Root\telemetry\__init__.py"

    "$Root\cache\__init__.py"

    "$Root\messaging\__init__.py"
)

foreach ($File in $Files) {
    if (!(Test-Path $File)) {
        New-Item `
            -ItemType File `
            -Path $File | Out-Null
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " Infrastructure structure created"
Write-Host "==========================================" -ForegroundColor Green