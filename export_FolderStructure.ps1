$exclude = @(
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build"
)

function Show-Tree {
    param(
        [string]$Path,
        [string]$Indent = ""
    )

    Get-ChildItem $Path |
        Where-Object {
            $exclude -notcontains $_.Name
        } |
        Sort-Object PSIsContainer, Name -Descending |
        ForEach-Object {

            "$Indent$($_.Name)"

            if ($_.PSIsContainer) {
                Show-Tree $_.FullName "$Indent    "
            }
        }
}

Show-Tree "." | Out-File AiSDR_project_structure.txt -Encoding UTF8