from sqlalchemy import Column, DateTime
import uuid
from datetime import datetime

from ..config.database import Base
from ..config.typing import GUID


class BaseModel(Base):
    __abstract__ = True

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
