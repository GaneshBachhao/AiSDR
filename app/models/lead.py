from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255), nullable=False)

    contact_name = Column(String(255), nullable=True)

    email = Column(String(255), nullable=True)

    phone = Column(String(50), nullable=True)

    website = Column(String(255), nullable=True)

    industry = Column(String(100), nullable=True)

    status = Column(
        String(50),
        default="NEW"
    )

    notes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )