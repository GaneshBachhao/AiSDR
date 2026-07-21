$folders = @(
    "app\application",
    "app\application\discovery",
    "app\application\company_intelligence",
    "app\application\qualification",
    "app\application\recommendation",
    "app\application\lead",
    "app\application\contact",
    "app\application\email",
    "app\application\pipeline"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

$files = @(
    "app\application\__init__.py",

    "app\application\discovery\__init__.py",
    "app\application\discovery\discover_companies.py",

    "app\application\company_intelligence\__init__.py",
    "app\application\company_intelligence\enrich_company.py",

    "app\application\qualification\__init__.py",
    "app\application\qualification\qualify_company.py",

    "app\application\recommendation\__init__.py",
    "app\application\recommendation\recommend_services.py",

    "app\application\lead\__init__.py",
    "app\application\lead\create_lead.py",

    "app\application\contact\__init__.py",
    "app\application\contact\discover_contacts.py",

    "app\application\email\__init__.py",
    "app\application\email\generate_email.py",
    "app\application\email\send_email.py",

    "app\application\pipeline\__init__.py",
    "app\application\pipeline\run_sales_pipeline.py"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host ""
Write-Host "Application layer created successfully." -ForegroundColor Green