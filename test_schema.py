from app.schemas.lead_schema import LeadCreate

lead = LeadCreate(
    company_name="OpenAI",
    email="contact@example.com"
)

print(lead.model_dump())