from pydantic import BaseModel


class EmailOutreach(BaseModel):
    subject: str
    message: str
    call_to_action: str


class LinkedInOutreach(BaseModel):
    message: str
    call_to_action: str


class WhatsAppOutreach(BaseModel):
    message: str


class PhoneScript(BaseModel):
    opening: str
    talking_points: list[str]
    call_to_action: str


class DiscoveryObjective(BaseModel):
    meeting_goal: str
    discovery_questions: list[str]


class OutreachGenerationResponse(BaseModel):
    email: EmailOutreach

    linkedin: LinkedInOutreach

    whatsapp: WhatsAppOutreach

    phone: PhoneScript

    discovery: DiscoveryObjective